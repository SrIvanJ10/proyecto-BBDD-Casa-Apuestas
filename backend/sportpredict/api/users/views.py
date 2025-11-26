"""
API de Usuarios - Perfil, ranking, historial
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Count, Sum, Q

from sportpredict.models import Usuario, Prediccion
from sportpredict.serializers import UsuarioSerializer
from sportpredict.db.mongodb.analytics import AnalyticsManager
from sportpredict.db.redis.sessions import SessionManager


# Inicializar managers
analytics_manager = AnalyticsManager()
session_manager = SessionManager()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Obtener perfil del usuario autenticado
    GET /api/users/profile/
    """
    try:
        user = request.user
        
        # Serializar usuario
        serializer = UsuarioSerializer(user)
        profile_data = serializer.data
        
        # Añadir estadísticas
        total_predictions = Prediccion.objects.filter(usuario=user).count()
        correct_predictions = Prediccion.objects.filter(usuario=user, correcta=True).count()
        
        profile_data['stats'] = {
            'total_predictions': total_predictions,
            'correct_predictions': correct_predictions,
            'success_rate': round((correct_predictions / total_predictions * 100), 2) if total_predictions > 0 else 0,
            'total_points': user.puntos_totales,
            'nivel_experto': user.nivel_experto
        }
        
        # Obtener datos de sesión de Redis
        session_data = session_manager.get_user_session(str(user.id))
        if session_data:
            profile_data['session'] = {
                'predictions_today': int(session_data.get('predicciones_hoy', 0)),
                'remaining_predictions': 10 - int(session_data.get('predicciones_hoy', 0))
            }
        
        return Response(profile_data)
        
    except Exception as e:
        return Response(
            {'error': f'Error cargando perfil: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Actualizar perfil del usuario
    PUT /api/users/profile/update/
    Body: {first_name, last_name, avatar}
    """
    try:
        user = request.user
        
        # Actualizar campos permitidos
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']
        if 'last_name' in request.data:
            user.last_name = request.data['last_name']
        if 'avatar' in request.data:
            user.avatar = request.data['avatar']
        
        user.save()
        
        # Actualizar sesión en Redis
        session_manager.refresh_session(user)
        
        # Log en MongoDB
        analytics_manager.registrar_actividad_usuario(
            user_id=user.id,
            action='profile_updated',
            metadata={}
        )
        
        # Serializar respuesta
        serializer = UsuarioSerializer(user)
        
        return Response({
            'message': 'Perfil actualizado exitosamente',
            'user': serializer.data
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error actualizando perfil: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 4e74b6e (v1.0)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_username(request):
    """
    Actualizar nombre de usuario
    PUT /api/users/update-username/
    Body: {new_username}
    """
    try:
        user = request.user
        new_username = request.data.get('new_username', '').strip()
        
        if not new_username:
            return Response({
                'error': 'El nombre de usuario no puede estar vacío'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar que el username no esté en uso
        if Usuario.objects.filter(username=new_username).exclude(id=user.id).exists():
            return Response({
                'error': 'Este nombre de usuario ya está en uso'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Actualizar username
        user.username = new_username
        user.save()
        
        # Log en MongoDB
        analytics_manager.registrar_actividad_usuario(
            user_id=user.id,
            action='username_updated',
            metadata={'new_username': new_username}
        )
        
        serializer = UsuarioSerializer(user)
        
        return Response({
            'message': 'Nombre de usuario actualizado exitosamente',
            'user': serializer.data
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error actualizando nombre de usuario: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_password(request):
    """
    Actualizar contraseña
    PUT /api/users/update-password/
    Body: {current_password, new_password}
    """
    try:
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        
        if not current_password or not new_password:
            return Response({
                'error': 'Se requiere la contraseña actual y la nueva contraseña'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar contraseña actual
        if not user.check_password(current_password):
            return Response({
                'error': 'La contraseña actual es incorrecta'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar nueva contraseña (mínimo 6 caracteres)
        if len(new_password) < 6:
            return Response({
                'error': 'La nueva contraseña debe tener al menos 6 caracteres'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Actualizar contraseña
        user.set_password(new_password)
        user.save()
        
        # Log en MongoDB
        analytics_manager.registrar_actividad_usuario(
            user_id=user.id,
            action='password_updated',
            metadata={}
        )
        
        return Response({
            'message': 'Contraseña actualizada exitosamente'
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error actualizando contraseña: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


<<<<<<< HEAD
=======
>>>>>>> d381094 (v0.14)
=======
>>>>>>> 4e74b6e (v1.0)
@api_view(['GET'])
@permission_classes([AllowAny])
def leaderboard(request):
    """
    Obtener ranking de usuarios
    GET /api/users/leaderboard/
    Query params: limit (default: 50)
    """
    try:
        limit = int(request.GET.get('limit', 50))
        
        # Obtener top usuarios por puntos
        top_users = Usuario.objects.filter(
            is_active=True
        ).order_by('-puntos_totales', '-nivel_experto')[:limit]
        
        leaderboard_data = []
        for idx, user in enumerate(top_users, start=1):
            total_predictions = Prediccion.objects.filter(usuario=user).count()
            correct_predictions = Prediccion.objects.filter(usuario=user, correcta=True).count()
            
            leaderboard_data.append({
                'rank': idx,
                'user_id': user.id,
                'username': user.username,
                'avatar': user.avatar,
                'puntos_totales': user.puntos_totales,
                'nivel_experto': user.nivel_experto,
                'total_predictions': total_predictions,
                'correct_predictions': correct_predictions,
                'success_rate': round((correct_predictions / total_predictions * 100), 2) if total_predictions > 0 else 0
            })
        
        # Si el usuario está autenticado, añadir su posición
        user_rank = None
        if request.user.is_authenticated:
            all_users = Usuario.objects.filter(
                is_active=True
            ).order_by('-puntos_totales', '-nivel_experto')
            
            for idx, user in enumerate(all_users, start=1):
                if user.id == request.user.id:
                    user_rank = idx
                    break
        
        return Response({
            'leaderboard': leaderboard_data,
            'total_users': Usuario.objects.filter(is_active=True).count(),
            'user_rank': user_rank
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error cargando leaderboard: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_activity(request):
    """
    Obtener historial de actividad del usuario desde MongoDB
    GET /api/users/activity/
    Query params: limit (default: 50)
    """
    try:
        user = request.user
        limit = int(request.GET.get('limit', 50))
        
        # Obtener actividad desde MongoDB
        activity = analytics_manager.obtener_actividad_usuario(
            user_id=str(user.id),
            limite=limit
        )
        
        return Response({
            'activity': activity,
            'count': len(activity)
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error cargando actividad: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> db693ad (v0.9)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upgrade_subscription(request):
    """
    Actualizar suscripción a Premium
    POST /api/users/upgrade-subscription/
    Costo: 500 puntos
    """
    try:
        user = request.user
        PREMIUM_COST = 500
        
        # Verificar que el usuario no sea ya Premium
        if user.tipo_suscripcion == 'PREMIUM':
            return Response({
                'error': 'Ya tienes suscripción Premium',
                'subscription_type': 'PREMIUM'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar que tenga suficientes puntos
        if user.puntos_totales < PREMIUM_COST:
            return Response({
                'error': 'Puntos insuficientes',
                'message': f'Necesitas {PREMIUM_COST} puntos para actualizar a Premium',
                'current_points': user.puntos_totales,
                'required_points': PREMIUM_COST,
                'missing_points': PREMIUM_COST - user.puntos_totales
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Descontar puntos y actualizar suscripción
        user.puntos_totales -= PREMIUM_COST
        user.tipo_suscripcion = 'PREMIUM'
        user.save()
        
        # Actualizar sesión en Redis
        session_manager.refresh_session(user)
        
        # Log en MongoDB
        analytics_manager.registrar_actividad_usuario(
            user_id=user.id,
            action='subscription_upgraded',
            metadata={
                'cost': PREMIUM_COST,
                'remaining_points': user.puntos_totales
            }
        )
        
        # Serializar respuesta
        serializer = UsuarioSerializer(user)
        
        return Response({
            'message': '¡Suscripción actualizada a Premium!',
            'subscription_type': 'PREMIUM',
            'points_spent': PREMIUM_COST,
            'remaining_points': user.puntos_totales,
            'user': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Error actualizando suscripción: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
<<<<<<< HEAD
=======
>>>>>>> d381094 (v0.14)
=======
>>>>>>> db693ad (v0.9)
