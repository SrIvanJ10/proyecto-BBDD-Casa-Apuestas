import api from './api';

// Obtener lista de conversaciones (último mensaje + no leídos)
export const getConversations = async () => {
    const response = await api.get('/chat/conversations/');
    return response.data;
};

// Obtener mensajes con un usuario específico
export const getMessagesWithUser = async (userId, { limit = 50, offset = 0 } = {}) => {
    const response = await api.get(`/chat/${userId}/messages/`, {
        params: { limit, offset },
    });
    return response.data;
};

// Enviar mensaje a un usuario
export const sendMessageToUser = async (userId, content) => {
    const response = await api.post(`/chat/${userId}/messages/`, { content });
    return response.data;
};
