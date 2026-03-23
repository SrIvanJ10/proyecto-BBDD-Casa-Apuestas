"""
API de Chat entre usuarios (solo amigos).
"""
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from sportpredict.models import Usuario, ChatMessage
from sportpredict.serializers import ChatMessageSerializer, UsuarioSerializer
from sportpredict.db.neo4j_utils import Neo4jClient


def _ensure_friendship(current_user, other_user_id):
    """Helper para validar que ambos usuarios son amigos."""
    client = Neo4jClient()
    return client.are_friends(current_user.id, other_user_id)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_conversations(request):
    """
    Obtener conversaciones del usuario con último mensaje y no leídos.
    GET /api/chat/conversations/
    """
    user = request.user
    user_messages = ChatMessage.objects.filter(Q(sender=user) | Q(receiver=user))

    participant_ids = set(user_messages.values_list('sender', flat=True)) | set(
        user_messages.values_list('receiver', flat=True)
    )
    participant_ids.discard(user.id)

    participants = Usuario.objects.filter(id__in=participant_ids)

    conversations = []
    for participant in participants:
        thread = user_messages.filter(Q(sender=participant) | Q(receiver=participant)).order_by('-created_at')
        last_message = thread.first()
        unread_count = thread.filter(sender=participant, receiver=user, is_read=False).count()

        conversations.append({
            'user': UsuarioSerializer(participant).data,
            'last_message': ChatMessageSerializer(last_message).data if last_message else None,
            'unread_count': unread_count,
        })

    conversations.sort(
        key=lambda c: c['last_message']['created_at'] if c['last_message'] else '',
        reverse=True,
    )

    return Response({
        'conversations': conversations,
        'count': len(conversations),
    })


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def chat_messages(request, user_id):
    """
    Listar o enviar mensajes a un amigo específico.
    GET/POST /api/chat/<user_id>/messages/
    """
    user = request.user

    if user.id == user_id:
        return Response(
            {'error': 'No puedes chatear contigo mismo'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        friend = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if not _ensure_friendship(user, friend.id):
        return Response(
            {'error': 'Solo puedes chatear con tus amigos'},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == 'POST':
        content = (request.data.get('content') or '').strip()
        if not content:
            return Response({'error': 'El mensaje no puede estar vacío'}, status=status.HTTP_400_BAD_REQUEST)
        if len(content) > 1000:
            return Response({'error': 'El mensaje es demasiado largo (máximo 1000 caracteres)'}, status=status.HTTP_400_BAD_REQUEST)

        message = ChatMessage.objects.create(sender=user, receiver=friend, content=content)
        serializer = ChatMessageSerializer(message)
        return Response({'message': serializer.data}, status=status.HTTP_201_CREATED)

    # GET: obtener mensajes
    limit = min(int(request.GET.get('limit', 50)), 100)
    offset = max(int(request.GET.get('offset', 0)), 0)

    qs = ChatMessage.objects.filter(
        Q(sender=user, receiver=friend) | Q(sender=friend, receiver=user)
    ).order_by('-created_at')

    total = qs.count()
    selected = list(qs[offset:offset + limit])
    # Devolver en orden cronológico ascendente
    selected.reverse()

    # Marcar mensajes como leídos
    qs.filter(sender=friend, receiver=user, is_read=False).update(is_read=True)

    serializer = ChatMessageSerializer(selected, many=True)
    return Response({
        'messages': serializer.data,
        'pagination': {
            'total': total,
            'limit': limit,
            'offset': offset,
        },
        'with_user': UsuarioSerializer(friend).data,
    })