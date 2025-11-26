import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { getFriendshipStatus, sendFriendRequest } from '../services/friendService';

const UserSearchCard = ({ user, onRequestSent }) => {
    const [status, setStatus] = useState('none');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        loadFriendshipStatus();
    }, [user.id]);

    const loadFriendshipStatus = async () => {
        try {
            const data = await getFriendshipStatus(user.id);
            setStatus(data.status);
        } catch (err) {
            console.error('Error loading friendship status:', err);
        }
    };

    const handleSendRequest = async () => {
        setLoading(true);
        setError(null);

        try {
            await sendFriendRequest(user.id);
            setStatus('pending_sent');
            if (onRequestSent) {
                onRequestSent(user);
            }
        } catch (err) {
            setError(err.response?.data?.error || 'Error enviando solicitud');
        } finally {
            setLoading(false);
        }
    };

    const getStatusButton = () => {
        switch (status) {
            case 'friends':
                return (
                    <button className="btn-status btn-friends" disabled>
                        ✓ Amigos
                    </button>
                );
            case 'pending_sent':
                return (
                    <button className="btn-status btn-pending" disabled>
                        ⏳ Solicitud enviada
                    </button>
                );
            case 'pending_received':
                return (
                    <button className="btn-status btn-pending" disabled>
                        📬 Solicitud recibida
                    </button>
                );
            case 'none':
            default:
                return (
                    <button
                        className="btn-add-friend"
                        onClick={handleSendRequest}
                        disabled={loading}
                    >
                        {loading ? '⏳ Enviando...' : '➕ Añadir amigo'}
                    </button>
                );
        }
    };

    return (
        <div className="user-search-card">
            <div className="user-info">
                <div className="user-avatar">
                    {user.avatar ? (
                        <img src={user.avatar} alt={user.username} />
                    ) : (
                        <div className="avatar-placeholder">
                            {user.username.charAt(0).toUpperCase()}
                        </div>
                    )}
                </div>
                <div className="user-details">
                    <h3>{user.username}</h3>
                    <p className="user-stats">
                        <span>⭐ {user.puntos_totales || 0} puntos</span>
                        <span>📊 Nivel {user.nivel_experto || 1}</span>
                    </p>
                </div>
            </div>

            <div className="user-actions">
                {getStatusButton()}
            </div>

            {error && <p className="error-message">{error}</p>}
        </div>
    );
};

UserSearchCard.propTypes = {
    user: PropTypes.shape({
        id: PropTypes.number.isRequired,
        username: PropTypes.string.isRequired,
        avatar: PropTypes.string,
        puntos_totales: PropTypes.number,
        nivel_experto: PropTypes.number,
    }).isRequired,
    onRequestSent: PropTypes.func,
};

export default UserSearchCard;
