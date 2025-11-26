"""
API de Analytics - Dashboard y métricas desde MongoDB
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import datetime, timedelta

from sportpredict.models import Usuario, Partido, Prediccion
from sportpredict.db.mongodb.analytics import AnalyticsManager


# Inicializar managers
analytics_manager = AnalyticsManager()


@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_metrics(request):
    """
    Obtener métricas del dashboard
    GET /api/analytics/dashboard/
    """
    try:
        # Obtener métricas de MongoDB
        mongo_metrics = analytics_manager.obtener_metricas_dashboard()
        
        # Calcular métricas en tiempo real de PostgreSQL
        total_users = Usuario.objects.filter(is_active=True).count()
        total_matches = Partido.objects.count()
        total_predictions = Prediccion.objects.count()
        
        # Predicciones de hoy
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        predictions_today = Prediccion.objects.filter(
            fecha_prediccion__gte=today_start
        ).count()
        
        # Partidos próximos
        upcoming_matches = Partido.objects.filter(
            estado='PENDIENTE',
            fecha_hora__gte=datetime.now()
        ).count()
        
        # Partidos en vivo
        live_matches = Partido.objects.filter(estado='EN_JUEGO').count()
        
        metrics = {
            'total_users': total_users,
            'total_matches': total_matches,
            'total_predictions': total_predictions,
            'predictions_today': predictions_today,
            'upcoming_matches': upcoming_matches,
            'live_matches': live_matches,
            'timestamp': datetime.now().isoformat()
        }
        
        # Combinar con métricas de MongoDB si existen
        if mongo_metrics:
            metrics.update(mongo_metrics)
        
        return Response(metrics)
        
    except Exception as e:
        return Response(
            {'error': f'Error cargando métricas: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def advanced_stats(request):
    """
    Obtener estadísticas avanzadas
    GET /api/analytics/stats/
    """
    try:
        # Obtener estadísticas avanzadas de MongoDB
        stats = analytics_manager.obtener_estadisticas_avanzadas()
        
        if not stats:
            # Si no hay datos en MongoDB, calcular desde PostgreSQL
            stats = {
                'total_predictions': Prediccion.objects.count(),
                'active_users': Usuario.objects.filter(is_active=True).count(),
                'sports_distribution': {},
                'timestamp': datetime.now().isoformat()
            }
        
        return Response(stats)
        
    except Exception as e:
        return Response(
            {'error': f'Error cargando estadísticas avanzadas: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def historical_dashboard(request):
    """
    Obtener histórico de métricas del dashboard
    GET /api/analytics/historical/
    Query params: days (default: 30)
    """
    try:
        days = int(request.GET.get('days', 30))
        
        # Obtener histórico desde MongoDB
        historical_data = analytics_manager.obtener_historico_dashboard(dias=days)
        
        return Response({
            'historical_data': historical_data,
            'days': days,
            'count': len(historical_data)
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error cargando histórico: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_dashboard(request):
    """
    Actualizar métricas del dashboard manualmente
    POST /api/analytics/update/
    """
    try:
        # Solo permitir a administradores
        if not request.user.is_staff:
            return Response(
                {'error': 'No tienes permisos para realizar esta acción'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Actualizar dashboard
        result = analytics_manager.actualizar_dashboard_automatico()
        
        if result:
            return Response({
                'message': 'Dashboard actualizado exitosamente'
            })
        else:
            return Response(
                {'error': 'Error actualizando dashboard'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    except Exception as e:
        return Response(
            {'error': f'Error actualizando dashboard: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
