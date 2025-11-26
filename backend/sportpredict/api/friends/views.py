"""
API de Amigos - Integración con Neo4j
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from sportpredict.models import Usuario
from sportpredict.db.neo4j_utils import Neo4jClient
from sportpredict.serializers import UsuarioSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_friends(request):
    """
    Obtener lista de amigos del usuario autenticado
    GET /api/friends/
    """
    try:
        user = request.user
        client = Neo4jClient()
        
        # Obtener amigos desde Neo4j
        friends_data = client.get_friends(user.id)
        
        if not friends_data:
            return Response({
                'friends': [],
                'count': 0
            })
        
        # Obtener IDs de amigos
        friend_ids = [f['user_id'] for f in friends_data]
        
        # Recuperar objetos Usuario de PostgreSQL
        friends = Usuario.objects.filter(id__in=friend_ids)
        
        # Serializar
        serializer = UsuarioSerializer(friends, many=True)
        
        return Response({
            'friends': serializer.data,
            'count': len(serializer.data)
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error obteniendo amigos: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_pending_requests(request):
    """
    Obtener solicitudes de amistad pendientes recibidas
    GET /api/friends/pending/
    """
    try:
        user = request.user
        client = Neo4jClient()
        
        # Obtener solicitudes pendientes desde Neo4j
        pending_data = client.get_pending_requests(user.id)
        
        if not pending_data:
            return Response({
                'pending_requests': [],
                'count': 0
            })
        
        # Obtener IDs de usuarios que enviaron solicitudes
        sender_ids = [p['user_id'] for p in pending_data]
        
        # Recuperar objetos Usuario de PostgreSQL
        senders = Usuario.objects.filter(id__in=sender_ids)
        
        # Serializar
        serializer = UsuarioSerializer(senders, many=True)
        
        return Response({
            'pending_requests': serializer.data,
            'count': len(serializer.data)
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error obteniendo solicitudes pendientes: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sent_requests(request):
    """
    Obtener solicitudes de amistad enviadas (pendientes)
    GET /api/friends/sent/
    """
    try:
        user = request.user
        client = Neo4jClient()
        
        # Obtener solicitudes enviadas desde Neo4j
        sent_data = client.get_sent_requests(user.id)
        
        if not sent_data:
            return Response({
                'sent_requests': [],
                'count': 0
            })
        
        # Obtener IDs de usuarios a quienes se enviaron solicitudes
        recipient_ids = [s['user_id'] for s in sent_data]
        
        # Recuperar objetos Usuario de PostgreSQL
        recipients = Usuario.objects.filter(id__in=recipient_ids)
        
        # Serializar
        serializer = UsuarioSerializer(recipients, many=True)
        
        return Response({
            'sent_requests': serializer.data,
            'count': len(serializer.data)
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error obteniendo solicitudes enviadas: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request):
    """
    Enviar solicitud de amistad a otro usuario
    POST /api/friends/request/
    Body: {"to_user": <user_id>}
    """
    try:
        user = request.user
        to_user_id = request.data.get('to_user')
        
        if not to_user_id:
            return Response(
                {'error': 'El campo "to_user" es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar que el usuario destino existe
        try:
            to_user = Usuario.objects.get(id=to_user_id)
        except Usuario.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # No puedes enviarte una solicitud a ti mismo
        if user.id == to_user_id:
            return Response(
                {'error': 'No puedes enviarte una solicitud de amistad a ti mismo'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Enviar solicitud en Neo4j
        client = Neo4jClient()
        success = client.send_friend_request(user.id, to_user_id)
        
        if success:
            return Response({
                'message': f'Solicitud de amistad enviada a {to_user.username}',
                'to_user': UsuarioSerializer(to_user).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'error': 'Ya existe una relación de amistad o solicitud pendiente'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
    except Exception as e:
        return Response(
            {'error': f'Error enviando solicitud de amistad: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, user_id):
    """
    Aceptar solicitud de amistad
    POST /api/friends/accept/<user_id>/
    """
    try:
        user = request.user
        
        # Verificar que el usuario que envió la solicitud existe
        try:
            from_user = Usuario.objects.get(id=user_id)
        except Usuario.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Aceptar solicitud en Neo4j
        client = Neo4jClient()
        success = client.accept_friend_request(user_id, user.id)
        
        if success:
            return Response({
                'message': f'Ahora eres amigo de {from_user.username}',
                'friend': UsuarioSerializer(from_user).data
            })
        else:
            return Response(
                {'error': 'No se encontró una solicitud de amistad pendiente'},
                status=status.HTTP_404_NOT_FOUND
            )
        
    except Exception as e:
        return Response(
            {'error': f'Error aceptando solicitud de amistad: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_friend_request(request, user_id):
    """
    Rechazar solicitud de amistad
    POST /api/friends/reject/<user_id>/
    """
    try:
        user = request.user
        
        # Verificar que el usuario que envió la solicitud existe
        try:
            from_user = Usuario.objects.get(id=user_id)
        except Usuario.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Rechazar solicitud en Neo4j
        client = Neo4jClient()
        success = client.reject_friend_request(user_id, user.id)
        
        if success:
            return Response({
                'message': f'Solicitud de amistad de {from_user.username} rechazada'
            })
        else:
            return Response(
                {'error': 'No se encontró una solicitud de amistad pendiente'},
                status=status.HTTP_404_NOT_FOUND
            )
        
    except Exception as e:
        return Response(
            {'error': f'Error rechazando solicitud de amistad: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_friend(request, user_id):
    """
    Eliminar un amigo
    DELETE /api/friends/<user_id>/
    """
    try:
        user = request.user
        
        # Verificar que el usuario existe
        try:
            friend = Usuario.objects.get(id=user_id)
        except Usuario.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Eliminar amistad en Neo4j
        client = Neo4jClient()
        success = client.remove_friend(user.id, user_id)
        
        if success:
            return Response({
                'message': f'Has eliminado a {friend.username} de tus amigos'
            })
        else:
            return Response(
                {'error': 'No se encontró una relación de amistad'},
                status=status.HTTP_404_NOT_FOUND
            )
        
    except Exception as e:
        return Response(
            {'error': f'Error eliminando amigo: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    """
    Buscar usuarios por nombre de usuario
    GET /api/friends/search/?q=<query>
    """
    try:
        query = request.GET.get('q', '').strip()
        
        if not query:
            return Response(
                {'error': 'El parámetro "q" es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Buscar usuarios en PostgreSQL (excluir al usuario actual)
        users = Usuario.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        ).exclude(
            id=request.user.id
        ).filter(
            is_active=True
        )[:20]  # Limitar a 20 resultados
        
        # Serializar
        serializer = UsuarioSerializer(users, many=True)
        
        return Response({
            'users': serializer.data,
            'count': len(serializer.data),
            'query': query
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error buscando usuarios: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_friendship_status(request, user_id):
    """
    Obtener el estado de amistad con un usuario específico
    GET /api/friends/status/<user_id>/
    Returns: {"status": "friends" | "pending_sent" | "pending_received" | "none"}
    """
    try:
        user = request.user
        
        # Verificar que el usuario existe
        try:
            other_user = Usuario.objects.get(id=user_id)
        except Usuario.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Obtener estado desde Neo4j
        client = Neo4jClient()
        friendship_status = client.get_friend_request_status(user.id, user_id)
        
        return Response({
            'user': UsuarioSerializer(other_user).data,
            'status': friendship_status
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error obteniendo estado de amistad: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
