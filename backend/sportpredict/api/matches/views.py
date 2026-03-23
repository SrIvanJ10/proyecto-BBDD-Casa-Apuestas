"""
API de Partidos - Usando PostgreSQL + MongoDB (estadísticas)
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime, timedelta

from sportpredict.models import Partido, Equipo, Prediccion
from sportpredict.serializers import PartidoSerializer, PartidoListSerializer
from sportpredict.db.mongodb.analytics import AnalyticsManager
from sportpredict.db.mongodb.partidos import PartidoStatsManager


# Inicializar managers
analytics_manager = AnalyticsManager()
stats_manager = PartidoStatsManager()


@api_view(['GET'])
@permission_classes([AllowAny])
def matches_list(request):
    """
    Obtener lista de partidos con filtros avanzados
    GET /api/matches/
    Query params: 
        - sport: nombre del deporte
        - status: all, finished, live, incoming (<24h), upcoming (24h-7days), future (>7days)
        - league: nombre de la liga
        - team: nombre del equipo
        - page, page_size: paginación
    """
    try:
        # Obtener parámetros de filtro
        sport_filter = request.GET.get('sport')
        status_filter = request.GET.get('status', 'all')
        league_filter = request.GET.get('league')
        team_filter = request.GET.get('team')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        
        # Query base
        queryset = Partido.objects.select_related(
            'equipo_local__deporte',
            'equipo_visitante__deporte'
        ).all()
        
        # Aplicar filtros de deporte
        if sport_filter:
            queryset = queryset.filter(
                Q(equipo_local__deporte__nombre__icontains=sport_filter) |
                Q(equipo_visitante__deporte__nombre__icontains=sport_filter)
            )
        
        # Aplicar filtros avanzados de estado
        now = timezone.now()
        incoming_threshold = now + timedelta(hours=24)
        
        # Calcular el inicio de la próxima semana (próximo lunes a las 00:00)
        # now.weekday() devuelve 0 para lunes, 1 para martes, etc.
        days_until_next_monday = (7 - now.weekday()) % 7
        if days_until_next_monday == 0:
            # Si hoy es lunes, la próxima semana empieza en 7 días
            days_until_next_monday = 7
        next_week_start = (now + timedelta(days=days_until_next_monday)).replace(hour=0, minute=0, second=0, microsecond=0)
        
        if status_filter == 'finished':
            # Partidos finalizados: con estado FINALIZADO o que comenzaron hace más de 120 minutos
            match_ended_time = now - timedelta(minutes=120)
            queryset = queryset.filter(
                Q(estado='FINALIZADO') | 
                Q(estado='PENDIENTE', fecha_hora__lt=match_ended_time)
            )
        elif status_filter == 'live':
            # Partidos en vivo: desde su hora de inicio hasta 120 minutos después
            live_end_threshold = now + timedelta(minutes=120)
            queryset = queryset.filter(
                estado='PENDIENTE',
                fecha_hora__lte=now,  # Ya comenzó
                fecha_hora__gte=now - timedelta(minutes=120)  # Comenzó hace menos de 120 min
            )
        elif status_filter == 'incoming':
            # Partidos que empiezan en las próximas 24 horas
            queryset = queryset.filter(
                estado='PENDIENTE',
                fecha_hora__gte=now,
                fecha_hora__lt=incoming_threshold
            )
        elif status_filter == 'upcoming':
            # Partidos que empiezan esta semana (hasta el próximo lunes)
            queryset = queryset.filter(
                estado='PENDIENTE',
                fecha_hora__gte=now,
                fecha_hora__lt=next_week_start
            )
        elif status_filter == 'future':
            # Partidos que empiezan a partir de la próxima semana (>= próximo lunes)
            queryset = queryset.filter(
                estado='PENDIENTE',
                fecha_hora__gte=next_week_start
            )
        # 'all' no filtra por estado
        
        if league_filter:
            queryset = queryset.filter(liga__icontains=league_filter)
        
        if team_filter:
            queryset = queryset.filter(
                Q(equipo_local__nombre__icontains=team_filter) |
                Q(equipo_visitante__nombre__icontains=team_filter)
            )
        
        # Ordenar por fecha
        queryset = queryset.order_by('fecha_hora')
        
        # Paginación
        total_matches = queryset.count()
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_matches = queryset[start_idx:end_idx]
        
        # Serializar
        serializer = PartidoListSerializer(paginated_matches, many=True)
        
        # Log de actividad si el usuario está autenticado
        if request.user.is_authenticated:
            analytics_manager.registrar_actividad_usuario(
                user_id=request.user.id,
                action='viewed_matches_list',
                metadata={
                    'filters': {
                        'sport': sport_filter,
                        'status': status_filter,
                        'league': league_filter,
                        'team': team_filter
                    },
                    'page': page
                }
            )
        
        return Response({
            'matches': serializer.data,
            'pagination': {
                'total': total_matches,
                'page': page,
                'page_size': page_size,
                'total_pages': (total_matches + page_size - 1) // page_size
            },
            'filters_applied': {
                'sport': sport_filter,
                'status': status_filter,
                'league': league_filter,
                'team': team_filter
            }
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error cargando partidos: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



@api_view(['GET'])
@permission_classes([AllowAny])
def match_detail(request, match_id):
    """
    Obtener detalles de un partido específico
    GET /api/matches/{id}/
    """
    try:
        # Buscar partido
        try:
            partido = Partido.objects.select_related(
                'equipo_local__deporte',
                'equipo_visitante__deporte'
            ).get(id=match_id)
        except Partido.DoesNotExist:
            return Response(
                {'error': 'Partido no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Serializar partido
        serializer = PartidoSerializer(partido)
        match_data = serializer.data
        
        # Obtener estadísticas de MongoDB
        mongo_stats = stats_manager.obtener_estadisticas_partido(match_id)
        if mongo_stats:
            match_data['statistics'] = mongo_stats
        
        # Obtener predicciones populares
        predicciones = Prediccion.objects.filter(partido=partido)
        predicciones_count = predicciones.values('prediccion').annotate(
            count=Count('prediccion')
        ).order_by('-count')[:5]
        
        total_predicciones = predicciones.count()
        popular_predictions = []
        for pred in predicciones_count:
            popular_predictions.append({
                'score': pred['prediccion'],
                'count': pred['count'],
                'percentage': round((pred['count'] / total_predicciones * 100), 1) if total_predicciones > 0 else 0
            })
        
        match_data['popular_predictions'] = popular_predictions
        match_data['total_predictions'] = total_predicciones
        
        # Si el usuario está autenticado, obtener su predicción
        if request.user.is_authenticated:
            user_prediction = Prediccion.objects.filter(
                usuario=request.user,
                partido=partido
            ).first()
            
            if user_prediction:
                match_data['user_prediction'] = {
                    'id': user_prediction.id,
                    'prediccion': user_prediction.prediccion,
                    'puntos_obtenidos': user_prediction.puntos_obtenidos,
                    'fecha_prediccion': user_prediction.fecha_prediccion,
                    'correcta': user_prediction.correcta
                }
            else:
                match_data['user_prediction'] = None
            
            # Log de actividad
            analytics_manager.registrar_actividad_usuario(
                user_id=request.user.id,
                action='viewed_match_detail',
                metadata={'match_id': match_id}
            )
        
        return Response(match_data)
        
    except Exception as e:
        return Response(
            {'error': f'Error cargando partido: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def upcoming_matches(request):
    """
    Obtener partidos próximos
    GET /api/matches/upcoming/
    Query params: sport, league, limit
    """
    try:
        sport_filter = request.GET.get('sport')
        league_filter = request.GET.get('league')
        limit = int(request.GET.get('limit', 10))
        
        # Query: partidos pendientes en el futuro
        queryset = Partido.objects.filter(
            estado='PENDIENTE',
            fecha_hora__gte=datetime.now()
        ).select_related(
            'equipo_local__deporte',
            'equipo_visitante__deporte'
        )
        
        # Aplicar filtros
        if sport_filter:
            queryset = queryset.filter(
                Q(equipo_local__deporte__nombre__icontains=sport_filter)
            )
        
        if league_filter:
            queryset = queryset.filter(liga__icontains=league_filter)
        
        # Ordenar por fecha más cercana y limitar
        queryset = queryset.order_by('fecha_hora')[:limit]
        
        # Serializar
        serializer = PartidoListSerializer(queryset, many=True)
        
        # Log de actividad
        if request.user.is_authenticated:
            analytics_manager.registrar_actividad_usuario(
                user_id=request.user.id,
                action='viewed_upcoming_matches',
                metadata={
                    'sport_filter': sport_filter,
                    'league_filter': league_filter,
                    'limit': limit
                }
            )
        
        return Response({
            'matches': serializer.data,
            'count': len(serializer.data)
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error cargando partidos próximos: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def live_matches(request):
    """
    Obtener partidos en vivo
    GET /api/matches/live/
    """
    try:
        # Query: partidos que están en su ventana de juego (desde inicio hasta 120 min después)
        now = timezone.now()
        queryset = Partido.objects.filter(
            estado='PENDIENTE',
            fecha_hora__lte=now,  # Ya comenzó
            fecha_hora__gte=now - timedelta(minutes=120)  # Comenzó hace menos de 120 min
        ).select_related(
            'equipo_local__deporte',
            'equipo_visitante__deporte'
        ).order_by('-fecha_hora')
        
        # Serializar
        serializer = PartidoListSerializer(queryset, many=True)
        
        # Log de actividad
        if request.user.is_authenticated:
            analytics_manager.registrar_actividad_usuario(
                user_id=request.user.id,
                action='viewed_live_matches',
                metadata={'count': len(serializer.data)}
            )
        
        return Response({
            'matches': serializer.data,
            'count': len(serializer.data),
            'last_updated': datetime.now().isoformat()
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error cargando partidos en vivo: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def finished_matches(request):
    """
    Obtener partidos finalizados
    GET /api/matches/finished/
    Query params: page, page_size
    """
    try:
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        # Query: partidos finalizados (estado FINALIZADO o que comenzaron hace más de 120 min)
        now = timezone.now()
        match_ended_time = now - timedelta(minutes=120)
        queryset = Partido.objects.filter(
            Q(estado='FINALIZADO') | 
            Q(estado='PENDIENTE', fecha_hora__lt=match_ended_time)
        ).select_related(
            'equipo_local__deporte',
            'equipo_visitante__deporte'
        ).order_by('-fecha_hora')
        
        # Paginación
        total_matches = queryset.count()
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_matches = queryset[start_idx:end_idx]
        
        # Serializar
        serializer = PartidoListSerializer(paginated_matches, many=True)
        
        # Log de actividad
        if request.user.is_authenticated:
            analytics_manager.registrar_actividad_usuario(
                user_id=request.user.id,
                action='viewed_finished_matches',
                metadata={'page': page, 'page_size': page_size}
            )
        
        return Response({
            'matches': serializer.data,
            'pagination': {
                'total': total_matches,
                'page': page,
                'page_size': page_size,
                'total_pages': (total_matches + page_size - 1) // page_size
            }
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error cargando partidos finalizados: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
