import os
import sys
import django
import random
from datetime import datetime, timedelta

# Setup Django environment
sys.path.append('/home/debian/luis/proyecto-BBDD-Casa-Apuestas/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sportpredict.settings')
django.setup()

from django.utils import timezone
from sportpredict.models import Usuario, Partido, Prediccion, Equipo
from sportpredict.db.neo4j_utils import Neo4jClient

def sync_data():
    print("Starting Neo4j Synchronization...")
    client = Neo4jClient()
    
    if not client.verify_connectivity():
        print("[ERROR] Could not connect to Neo4j")
        return

    # 1. Sync Users
    print("\n1. Syncing Users...")
    users = Usuario.objects.all()
    for user in users:
        client.create_user(user.id, user.username, user.email)
    print(f"[OK] Synced {users.count()} users")

    # 2. Sync Matches
    print("\n2. Syncing Matches...")
    matches = Partido.objects.all()
    for match in matches:
        client.create_match(
            match.id, 
            match.equipo_local.nombre, 
            match.equipo_visitante.nombre, 
            match.equipo_local.deporte.nombre,
            match.fecha_hora
        )
    print(f"[OK] Synced {matches.count()} matches")

    # 3. Sync Existing Predictions
    print("\n3. Syncing Existing Predictions...")
    predictions = Prediccion.objects.all()
    for pred in predictions:
        client.create_prediction(pred.usuario.id, pred.partido.id, pred.prediccion)
    print(f"[OK] Synced {predictions.count()} predictions")

    # 4. Generate Synthetic Data (Bots)
    print("\n4. Generating Synthetic Data for Recommendations...")
    
    # Create 5 bots
    bots = []
    for i in range(1, 6):
        username = f"bot_expert_{i}"
        email = f"bot{i}@example.com"
        user, created = Usuario.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': 'Bot',
                'last_name': f'Expert {i}',
                'is_active': True,
                'puntos_totales': random.randint(100, 500)
            }
        )
        if created:
            user.set_password('botpass123')
            user.save()
            print(f"Created bot: {username}")
        
        client.create_user(user.id, user.username, user.email)
        bots.append(user)

    # Get a real user to generate recommendations for (e.g., the one we just used)
    # Assuming the last created user is our test user
    target_user = Usuario.objects.exclude(username__startswith='bot').last()
    
    if target_user:
        print(f"Generating data to recommend for: {target_user.username}")
        
        # Get matches predicted by target user
        target_preds = Prediccion.objects.filter(usuario=target_user)
        target_match_ids = [p.partido.id for p in target_preds]
        
        if not target_match_ids:
            print("[WARN] Target user has no predictions. Making one for them...")
            # Find a pending match
            match = Partido.objects.filter(estado='PENDIENTE').first()
            if match:
                Prediccion.objects.create(usuario=target_user, partido=match, prediccion="1-0")
                client.create_prediction(target_user.id, match.id, "1-0")
                target_match_ids.append(match.id)
                print(f"Created prediction for {target_user.username} on match {match}")

        # Have bots predict on the SAME matches (to create similarity)
        for match_id in target_match_ids:
            match = Partido.objects.get(id=match_id)
            for bot in bots:
                # 80% chance to predict the same match
                if random.random() < 0.8:
                    # 70% chance to predict the SAME outcome (high similarity)
                    pred_value = "1-0" # Simplified, ideally match the user's prediction
                    
                    # Check if bot already predicted
                    if not Prediccion.objects.filter(usuario=bot, partido=match).exists():
                        Prediccion.objects.create(usuario=bot, partido=match, prediccion=pred_value)
                        client.create_prediction(bot.id, match.id, pred_value)
                        print(f"Bot {bot.username} predicted on shared match {match}")

        # Have bots predict on OTHER future matches (to generate recommendations)
        future_matches = Partido.objects.filter(
            estado='PENDIENTE', 
            fecha_hora__gt=timezone.now()
        ).exclude(id__in=target_match_ids)[:5]

        for match in future_matches:
            for bot in bots:
                if random.random() < 0.6:
                    if not Prediccion.objects.filter(usuario=bot, partido=match).exists():
                        Prediccion.objects.create(usuario=bot, partido=match, prediccion="2-1")
                        client.create_prediction(bot.id, match.id, "2-1")
                        print(f"Bot {bot.username} predicted on recommendation candidate {match}")

    client.close()
    print("\nSynchronization and Generation Complete!")

if __name__ == "__main__":
    sync_data()
