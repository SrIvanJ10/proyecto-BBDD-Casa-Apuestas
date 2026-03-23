import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import FriendCard from '../components/FriendCard';
import UserSearchCard from '../components/UserSearchCard';
import {
    getFriends,
    getPendingRequests,
    acceptFriendRequest,
    rejectFriendRequest,
    removeFriend,
    searchUsers
} from '../services/friendService';
import './Friends.css';

const Friends = () => {
    const { user } = useAuth();
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState('all');
    const [friends, setFriends] = useState([]);
    const [pendingRequests, setPendingRequests] = useState([]);
    const [searchResults, setSearchResults] = useState([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState(null);

    useEffect(() => {
        if (user) {
            loadFriends();
            loadPendingRequests();
        }
    }, [user]);

    const loadFriends = async () => {
        try {
            setLoading(true);
            const data = await getFriends();
            setFriends(data.friends || []);
        } catch (err) {
            console.error('Error loading friends:', err);
            setError('Error cargando amigos');
        } finally {
            setLoading(false);
        }
    };

    const loadPendingRequests = async () => {
        try {
            const data = await getPendingRequests();
            setPendingRequests(data.pending_requests || []);
        } catch (err) {
            console.error('Error loading pending requests:', err);
        }
    };

    const handleSearch = async (e) => {
        e.preventDefault();
        if (!searchQuery.trim()) {
            setSearchResults([]);
            return;
        }

        try {
            setLoading(true);
            setError(null);
            const data = await searchUsers(searchQuery);
            setSearchResults(data.users || []);
        } catch (err) {
            console.error('Error searching users:', err);
            setError('Error buscando usuarios');
        } finally {
            setLoading(false);
        }
    };

    const handleAcceptRequest = async (userId) => {
        try {
            setError(null);
            const data = await acceptFriendRequest(userId);
            setSuccessMessage(data.message);

            // Actualizar listas
            await loadFriends();
            await loadPendingRequests();

            setTimeout(() => setSuccessMessage(null), 3000);
        } catch (err) {
            console.error('Error accepting request:', err);
            setError(err.response?.data?.error || 'Error aceptando solicitud');
        }
    };

    const handleRejectRequest = async (userId) => {
        try {
            setError(null);
            const data = await rejectFriendRequest(userId);
            setSuccessMessage(data.message);

            // Actualizar lista
            await loadPendingRequests();

            setTimeout(() => setSuccessMessage(null), 3000);
        } catch (err) {
            console.error('Error rejecting request:', err);
            setError(err.response?.data?.error || 'Error rechazando solicitud');
        }
    };

    const handleRemoveFriend = async (userId) => {
        if (!window.confirm('¿Estás seguro de que quieres eliminar este amigo?')) {
            return;
        }

        try {
            setError(null);
            const data = await removeFriend(userId);
            setSuccessMessage(data.message);

            // Actualizar lista
            await loadFriends();

            setTimeout(() => setSuccessMessage(null), 3000);
        } catch (err) {
            console.error('Error removing friend:', err);
            setError(err.response?.data?.error || 'Error eliminando amigo');
        }
    };

    const handleOpenChat = (userId) => {
        navigate(`/chat?with=${userId}`);
    };

    const handleRequestSent = () => {
        setSuccessMessage('Solicitud de amistad enviada');
        setTimeout(() => setSuccessMessage(null), 3000);
    };

    const renderContent = () => {
        switch (activeTab) {
            case 'all':
                return (
                    <div className="friends-list">
                        <h2>Todos los amigos ({friends.length})</h2>
                        {loading ? (
                            <p className="loading">Cargando amigos...</p>
                        ) : friends.length === 0 ? (
                            <div className="empty-state">
                                <p>👥 Aún no tienes amigos</p>
                                <p>Ve a la pestaña "Añadir amigo" para buscar usuarios</p>
                            </div>
                        ) : (
                            <div className="friends-grid">
                                {friends.map(friend => (
                                    <FriendCard
                                        key={friend.id}
                                        user={friend}
                                        type="friend"
                                        onChat={handleOpenChat}
                                        onRemove={handleRemoveFriend}
                                    />
                                ))}
                            </div>
                        )}
                    </div>
                );

            case 'pending':
                return (
                    <div className="friends-list">
                        <h2>Solicitudes pendientes ({pendingRequests.length})</h2>
                        {pendingRequests.length === 0 ? (
                            <div className="empty-state">
                                <p>📭 No tienes solicitudes pendientes</p>
                            </div>
                        ) : (
                            <div className="friends-grid">
                                {pendingRequests.map(request => (
                                    <FriendCard
                                        key={request.id}
                                        user={request}
                                        type="pending"
                                        onAccept={handleAcceptRequest}
                                        onReject={handleRejectRequest}
                                    />
                                ))}
                            </div>
                        )}
                    </div>
                );

            case 'add':
                return (
                    <div className="add-friend-section">
                        <h2>Añadir amigo</h2>
                        <form onSubmit={handleSearch} className="search-form">
                            <input
                                type="text"
                                placeholder="Buscar por nombre de usuario..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="search-input"
                            />
                            <button type="submit" className="btn-search" disabled={loading}>
                                {loading ? '🔍 Buscando...' : '🔍 Buscar'}
                            </button>
                        </form>

                        {searchResults.length > 0 && (
                            <div className="search-results">
                                <h3>Resultados ({searchResults.length})</h3>
                                <div className="users-grid">
                                    {searchResults.map(searchUser => (
                                        <UserSearchCard
                                            key={searchUser.id}
                                            user={searchUser}
                                            onRequestSent={handleRequestSent}
                                        />
                                    ))}
                                </div>
                            </div>
                        )}

                        {searchQuery && searchResults.length === 0 && !loading && (
                            <div className="empty-state">
                                <p>😕 No se encontraron usuarios</p>
                            </div>
                        )}
                    </div>
                );

            default:
                return null;
        }
    };

    if (!user) {
        return (
            <div className="friends-page">
                <div className="container">
                    <p>Debes iniciar sesión para ver tus amigos</p>
                </div>
            </div>
        );
    }

    return (
        <div className="friends-page">
            <div className="container">
                <div className="friends-header">
                    <h1>👥 Amigos</h1>
                </div>

                {error && (
                    <div className="alert alert-error">
                        {error}
                        <button onClick={() => setError(null)}>✕</button>
                    </div>
                )}

                {successMessage && (
                    <div className="alert alert-success">
                        {successMessage}
                        <button onClick={() => setSuccessMessage(null)}>✕</button>
                    </div>
                )}

                <div className="friends-tabs">
                    <button
                        className={`tab ${activeTab === 'all' ? 'active' : ''}`}
                        onClick={() => setActiveTab('all')}
                    >
                        Todos los amigos
                        {friends.length > 0 && <span className="badge">{friends.length}</span>}
                    </button>
                    <button
                        className={`tab ${activeTab === 'pending' ? 'active' : ''}`}
                        onClick={() => setActiveTab('pending')}
                    >
                        Pendientes
                        {pendingRequests.length > 0 && (
                            <span className="badge badge-pending">{pendingRequests.length}</span>
                        )}
                    </button>
                    <button
                        className={`tab ${activeTab === 'add' ? 'active' : ''}`}
                        onClick={() => setActiveTab('add')}
                    >
                        Añadir amigo
                    </button>
                </div>

                <div className="friends-content">
                    {renderContent()}
                </div>
            </div>
        </div>
    );
};

export default Friends;
