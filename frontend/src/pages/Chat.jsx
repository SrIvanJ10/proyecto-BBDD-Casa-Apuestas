import React, { useEffect, useMemo, useRef, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getConversations, getMessagesWithUser } from '../services/chatService';
import './Chat.css';

// URL base del servidor WebSocket (mismo host que la API REST)
const WS_BASE = 'ws://localhost:8000';

const Chat = () => {
    const { user } = useAuth();
    const [searchParams] = useSearchParams();
    const initialUserId = useMemo(() => {
        const raw = searchParams.get('with');
        return raw ? parseInt(raw, 10) : null;
    }, [searchParams]);

    const [conversations, setConversations] = useState([]);
    const [selectedUser, setSelectedUser] = useState(null);
    const [messages, setMessages] = useState([]);
    const [messageText, setMessageText] = useState('');
    const [loadingConversations, setLoadingConversations] = useState(false);
    const [loadingMessages, setLoadingMessages] = useState(false);
    const [connected, setConnected] = useState(false);
    const [error, setError] = useState(null);

    const wsRef = useRef(null);

    useEffect(() => {
        if (user) {
            loadConversations(initialUserId);
        }
        return () => {
            wsRef.current?.close();
        };
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [user]);

    // ------------------------------------------------------------------
    // WebSocket
    // ------------------------------------------------------------------

    const connectWebSocket = (userId) => {
        wsRef.current?.close();

        const token = localStorage.getItem('token');
        if (!token) return;

        const ws = new WebSocket(`${WS_BASE}/ws/chat/${userId}/?token=${token}`);

        ws.onopen = () => setConnected(true);

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                if (data.type === 'message') {
                    const msg = data.message;
                    setMessages(prev => [...prev, msg]);
                    // Actualizar el último mensaje en la barra lateral
                    setConversations(prev => prev.map(c =>
                        c.user.id === (msg.sender.id === user.id ? msg.receiver.id : msg.sender.id)
                            ? { ...c, last_message: msg, unread_count: 0 }
                            : c
                    ));
                }
            } catch (e) {
                console.error('Error parseando mensaje WebSocket', e);
            }
        };

        ws.onerror = () => {
            setError('Error en la conexión en tiempo real');
            setConnected(false);
        };

        ws.onclose = () => setConnected(false);

        wsRef.current = ws;
    };

    // ------------------------------------------------------------------
    // Carga de datos (REST)
    // ------------------------------------------------------------------

    const loadConversations = async (selectUserId = null) => {
        try {
            setLoadingConversations(true);
            const data = await getConversations();
            setConversations(data.conversations || []);

            if (selectUserId) {
                const match = (data.conversations || []).find(c => c.user.id === selectUserId);
                if (match) {
                    await selectConversation(match.user.id);
                }
            }
        } catch (err) {
            console.error('Error cargando conversaciones', err);
            setError('No se pudieron cargar las conversaciones');
        } finally {
            setLoadingConversations(false);
        }
    };

    const selectConversation = async (userId) => {
        try {
            setLoadingMessages(true);
            setError(null);
            const data = await getMessagesWithUser(userId, { limit: 100 });
            setMessages(data.messages || []);
            setSelectedUser(data.with_user);
            connectWebSocket(userId);
        } catch (err) {
            console.error('Error cargando mensajes', err);
            setError(err.response?.data?.error || 'No se pudieron cargar los mensajes');
        } finally {
            setLoadingMessages(false);
        }
    };

    // ------------------------------------------------------------------
    // Envío de mensajes (WebSocket)
    // ------------------------------------------------------------------

    const handleSend = (e) => {
        e.preventDefault();
        if (!selectedUser || !messageText.trim()) return;

        const text = messageText.trim();

        if (wsRef.current?.readyState === WebSocket.OPEN) {
            wsRef.current.send(JSON.stringify({ content: text }));
            setMessageText('');
        } else {
            setError('Sin conexión en tiempo real. Selecciona la conversación de nuevo.');
        }
    };

    // ------------------------------------------------------------------
    // Render
    // ------------------------------------------------------------------

    if (!user) {
        return (
            <div className="chat-page">
                <div className="container">
                    <p>Debes iniciar sesión para usar el chat.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="chat-page">
            <div className="container chat-layout">
                <aside className="chat-sidebar">
                    <div className="chat-sidebar-header">
                        <h2>Conversaciones</h2>
                        <button className="btn-refresh" onClick={() => loadConversations(selectedUser?.id)} disabled={loadingConversations}>
                            {loadingConversations ? 'Actualizando...' : '↻'}
                        </button>
                    </div>
                    {conversations.length === 0 && !loadingConversations ? (
                        <p className="empty-state">Aún no tienes conversaciones. ¡Habla con tus amigos!</p>
                    ) : (
                        <ul className="conversation-list">
                            {conversations.map((conv) => (
                                <li
                                    key={conv.user.id}
                                    className={`conversation-item ${selectedUser?.id === conv.user.id ? 'active' : ''}`}
                                    onClick={() => selectConversation(conv.user.id)}
                                >
                                    <div className="conversation-avatar">
                                        {conv.user.avatar ? (
                                            <img src={conv.user.avatar} alt={conv.user.username} />
                                        ) : (
                                            <div className="avatar-placeholder">{conv.user.username.charAt(0).toUpperCase()}</div>
                                        )}
                                    </div>
                                    <div className="conversation-info">
                                        <div className="conversation-top">
                                            <span className="conversation-name">{conv.user.username}</span>
                                            {conv.unread_count > 0 && <span className="badge-unread">{conv.unread_count}</span>}
                                        </div>
                                        <p className="conversation-snippet">
                                            {conv.last_message?.content ? conv.last_message.content.slice(0, 60) : 'Sin mensajes aún'}
                                        </p>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    )}
                </aside>

                <section className="chat-main">
                    {error && (
                        <div className="alert alert-error">
                            {error}
                            <button onClick={() => setError(null)}>✕</button>
                        </div>
                    )}

                    {!selectedUser ? (
                        <div className="chat-placeholder">
                            <p>Selecciona un amigo para comenzar a chatear.</p>
                        </div>
                    ) : (
                        <div className="chat-window">
                            <header className="chat-header">
                                <div className="chat-user">
                                    <div className="conversation-avatar">
                                        {selectedUser.avatar ? (
                                            <img src={selectedUser.avatar} alt={selectedUser.username} />
                                        ) : (
                                            <div className="avatar-placeholder">{selectedUser.username.charAt(0).toUpperCase()}</div>
                                        )}
                                    </div>
                                    <div>
                                        <h3>{selectedUser.username}</h3>
                                        <small className={connected ? 'status-online' : 'status-offline'}>
                                            {connected ? '● En línea' : '○ Conectando...'}
                                        </small>
                                    </div>
                                </div>
                            </header>

                            <div className="chat-messages">
                                {loadingMessages ? (
                                    <p className="loading">Cargando mensajes...</p>
                                ) : messages.length === 0 ? (
                                    <p className="empty-state">Aún no hay mensajes. Escribe el primero.</p>
                                ) : (
                                    messages.map(msg => (
                                        <div
                                            key={msg.id}
                                            className={`message ${msg.sender.id === user.id ? 'own' : ''}`}
                                        >
                                            <div className="message-content">{msg.content}</div>
                                            <div className="message-meta">
                                                <span>{new Date(msg.created_at).toLocaleString()}</span>
                                                {msg.sender.id === user.id && (
                                                    <span className="message-status">{msg.is_read ? '✓✓' : '✓'}</span>
                                                )}
                                            </div>
                                        </div>
                                    ))
                                )}
                            </div>

                            <form className="chat-input" onSubmit={handleSend}>
                                <input
                                    type="text"
                                    placeholder="Escribe tu mensaje..."
                                    value={messageText}
                                    onChange={(e) => setMessageText(e.target.value)}
                                    disabled={!connected}
                                />
                                <button type="submit" className="btn-send" disabled={!connected || !messageText.trim()}>
                                    Enviar
                                </button>
                            </form>
                        </div>
                    )}
                </section>
            </div>
        </div>
    );
};

export default Chat;
