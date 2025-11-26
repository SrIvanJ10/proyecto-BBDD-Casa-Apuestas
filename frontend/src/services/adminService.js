import api from './api';

// Users
export const getAdminUsers = async () => {
    const response = await api.get('/admin/users/');
    return response.data;
};

export const deleteAdminUser = async (userId) => {
    const response = await api.delete(`/admin/users/${userId}/`);
    return response.data;
};

// Sports
export const getAdminSports = async () => {
    const response = await api.get('/admin/sports/');
    return response.data;
};

export const createAdminSport = async (data) => {
    const response = await api.post('/admin/sports/create/', data);
    return response.data;
};

export const deleteAdminSport = async (sportId) => {
    const response = await api.delete(`/admin/sports/${sportId}/`);
    return response.data;
};

// Teams
export const getAdminTeams = async () => {
    const response = await api.get('/admin/teams/');
    return response.data;
};

export const createAdminTeam = async (data) => {
    const response = await api.post('/admin/teams/create/', data);
    return response.data;
};

export const deleteAdminTeam = async (teamId) => {
    const response = await api.delete(`/admin/teams/${teamId}/`);
    return response.data;
};

// Matches
export const getAdminMatches = async () => {
    const response = await api.get('/admin/matches/');
    return response.data;
};

export const createAdminMatch = async (data) => {
    const response = await api.post('/admin/matches/create/', data);
    return response.data;
};

export const updateAdminMatch = async (matchId, data) => {
    const response = await api.put(`/admin/matches/${matchId}/`, data);
    return response.data;
};

export const deleteAdminMatch = async (matchId) => {
    const response = await api.delete(`/admin/matches/${matchId}/delete/`);
    return response.data;
};

// Predictions
export const getAdminPredictions = async () => {
    const response = await api.get('/admin/predictions/');
    return response.data;
};

export const deleteAdminPrediction = async (predictionId) => {
    const response = await api.delete(`/admin/predictions/${predictionId}/`);
    return response.data;
};

// Profile
export const updateUsername = async (newUsername) => {
    const response = await api.put('/users/update-username/', { new_username: newUsername });
    return response.data;
};

export const updatePassword = async (currentPassword, newPassword) => {
    const response = await api.put('/users/update-password/', {
        current_password: currentPassword,
        new_password: newPassword
    });
    return response.data;
};
