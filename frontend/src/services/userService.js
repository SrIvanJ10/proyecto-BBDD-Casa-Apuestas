import api from './api';

export const getProfile = async () => {
    const response = await api.get('/users/profile/');
    return response.data;
};

export const updateProfile = async (data) => {
    const response = await api.put('/users/profile/update/', data);
    return response.data;
};

export const getLeaderboard = async () => {
    const response = await api.get('/users/leaderboard/');
    return response.data;
};

export const getUserActivity = async () => {
    const response = await api.get('/users/activity/');
    return response.data;
};
