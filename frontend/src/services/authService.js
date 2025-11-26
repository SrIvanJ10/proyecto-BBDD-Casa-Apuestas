import api from './api';

export const login = async (username, password) => {
    const response = await api.post('/auth/login/', { email_or_username: username, password });
    if (response.data.token) {
        localStorage.setItem('token', response.data.token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
};

export const register = async (userData) => {
    const response = await api.post('/auth/register/', userData);
    return response.data;
};

export const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh');
};

export const verifyOtp = async (email, otp) => {
    const response = await api.post('/auth/verify-otp/', { email, otp });
    if (response.data.token) {
        localStorage.setItem('token', response.data.token);
        localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
};
