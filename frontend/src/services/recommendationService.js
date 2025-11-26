import api from './api';

export const getRecommendedMatches = async () => {
    const response = await api.get('/recommendations/matches/');
    return response.data;
};

export const getSimilarUsers = async () => {
    const response = await api.get('/recommendations/users/');
    return response.data;
};

export const getTrendingMatches = async () => {
    const response = await api.get('/recommendations/trending/');
    return response.data;
};
