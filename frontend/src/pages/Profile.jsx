import React, { useContext, useEffect, useState } from 'react';
import { AuthContext } from '../context/AuthContext';
import { getProfile } from '../services/userService';
import { getUserPredictions } from '../services/predictionService';
<<<<<<< HEAD
<<<<<<< HEAD
import { upgradeSubscription } from '../services/subscriptionService';
import { updateUsername, updatePassword } from '../services/adminService';

const Profile = () => {
    const { user, setUser } = useContext(AuthContext);
    const [profileData, setProfileData] = useState(null);
    const [predictions, setPredictions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [upgrading, setUpgrading] = useState(false);
    const [upgradeMessage, setUpgradeMessage] = useState('');
    const [upgradeError, setUpgradeError] = useState('');

    // Profile edit states
    const [editingUsername, setEditingUsername] = useState(false);
    const [newUsername, setNewUsername] = useState('');
    const [usernameMessage, setUsernameMessage] = useState('');
    const [usernameError, setUsernameError] = useState('');

    const [editingPassword, setEditingPassword] = useState(false);
    const [passwordData, setPasswordData] = useState({ current: '', new: '' });
    const [passwordMessage, setPasswordMessage] = useState('');
    const [passwordError, setPasswordError] = useState('');
<<<<<<< HEAD
=======
=======
import { upgradeSubscription } from '../services/subscriptionService';
>>>>>>> db693ad (v0.9)

const Profile = () => {
    const { user, setUser } = useContext(AuthContext);
    const [profileData, setProfileData] = useState(null);
    const [predictions, setPredictions] = useState([]);
    const [loading, setLoading] = useState(true);
<<<<<<< HEAD
>>>>>>> d381094 (v0.14)
=======
    const [upgrading, setUpgrading] = useState(false);
    const [upgradeMessage, setUpgradeMessage] = useState('');
    const [upgradeError, setUpgradeError] = useState('');
>>>>>>> db693ad (v0.9)
=======
>>>>>>> 4e74b6e (v1.0)

    useEffect(() => {
        const fetchProfile = async () => {
            if (user) {
                try {
                    const [profile, predictionsData] = await Promise.all([
                        getProfile(),
                        getUserPredictions()
                    ]);
                    setProfileData(profile);

                    // The API returns {predictions: [...], stats: {...}, pagination: {...}}
                    if (predictionsData.predictions) {
                        setPredictions(predictionsData.predictions);
                    }
                } catch (error) {
                    console.error("Error fetching profile:", error);
                } finally {
                    setLoading(false);
                }
            }
        };
        fetchProfile();
    }, [user]);

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> db693ad (v0.9)
    const handleUpgrade = async () => {
        setUpgrading(true);
        setUpgradeError('');
        setUpgradeMessage('');

        try {
            const response = await upgradeSubscription();
            setUpgradeMessage(response.message);

            // Update user data
            const updatedProfile = await getProfile();
            setProfileData(updatedProfile);
            if (setUser) {
                setUser({ ...user, tipo_suscripcion: 'PREMIUM', puntos_totales: response.remaining_points });
            }
        } catch (error) {
            const errorMsg = error.response?.data?.message || error.response?.data?.error || 'Error al actualizar suscripción';
            setUpgradeError(errorMsg);
        } finally {
            setUpgrading(false);
        }
    };

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 4e74b6e (v1.0)
    const handleUpdateUsername = async (e) => {
        e.preventDefault();
        setUsernameError('');
        setUsernameMessage('');
        try {
            const response = await updateUsername(newUsername);
            setUsernameMessage(response.message);
            setEditingUsername(false);
            const updatedProfile = await getProfile();
            setProfileData(updatedProfile);
            if (setUser) {
                setUser({ ...user, username: newUsername });
            }
        } catch (error) {
            setUsernameError(error.response?.data?.error || 'Error actualizando username');
        }
    };

    const handleUpdatePassword = async (e) => {
        e.preventDefault();
        setPasswordError('');
        setPasswordMessage('');
        try {
            const response = await updatePassword(passwordData.current, passwordData.new);
            setPasswordMessage(response.message);
            setEditingPassword(false);
            setPasswordData({ current: '', new: '' });
        } catch (error) {
            setPasswordError(error.response?.data?.error || 'Error actualizando contraseña');
        }
    };

<<<<<<< HEAD
=======
>>>>>>> d381094 (v0.14)
=======
>>>>>>> db693ad (v0.9)
=======
>>>>>>> 4e74b6e (v1.0)
    if (!user) {
        return <div className="container" style={{ padding: '4rem', textAlign: 'center' }}>Por favor inicia sesión para ver tu perfil.</div>;
    }

    if (loading) {
        return <div className="container" style={{ padding: '4rem', textAlign: 'center' }}>Cargando perfil...</div>;
    }

    const displayUser = profileData || user;
<<<<<<< HEAD
<<<<<<< HEAD
    const subscriptionType = displayUser.tipo_suscripcion || 'FREE';
=======
>>>>>>> d381094 (v0.14)
=======
    const subscriptionType = displayUser.tipo_suscripcion || 'FREE';
>>>>>>> db693ad (v0.9)

    return (
        <div className="container" style={{ paddingTop: '2rem', paddingBottom: '4rem' }}>
            <div className="card" style={{ marginBottom: '2rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
                    <div style={{
                        width: '80px', height: '80px', borderRadius: '50%',
                        background: 'var(--primary)', color: 'white',
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                        fontSize: '2rem', fontWeight: 'bold'
                    }}>
                        {displayUser.username ? displayUser.username[0].toUpperCase() : 'U'}
                    </div>
                    <div>
                        <h2 style={{ marginBottom: '0.25rem' }}>{displayUser.username}</h2>
                        <p style={{ color: 'var(--text-secondary)' }}>{displayUser.email || 'usuario@ejemplo.com'}</p>
                        <div style={{ marginTop: '0.5rem', display: 'flex', gap: '1rem' }}>
                            <span style={{ background: '#edf2f7', padding: '0.2rem 0.5rem', borderRadius: '4px', fontSize: '0.8rem' }}>
                                Puntos: {displayUser.puntos_totales || 0}
                            </span>
                            <span style={{ background: '#edf2f7', padding: '0.2rem 0.5rem', borderRadius: '4px', fontSize: '0.8rem' }}>
                                Nivel: {displayUser.nivel_experto || 1}
                            </span>
                        </div>
                    </div>
                </div>
            </div>

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> db693ad (v0.9)
            {/* Subscription Section */}
            <div className="card" style={{ marginBottom: '2rem', background: subscriptionType === 'PREMIUM' ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : '#f7fafc', color: subscriptionType === 'PREMIUM' ? 'white' : 'inherit' }}>
                <h3 style={{ marginBottom: '1rem', color: subscriptionType === 'PREMIUM' ? 'white' : 'inherit' }}>
                    {subscriptionType === 'PREMIUM' ? '⭐ Suscripción Premium' : '📦 Plan Gratuito'}
                </h3>

                {subscriptionType === 'FREE' ? (
                    <>
                        <p style={{ marginBottom: '1rem', color: 'var(--text-secondary)' }}>
                            Tienes un límite de 5 apuestas totales. Actualiza a Premium para apuestas ilimitadas.
                        </p>
                        <div style={{ marginBottom: '1rem' }}>
                            <strong>Beneficios Premium:</strong>
                            <ul style={{ marginTop: '0.5rem', paddingLeft: '1.5rem' }}>
                                <li>Apuestas ilimitadas</li>
                                <li>Sin restricciones</li>
                                <li>Acceso completo a todas las funciones</li>
                            </ul>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                            <button
                                className="btn btn-primary"
                                onClick={handleUpgrade}
                                disabled={upgrading || displayUser.puntos_totales < 500}
                                style={{ opacity: (upgrading || displayUser.puntos_totales < 500) ? 0.6 : 1 }}
                            >
                                {upgrading ? 'Actualizando...' : 'Actualizar a Premium (500 puntos)'}
                            </button>
                            {displayUser.puntos_totales < 500 && (
                                <span style={{ color: '#e53e3e', fontSize: '0.9rem' }}>
                                    Necesitas {500 - displayUser.puntos_totales} puntos más
                                </span>
                            )}
                        </div>
                        {upgradeMessage && (
                            <div style={{ marginTop: '1rem', padding: '0.75rem', background: '#c6f6d5', color: '#22543d', borderRadius: '0.5rem' }}>
                                {upgradeMessage}
                            </div>
                        )}
                        {upgradeError && (
                            <div style={{ marginTop: '1rem', padding: '0.75rem', background: '#fed7d7', color: '#c53030', borderRadius: '0.5rem' }}>
                                {upgradeError}
                            </div>
                        )}
                    </>
                ) : (
                    <p>¡Disfruta de apuestas ilimitadas con tu suscripción Premium!</p>
                )}
            </div>

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 4e74b6e (v1.0)
            {/* Edit Username Section */}
            <div className="card" style={{ marginBottom: '2rem' }}>
                <h3 style={{ marginBottom: '1rem' }}>Editar Nombre de Usuario</h3>
                {!editingUsername ? (
                    <div>
                        <p style={{ marginBottom: '1rem', color: 'var(--text-secondary)' }}>
                            Usuario actual: <strong>{displayUser.username}</strong>
                        </p>
                        <button onClick={() => { setEditingUsername(true); setNewUsername(displayUser.username); }} className="btn btn-primary">
                            Cambiar Username
                        </button>
                    </div>
                ) : (
                    <form onSubmit={handleUpdateUsername}>
                        <input
                            type="text"
                            value={newUsername}
                            onChange={(e) => setNewUsername(e.target.value)}
                            placeholder="Nuevo username"
                            required
                            style={{ width: '100%', padding: '0.75rem', border: '1px solid #e2e8f0', borderRadius: '0.25rem', marginBottom: '1rem' }}
                        />
                        <div style={{ display: 'flex', gap: '1rem' }}>
                            <button type="submit" className="btn btn-primary">Guardar</button>
                            <button type="button" onClick={() => setEditingUsername(false)} className="btn" style={{ background: '#e2e8f0' }}>
                                Cancelar
                            </button>
                        </div>
                    </form>
                )}
                {usernameMessage && (
                    <div style={{ marginTop: '1rem', padding: '0.75rem', background: '#c6f6d5', color: '#22543d', borderRadius: '0.5rem' }}>
                        {usernameMessage}
                    </div>
                )}
                {usernameError && (
                    <div style={{ marginTop: '1rem', padding: '0.75rem', background: '#fed7d7', color: '#c53030', borderRadius: '0.5rem' }}>
                        {usernameError}
                    </div>
                )}
            </div>

            {/* Edit Password Section */}
            <div className="card" style={{ marginBottom: '2rem' }}>
                <h3 style={{ marginBottom: '1rem' }}>Cambiar Contraseña</h3>
                {!editingPassword ? (
                    <button onClick={() => setEditingPassword(true)} className="btn btn-primary">
                        Cambiar Contraseña
                    </button>
                ) : (
                    <form onSubmit={handleUpdatePassword}>
                        <input
                            type="password"
                            value={passwordData.current}
                            onChange={(e) => setPasswordData({ ...passwordData, current: e.target.value })}
                            placeholder="Contraseña actual"
                            required
                            style={{ width: '100%', padding: '0.75rem', border: '1px solid #e2e8f0', borderRadius: '0.25rem', marginBottom: '1rem' }}
                        />
                        <input
                            type="password"
                            value={passwordData.new}
                            onChange={(e) => setPasswordData({ ...passwordData, new: e.target.value })}
                            placeholder="Nueva contraseña (mínimo 6 caracteres)"
                            required
                            minLength="6"
                            style={{ width: '100%', padding: '0.75rem', border: '1px solid #e2e8f0', borderRadius: '0.25rem', marginBottom: '1rem' }}
                        />
                        <div style={{ display: 'flex', gap: '1rem' }}>
                            <button type="submit" className="btn btn-primary">Guardar</button>
                            <button type="button" onClick={() => { setEditingPassword(false); setPasswordData({ current: '', new: '' }); }} className="btn" style={{ background: '#e2e8f0' }}>
                                Cancelar
                            </button>
                        </div>
                    </form>
                )}
                {passwordMessage && (
                    <div style={{ marginTop: '1rem', padding: '0.75rem', background: '#c6f6d5', color: '#22543d', borderRadius: '0.5rem' }}>
                        {passwordMessage}
                    </div>
                )}
                {passwordError && (
                    <div style={{ marginTop: '1rem', padding: '0.75rem', background: '#fed7d7', color: '#c53030', borderRadius: '0.5rem' }}>
                        {passwordError}
                    </div>
                )}
            </div>

<<<<<<< HEAD
=======
>>>>>>> d381094 (v0.14)
=======
>>>>>>> db693ad (v0.9)
=======
>>>>>>> 4e74b6e (v1.0)
            <h3 style={{ marginBottom: '1.5rem' }}>Mis Apuestas Recientes</h3>
            {predictions.length > 0 ? (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    {predictions.map(prediction => (
                        <div key={prediction.id} className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <div>
                                <h4 style={{ marginBottom: '0.5rem' }}>
                                    {prediction.partido?.equipo_local_nombre || 'Equipo 1'} vs {prediction.partido?.equipo_visitante_nombre || 'Equipo 2'}
                                </h4>
                                <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                                    Predicción: <span style={{ fontWeight: '600', color: 'var(--text-primary)' }}>{prediction.prediccion}</span>
                                </p>
                                <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
                                    {new Date(prediction.fecha_prediccion).toLocaleDateString('es-ES', {
                                        day: 'numeric',
                                        month: 'short',
                                        year: 'numeric',
                                        hour: '2-digit',
                                        minute: '2-digit'
                                    })}
                                </p>
                            </div>
                            <div style={{ textAlign: 'right' }}>
                                <div style={{ fontWeight: 'bold', fontSize: '1.1rem', marginBottom: '0.25rem' }}>
                                    {prediction.partido?.estado === 'FINALIZADO' ? (
                                        prediction.puntos_obtenidos > 0 ? `+${prediction.puntos_obtenidos} pts` : '0 pts'
                                    ) : (
                                        <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>--</span>
                                    )}
                                </div>
                                <span style={{
                                    padding: '0.25rem 0.75rem', borderRadius: '9999px', fontSize: '0.8rem', fontWeight: '600',
                                    backgroundColor:
                                        prediction.partido?.estado === 'PENDIENTE' ? '#bee3f8' :
                                            prediction.partido?.estado === 'EN_JUEGO' ? '#fefcbf' :
                                                prediction.partido?.estado === 'CANCELADO' ? '#e2e8f0' :
                                                    prediction.correcta === true ? '#c6f6d5' : '#fed7d7',
                                    color:
                                        prediction.partido?.estado === 'PENDIENTE' ? '#2b6cb0' :
                                            prediction.partido?.estado === 'EN_JUEGO' ? '#b7791f' :
                                                prediction.partido?.estado === 'CANCELADO' ? '#4a5568' :
                                                    prediction.correcta === true ? '#22543d' : '#c53030'
                                }}>
                                    {
                                        prediction.partido?.estado === 'PENDIENTE' ? 'Pendiente' :
                                            prediction.partido?.estado === 'EN_JUEGO' ? 'En Juego' :
                                                prediction.partido?.estado === 'CANCELADO' ? 'Cancelado' :
                                                    prediction.correcta === true ? 'Acertada' : 'Fallada'
                                    }
                                </span>
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                <p style={{ color: 'var(--text-secondary)' }}>No has realizado ninguna apuesta todavía.</p>
            )}
        </div>
    );
};

export default Profile;
