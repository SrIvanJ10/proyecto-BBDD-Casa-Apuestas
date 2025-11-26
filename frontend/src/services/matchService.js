import api from './api';

export const getMatches = async (filters = {}) => {
    const params = new URLSearchParams();
    if (filters.sport) params.append('sport', filters.sport);
    if (filters.status) params.append('status', filters.status);

    const response = await api.get(`/matches/?${params.toString()}`);
    return response.data.matches || [];
};

export const getMatchDetail = async (id) => {
    const response = await api.get(`/matches/${id}/`);
    return response.data;
};

export const getUpcomingMatches = async () => {
    const response = await api.get('/matches/upcoming/');
    return response.data;
};

export const getLiveMatches = async () => {
    const response = await api.get('/matches/live/');
    return response.data;
};
