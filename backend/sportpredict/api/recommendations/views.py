"""
API de Recomendaciones - Integración con Neo4j
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from datetime import datetime

from sportpredict.models import Partido, Usuario
from sportpredict.db.neo4j_utils import Neo4jClient

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommended_matches(request):
    """
    Obtener partidos recomendados para el usuario usando Neo4j
    GET /api/recommendations/matches/
    """
    try:
        user = request.user
        limit = int(request.GET.get('limit', 10))
        
        client = Neo4jClient()
        
        # Obtener IDs de partidos recomendados desde Neo4j (Filtrado Colaborativo)
        # Solo muestra partidos donde los amigos han apostado
        recommended_ids = client.get_recommended_matches(user.id, limit=limit)
        
        recommended_matches = []
        if recommended_ids:
            # Recuperar objetos Partido de PostgreSQL
            recommended_matches = Partido.objects.filter(
                id__in=recommended_ids,
                estado='PENDIENTE',
                fecha_hora__gte=datetime.now()
            ).select_related(
                'equipo_local__deporte', 
                'equipo_visitante__deporte'
            )
        
        # Serializar
        from sportpredict.serializers import PartidoListSerializer
        serializer = PartidoListSerializer(recommended_matches, many=True)
        
        return Response({
            'recommended_matches': serializer.data,
            'count': len(serializer.data),
            'algorithm': 'neo4j_collaborative_filtering',
            'source': 'friends_predictions_only'
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error generando recomendaciones: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def similar_users(request):
    """
    Obtener usuarios similares usando Neo4j
    GET /api/recommendations/users/
    """
    try:
        user = request.user
        limit = int(request.GET.get('limit', 10))
        
        client = Neo4jClient()
        
        # Obtener IDs de usuarios similares desde Neo4j
        similar_ids = client.get_similar_users(user.id, limit=limit)
        
        similar_users = []
        if similar_ids:
            similar_users = Usuario.objects.filter(
                id__in=similar_ids
            ).order_by('-puntos_totales')
            
        # Fallback si no hay suficientes
        if len(similar_users) < limit:
            exclude_ids = [u.id for u in similar_users] + [user.id]
            needed = limit - len(similar_users)
            
            others = Usuario.objects.filter(
                is_active=True
            ).exclude(
                id__in=exclude_ids
            ).order_by('-puntos_totales')[:needed]
            
            similar_users = list(similar_users) + list(others)
        
        # Serializar
        from sportpredict.serializers import UsuarioSerializer
        serializer = UsuarioSerializer(similar_users, many=True)
        
        return Response({
            'similar_users': serializer.data,
            'count': len(serializer.data),
            'algorithm': 'neo4j_user_similarity'
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error buscando usuarios similares: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trending_matches(request):
    """
    Obtener partidos en tendencia (más predicciones)
    GET /api/recommendations/trending/
    """
    try:
        limit = int(request.GET.get('limit', 10))
        
        # Para trending seguimos usando PostgreSQL ya que es una agregación simple
        # Podríamos usar Neo4j también, pero SQL es eficiente para esto
        trending = Partido.objects.filter(
            estado='PENDIENTE',
            fecha_hora__gte=datetime.now()
        ).annotate(
            prediction_count=Count('prediccion')
        ).filter(
            prediction_count__gt=0
        ).select_related(
            'equipo_local__deporte',
            'equipo_visitante__deporte'
        ).order_by('-prediction_count', 'fecha_hora')[:limit]
        
        # Serializar
        from sportpredict.serializers import PartidoListSerializer
        serializer = PartidoListSerializer(trending, many=True)
        
        trending_data = []
        for idx, match in enumerate(trending):
            match_data = serializer.data[idx]
            match_data['prediction_count'] = match.prediction_count
            match_data['trending_rank'] = idx + 1
            trending_data.append(match_data)
        
        return Response({
            'trending_matches': trending_data,
            'count': len(trending_data)
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error obteniendo partidos en tendencia: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def debug_neo4j(request):
    try:
        from sportpredict.models import Usuario, Prediccion
        from sportpredict.db.neo4j_utils import Neo4jClient
        
        output = []
        
        try:
            dios = Usuario.objects.get(username='dios')
            rodri = Usuario.objects.get(username='RodriBdO')
            output.append(f"Dios ID: {dios.id}")
            output.append(f"Rodri ID: {rodri.id}")
        except Usuario.DoesNotExist:
            return Response({'error': "Users not found in Postgres"})

        client = Neo4jClient()
        
        # Check friendship
        are_friends = client.are_friends(dios.id, rodri.id)
        output.append(f"Are friends in Neo4j: {are_friends}")

        # Check Rodri's predictions in Postgres
        rodri_preds = Prediccion.objects.filter(usuario=rodri)
        output.append(f"Rodri has {rodri_preds.count()} predictions in Postgres")
        
        for p in rodri_preds:
            output.append(f" - Match {p.partido.id} ({p.partido.equipo_local} vs {p.partido.equipo_visitante}), Status: {p.partido.estado}")

        # Check Rodri's predictions in Neo4j
        with client._driver.session() as session:
            query = "MATCH (u:User {id: $user_id})-[:PREDICTED]->(m:Match) RETURN m.id as match_id"
            result = session.run(query, user_id=str(rodri.id))
            neo4j_preds = [record["match_id"] for record in result]
            output.append(f"Rodri has {len(neo4j_preds)} predictions in Neo4j: {neo4j_preds}")

        # Check recommendations for Dios
        recs = client.get_recommended_matches(dios.id)
        output.append(f"Recommendations for Dios from Neo4j: {recs}")
        
        return Response({'debug_output': output})
    except Exception as e:
        return Response({'error': str(e)})
