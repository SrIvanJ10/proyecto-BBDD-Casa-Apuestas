import React from 'react';
import PropTypes from 'prop-types';

const FriendCard = ({ user, onAccept, onReject, onRemove, onChat, type = 'friend' }) => {
    return (
        <div className="friend-card">
            <div className="friend-info">
                <div className="friend-avatar">
                    {user.avatar ? (
                        <img src={user.avatar} alt={user.username} />
                    ) : (
                        <div className="avatar-placeholder">
                            {user.username.charAt(0).toUpperCase()}
                        </div>
                    )}
                </div>
                <div className="friend-details">
                    <h3>{user.username}</h3>
                    <p className="friend-stats">
                        <span>⭐ {user.puntos_totales || 0} puntos</span>
                        <span>📊 Nivel {user.nivel_experto || 1}</span>
                    </p>
                </div>
            </div>

            <div className="friend-actions">
                {type === 'pending' && (
                    <>
                        <button
                            className="btn-accept"
                            onClick={() => onAccept(user.id)}
                            title="Aceptar solicitud"
                        >
                            ✓ Aceptar
                        </button>
                        <button
                            className="btn-reject"
                            onClick={() => onReject(user.id)}
                            title="Rechazar solicitud"
                        >
                            ✗ Rechazar
                        </button>
                    </>
                )}

                {type === 'friend' && (
                    <>
                        {onChat && (
                            <button
                                className="btn-accept"
                                onClick={() => onChat(user.id)}
                                title="Abrir chat"
                            >
                                💬 Chat
                            </button>
                        )}
                        <button
                            className="btn-remove"
                            onClick={() => onRemove(user.id)}
                            title="Eliminar amigo"
                        >
                            🗑️ Eliminar
                        </button>
                    </>
                )}
            </div>
        </div>
    );
};

FriendCard.propTypes = {
    user: PropTypes.shape({
        id: PropTypes.number.isRequired,
        username: PropTypes.string.isRequired,
        avatar: PropTypes.string,
        puntos_totales: PropTypes.number,
        nivel_experto: PropTypes.number,
    }).isRequired,
    onAccept: PropTypes.func,
    onReject: PropTypes.func,
    onRemove: PropTypes.func,
    onChat: PropTypes.func,
    type: PropTypes.oneOf(['friend', 'pending']),
};

export default FriendCard;
