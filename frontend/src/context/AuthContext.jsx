import React, { createContext, useState, useEffect, useContext } from 'react';
import { login as apiLogin, logout as apiLogout } from '../services/authService';
import api from '../services/api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkLoggedIn = async () => {
            const token = localStorage.getItem('token');
            if (token) {
                try {
                    const response = await api.get('/users/profile/');
                    setUser(response.data);
                } catch (error) {
                    if (error.response?.status === 401) {
                        localStorage.removeItem('token');
                    }
                    setUser(null);
                }
            }
            setLoading(false);
        };
        checkLoggedIn();
    }, []);

    const login = async (username, password) => {
        try {
            const data = await apiLogin(username, password);
            setUser(data.user);
            return data;
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    };

    const logout = () => {
        apiLogout();
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, setUser, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
export default AuthContext;
