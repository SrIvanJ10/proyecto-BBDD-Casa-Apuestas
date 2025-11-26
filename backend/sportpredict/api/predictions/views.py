"""
API de Predicciones - Usando PostgreSQL + Redis (rate limiting) + MongoDB (logs)
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import datetime, timedelta

from sportpredict.models import Prediccion, Partido, Usuario
from sportpredict.serializers import PrediccionSerializer, PrediccionCreateSerializer
from sportpredict.db.mongodb.analytics import AnalyticsManager
from ..utils.rate_limiter import RateLimiter


# Inicializar managers
analytics_manager = AnalyticsManager()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_prediction(request):
    """
    Crear una nueva predicción
    POST /api/predictions/
    Body: {partido_id, prediccion}
    """
    try:
        user = request.user
        
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> db693ad (v0.9)
        # Verificar límites de suscripción
        if not user.puede_apostar():
            predicciones_count = Prediccion.objects.filter(usuario=user).count()
            if user.tipo_suscripcion == 'FREE':
                return Response({
                    'error': 'Límite de apuestas alcanzado',
                    'message': 'Has alcanzado el límite de 5 apuestas del plan gratuito. Actualiza a Premium para apuestas ilimitadas.',
                    'subscription_type': 'FREE',
                    'predictions_made': predicciones_count,
                    'max_predictions': 5
                }, status=status.HTTP_403_FORBIDDEN)
            else:  # PREMIUM
                return Response({
                    'error': 'Puntos insuficientes',
                    'message': 'Necesitas al menos 500 puntos para usar el plan Premium.',
                    'subscription_type': 'PREMIUM',
                    'current_points': user.puntos_totales,
                    'required_points': 500
                }, status=status.HTTP_403_FORBIDDEN)
        
<<<<<<< HEAD
=======
>>>>>>> d381094 (v0.14)
=======
>>>>>>> db693ad (v0.9)
        # Verificar rate limiting (máximo 10 predicciones por día)
        rate_limiter = RateLimiter(user.id)
        if not rate_limiter.can_make_prediction():
            return Response({
                'error': 'Límite de predicciones excedido',
                'message': 'Máximo 10 predicciones por día permitidas',
                'remaining_predictions': 0,
                'remaining_time': rate_limiter.get_remaining_time()
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        # Validar datos
        serializer = PrediccionCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Datos inválidos', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        partido = serializer.validated_data['partido']
        prediccion_simple = serializer.validated_data.get('prediccion', '')
        
        # Verificar que el partido esté pendiente
        if partido.estado != 'PENDIENTE':
            return Response(
                {'error': 'No se pueden hacer predicciones para partidos que no están pendientes'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar que el partido no haya empezado
        if partido.fecha_hora <= timezone.now():
            return Response(
                {'error': 'No se pueden hacer predicciones para partidos que ya empezaron'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar que el usuario no tenga ya una predicción para este partido
        if Prediccion.objects.filter(usuario=user, partido=partido).exists():
            return Response(
                {'error': 'Ya tienes una predicción para este partido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Crear predicción
        # Crear predicción con todos los campos
        prediccion_data = {
            'usuario': user,
            'partido': partido,
            'prediccion': serializer.validated_data.get('prediccion', ''),
            'pred_goles_local': serializer.validated_data.get('pred_goles_local'),
            'pred_goles_visitante': serializer.validated_data.get('pred_goles_visitante'),
            'pred_amarillas_local': serializer.validated_data.get('pred_amarillas_local'),
            'pred_amarillas_visitante': serializer.validated_data.get('pred_amarillas_visitante'),
            'pred_rojas_local': serializer.validated_data.get('pred_rojas_local'),
            'pred_rojas_visitante': serializer.validated_data.get('pred_rojas_visitante'),
            'pred_expulsiones_local': serializer.validated_data.get('pred_expulsiones_local'),
            'pred_expulsiones_visitante': serializer.validated_data.get('pred_expulsiones_visitante'),
            'pred_mvp_jugador': serializer.validated_data.get('pred_mvp_jugador'),
        }
        
        nueva_prediccion = Prediccion.objects.create(**prediccion_data)
        
        # Registrar en rate limiter
        rate_limiter.record_prediction()
        
        # Log en MongoDB
        analytics_manager.registrar_actividad_usuario(
            user_id=user.id,
            action='create_prediction',
            metadata={
                'prediction_id': nueva_prediccion.id,
                'match_id': partido.id,
                'prediction': prediccion_simple
            }
        )
        
        # Serializar respuesta
        response_serializer = PrediccionSerializer(nueva_prediccion)
        
        return Response({
            'message': 'Predicción creada exitosamente',
            'prediction': response_serializer.data,
            'remaining_predictions_today': rate_limiter.get_remaining_predictions()
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': f'Error creando predicción: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_predictions(request):
    """
    Obtener predicciones del usuario
    GET /api/predictions/
    Query params: status (all, pending, scored), page, page_size
    """
    try:
        user = request.user
        status_filter = request.GET.get('status', 'all')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        
        # Query base
        queryset = Prediccion.objects.filter(
            usuario=user
        ).select_related(
            'partido__equipo_local',
            'partido__equipo_visitante'
        )
        
        # Aplicar filtros
        if status_filter == 'pending':
            queryset = queryset.filter(partido__estado='PENDIENTE')
        elif status_filter == 'scored':
            queryset = queryset.filter(partido__estado='FINALIZADO')
        
        # Ordenar por fecha de predicción (más reciente primero)
        queryset = queryset.order_by('-fecha_prediccion')
        
        # Paginación
        total_predictions = queryset.count()
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_predictions = queryset[start_idx:end_idx]
        
        # Serializar
        serializer = PrediccionSerializer(paginated_predictions, many=True)
        
        # Calcular estadísticas del usuario
        stats = {
            'total_predictions': Prediccion.objects.filter(usuario=user).count(),
            'correct_predictions': Prediccion.objects.filter(usuario=user, correcta=True).count(),
            'total_points': user.puntos_totales,
            'nivel_experto': user.nivel_experto
        }
        
        if stats['total_predictions'] > 0:
            stats['success_rate'] = round((stats['correct_predictions'] / stats['total_predictions']) * 100, 2)
        else:
            stats['success_rate'] = 0
        
        return Response({
            'predictions': serializer.data,
            'stats': stats,
            'pagination': {
                'total': total_predictions,
                'page': page,
                'page_size': page_size,
                'total_pages': (total_predictions + page_size - 1) // page_size
            },
            'filters': {
                'status': status_filter
            }
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error cargando predicciones: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def prediction_detail(request, prediction_id):
    """
    Obtener detalles de una predicción específica
    GET /api/predictions/{id}/
    """
    try:
        user = request.user
        
        # Buscar predicción
        try:
            prediccion = Prediccion.objects.select_related(
                'partido__equipo_local',
                'partido__equipo_visitante',
                'usuario'
            ).get(id=prediction_id)
        except Prediccion.DoesNotExist:
            return Response(
                {'error': 'Predicción no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Verificar que la predicción pertenece al usuario
        if prediccion.usuario != user:
            return Response(
                {'error': 'No tienes permisos para ver esta predicción'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Serializar
        serializer = PrediccionSerializer(prediccion)
        prediction_data = serializer.data
        
        # Añadir comparación con la comunidad
        partido = prediccion.partido
        predicciones_partido = Prediccion.objects.filter(partido=partido)
        total_predicciones = predicciones_partido.count()
        
        if total_predicciones > 0:
            same_prediction_count = predicciones_partido.filter(
                prediccion=prediccion.prediccion
            ).count()
            
            prediction_data['community_comparison'] = {
                'total_predictions': total_predicciones,
                'same_prediction_count': same_prediction_count,
                'same_prediction_percentage': round((same_prediction_count / total_predicciones) * 100, 1)
            }
        
        return Response(prediction_data)
        
    except Exception as e:
        return Response(
            {'error': f'Error cargando predicción: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_prediction(request, prediction_id):
    """
    Actualizar una predicción (solo si el partido no ha empezado)
    PUT /api/predictions/{id}/
    Body: {prediccion}
    """
    try:
        user = request.user
        
        # Buscar predicción
        try:
            prediccion = Prediccion.objects.select_related('partido').get(id=prediction_id)
        except Prediccion.DoesNotExist:
            return Response(
                {'error': 'Predicción no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Verificar que la predicción pertenece al usuario
        if prediccion.usuario != user:
            return Response(
                {'error': 'No tienes permisos para modificar esta predicción'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Verificar que el partido no haya empezado
        if prediccion.partido.fecha_hora <= timezone.now():
            return Response(
                {'error': 'No se puede modificar una predicción de un partido que ya empezó'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar que el partido esté pendiente
        if prediccion.partido.estado != 'PENDIENTE':
            return Response(
                {'error': 'No se puede modificar una predicción de un partido que no está pendiente'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validar y actualizar predicción
        serializer = PrediccionCreateSerializer(prediccion, data=request.data, partial=True)
        if not serializer.is_valid():
             return Response(
                {'error': 'Datos inválidos', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Guardar cambios
        prediccion_anterior = prediccion.prediccion
        serializer.save()
        
        # Recargar para tener los datos actualizados
        prediccion.refresh_from_db()
        nueva_prediccion = prediccion.prediccion
        
        # Log en MongoDB
        analytics_manager.registrar_actividad_usuario(
            user_id=user.id,
            action='update_prediction',
            metadata={
                'prediction_id': prediction_id,
                'old_prediction': prediccion_anterior,
                'new_prediction': nueva_prediccion
            }
        )
        
        # Serializar respuesta
        serializer = PrediccionSerializer(prediccion)
        
        return Response({
            'message': 'Predicción actualizada exitosamente',
            'prediction': serializer.data
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error actualizando predicción: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_prediction(request, prediction_id):
    """
    Eliminar una predicción (solo si el partido no ha empezado)
    DELETE /api/predictions/{id}/
    """
    try:
        user = request.user
        
        # Buscar predicción
        try:
            prediccion = Prediccion.objects.select_related('partido').get(id=prediction_id)
        except Prediccion.DoesNotExist:
            return Response(
                {'error': 'Predicción no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Verificar que la predicción pertenece al usuario
        if prediccion.usuario != user:
            return Response(
                {'error': 'No tienes permisos para eliminar esta predicción'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Verificar que el partido no haya empezado
        if prediccion.partido.fecha_hora <= timezone.now():
            return Response(
                {'error': 'No se puede eliminar una predicción de un partido que ya empezó'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Eliminar predicción
        prediccion.delete()
        
        # Devolver una predicción al rate limiter
        rate_limiter = RateLimiter(user.id)
        rate_limiter.refund_prediction()
        
        # Log en MongoDB
        analytics_manager.registrar_actividad_usuario(
            user_id=user.id,
            action='delete_prediction',
            metadata={'prediction_id': prediction_id}
        )
        
        return Response({
            'message': 'Predicción eliminada exitosamente',
            'remaining_predictions_today': rate_limiter.get_remaining_predictions()
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error eliminando predicción: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def prediction_stats(request):
    """
    Obtener estadísticas de predicciones del usuario
    GET /api/predictions/stats/
    """
    try:
        user = request.user
        
        # Estadísticas básicas
        total_predictions = Prediccion.objects.filter(usuario=user).count()
        correct_predictions = Prediccion.objects.filter(usuario=user, correcta=True).count()
        
        stats = {
            'total_predictions': total_predictions,
            'correct_predictions': correct_predictions,
            'incorrect_predictions': Prediccion.objects.filter(usuario=user, correcta=False).count(),
            'pending_predictions': Prediccion.objects.filter(usuario=user, correcta=None).count(),
            'total_points': user.puntos_totales,
            'nivel_experto': user.nivel_experto,
            'success_rate': round((correct_predictions / total_predictions * 100), 2) if total_predictions > 0 else 0
        }
        
        # Predicciones por deporte
        predicciones_por_deporte = Prediccion.objects.filter(
            usuario=user
        ).values(
            'partido__equipo_local__deporte__nombre'
        ).annotate(
            total=Count('id'),
            correctas=Count('id', filter=Q(correcta=True))
        )
        
        sport_stats = []
        for item in predicciones_por_deporte:
            deporte_nombre = item['partido__equipo_local__deporte__nombre']
            total = item['total']
            correctas = item['correctas']
            sport_stats.append({
                'sport': deporte_nombre,
                'total_predictions': total,
                'correct_predictions': correctas,
                'success_rate': round((correctas / total * 100), 2) if total > 0 else 0
            })
        
        stats['sport_analysis'] = sport_stats
        
        # Predicciones hoy
        rate_limiter = RateLimiter(user.id)
        stats['today_predictions'] = rate_limiter.get_today_predictions()
        stats['remaining_predictions_today'] = rate_limiter.get_remaining_predictions()
        
        return Response(stats)
        
    except Exception as e:
        return Response(
            {'error': f'Error cargando estadísticas: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def match_predictions(request, match_id):
    """
    Obtener predicción del usuario para un partido específico
    GET /api/predictions/match/{match_id}/
    """
    try:
        user = request.user
        
        # Buscar partido
        try:
            partido = Partido.objects.get(id=match_id)
        except Partido.DoesNotExist:
            return Response(
                {'error': 'Partido no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Buscar predicción del usuario
        user_prediction = Prediccion.objects.filter(
            usuario=user,
            partido=partido
        ).first()
        
        # Verificar si puede predecir
        rate_limiter = RateLimiter(user.id)
        can_predict = (
            rate_limiter.can_make_prediction() and
            partido.estado == 'PENDIENTE' and
            partido.fecha_hora > timezone.now() and
            user_prediction is None
        )
        
        response_data = {
            'match_id': match_id,
            'can_predict': can_predict,
            'user_prediction': None
        }
        
        if user_prediction:
            serializer = PrediccionSerializer(user_prediction)
            response_data['user_prediction'] = serializer.data
        
        if not can_predict and user_prediction is None:
            if not rate_limiter.can_make_prediction():
                response_data['reason'] = 'Límite de predicciones diarias alcanzado'
            elif partido.estado != 'PENDIENTE':
                response_data['reason'] = 'El partido no está pendiente'
            elif partido.fecha_hora <= timezone.now():
                response_data['reason'] = 'El partido ya empezó'
        
        return Response(response_data)
        
    except Exception as e:
        return Response(
            {'error': f'Error cargando predicciones del partido: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
