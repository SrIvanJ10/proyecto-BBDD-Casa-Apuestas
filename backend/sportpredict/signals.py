from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Usuario, Partido, Prediccion
from .db.neo4j_utils import Neo4jClient
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Usuario)
def sync_user_to_neo4j(sender, instance, created, **kwargs):
    """Sync user creation/update to Neo4j"""
    try:
        client = Neo4jClient()
        client.create_user(
            user_id=instance.id,
            username=instance.username,
            email=instance.email
        )
    except Exception as e:
        logger.error(f"Error syncing user to Neo4j: {e}")

@receiver(post_save, sender=Partido)
def sync_match_to_neo4j(sender, instance, created, **kwargs):
    """Sync match creation/update to Neo4j"""
    try:
        client = Neo4jClient()
        # Ensure related fields are available
        sport_name = instance.equipo_local.deporte.nombre if instance.equipo_local and instance.equipo_local.deporte else "Unknown"
        team_home = instance.equipo_local.nombre if instance.equipo_local else "Unknown"
        team_away = instance.equipo_visitante.nombre if instance.equipo_visitante else "Unknown"
        
        client.create_match(
            match_id=instance.id,
            team_home=team_home,
            team_away=team_away,
            sport=sport_name,
            date=instance.fecha_hora
        )
    except Exception as e:
        logger.error(f"Error syncing match to Neo4j: {e}")

@receiver(post_save, sender=Prediccion)
def sync_prediction_to_neo4j(sender, instance, created, **kwargs):
    """Sync prediction creation to Neo4j"""
    if created:
        try:
            client = Neo4jClient()
            client.create_prediction(
                user_id=instance.usuario.id,
                match_id=instance.partido.id,
                prediction=instance.prediccion
            )
        except Exception as e:
            logger.error(f"Error syncing prediction to Neo4j: {e}")
