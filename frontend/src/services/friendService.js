import api from './api';

/**
 * Servicio para gestionar amigos
 */

// Obtener lista de amigos
export const getFriends = async () => {
    const response = await api.get('/friends/');
    return response.data;
};

// Obtener solicitudes de amistad pendientes (recibidas)
export const getPendingRequests = async () => {
    const response = await api.get('/friends/pending/');
    return response.data;
};

// Obtener solicitudes de amistad enviadas
export const getSentRequests = async () => {
    const response = await api.get('/friends/sent/');
    return response.data;
};

// Enviar solicitud de amistad
export const sendFriendRequest = async (userId) => {
    const response = await api.post('/friends/request/', { to_user: userId });
    return response.data;
};

// Aceptar solicitud de amistad
export const acceptFriendRequest = async (userId) => {
    const response = await api.post(`/friends/accept/${userId}/`);
    return response.data;
};

// Rechazar solicitud de amistad
export const rejectFriendRequest = async (userId) => {
    const response = await api.post(`/friends/reject/${userId}/`);
    return response.data;
};

// Eliminar amigo
export const removeFriend = async (userId) => {
    const response = await api.delete(`/friends/${userId}/`);
    return response.data;
};

// Buscar usuarios por nombre
export const searchUsers = async (query) => {
    const response = await api.get(`/friends/search/?q=${encodeURIComponent(query)}`);
    return response.data;
};

// Obtener estado de amistad con un usuario
export const getFriendshipStatus = async (userId) => {
    const response = await api.get(`/friends/status/${userId}/`);
    return response.data;
};
