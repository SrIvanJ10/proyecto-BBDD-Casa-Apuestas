import api from './api';

export const upgradeSubscription = async () => {
    const response = await api.post('/users/upgrade-subscription/');
    return response.data;
};
