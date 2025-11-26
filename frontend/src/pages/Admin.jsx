<<<<<<< HEAD
<<<<<<< HEAD
import React, { useState, useEffect } from 'react'; // Force rebuild
=======
import React, { useState, useEffect } from 'react';
>>>>>>> 4e74b6e (v1.0)
=======
import React, { useState, useEffect } from 'react'; // Force rebuild
>>>>>>> b5c841f (v1.1)
import {
    getAdminUsers, deleteAdminUser,
    getAdminSports, createAdminSport, deleteAdminSport,
    getAdminTeams, createAdminTeam, deleteAdminTeam,
<<<<<<< HEAD
<<<<<<< HEAD
    getAdminMatches, createAdminMatch, updateAdminMatch, deleteAdminMatch
=======
    getAdminMatches, createAdminMatch, updateAdminMatch, deleteAdminMatch,
    getAdminPredictions, deleteAdminPrediction
>>>>>>> 4e74b6e (v1.0)
=======
    getAdminMatches, createAdminMatch, updateAdminMatch, deleteAdminMatch
>>>>>>> b5c841f (v1.1)
} from '../services/adminService';

const Admin = () => {
    const [activeTab, setActiveTab] = useState('users');
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');

    // Data states
    const [users, setUsers] = useState([]);
    const [sports, setSports] = useState([]);
    const [teams, setTeams] = useState([]);
    const [matches, setMatches] = useState([]);
<<<<<<< HEAD
<<<<<<< HEAD
=======
    const [predictions, setPredictions] = useState([]);
>>>>>>> 4e74b6e (v1.0)
=======
>>>>>>> b5c841f (v1.1)

    // Form states
    const [newSport, setNewSport] = useState('');
    const [newTeam, setNewTeam] = useState({ nombre: '', deporte_id: '', codigo: '' });
    const [newMatch, setNewMatch] = useState({ equipo_local_id: '', equipo_visitante_id: '', fecha_hora: '', liga: '' });

    useEffect(() => {
        loadData();
    }, [activeTab]);

    const loadData = async () => {
        setLoading(true);
        setError('');
        try {
            switch (activeTab) {
                case 'users':
                    const usersData = await getAdminUsers();
                    setUsers(usersData.users || []);
                    break;
                case 'sports':
                    const sportsData = await getAdminSports();
                    setSports(sportsData.sports || []);
                    break;
                case 'teams':
                    const teamsData = await getAdminTeams();
                    setTeams(teamsData.teams || []);
                    const sportsForTeams = await getAdminSports();
                    setSports(sportsForTeams.sports || []);
                    break;
                case 'matches':
                    const matchesData = await getAdminMatches();
                    setMatches(matchesData.matches || []);
                    const teamsForMatches = await getAdminTeams();
                    setTeams(teamsForMatches.teams || []);
                    break;
<<<<<<< HEAD
<<<<<<< HEAD

=======
                case 'predictions':
                    const predsData = await getAdminPredictions();
                    setPredictions(predsData.predictions || []);
                    break;
>>>>>>> 4e74b6e (v1.0)
=======

>>>>>>> b5c841f (v1.1)
            }
        } catch (err) {
            setError(err.response?.data?.error || 'Error cargando datos');
        } finally {
            setLoading(false);
        }
    };

    const handleDeleteUser = async (userId) => {
        if (!window.confirm('¿Eliminar este usuario?')) return;
        try {
            await deleteAdminUser(userId);
            setMessage('Usuario eliminado');
            loadData();
        } catch (err) {
            setError(err.response?.data?.error || 'Error');
        }
    };

    const handleCreateSport = async (e) => {
        e.preventDefault();
        try {
            await createAdminSport({ nombre: newSport });
            setMessage('Deporte creado');
            setNewSport('');
            loadData();
        } catch (err) {
            setError(err.response?.data?.error || 'Error');
        }
    };

    const handleDeleteSport = async (sportId) => {
        if (!window.confirm('¿Eliminar este deporte?')) return;
        try {
            await deleteAdminSport(sportId);
            setMessage('Deporte eliminado');
            loadData();
        } catch (err) {
            setError(err.response?.data?.error || 'Error');
        }
    };

    const handleCreateTeam = async (e) => {
        e.preventDefault();
        try {
            await createAdminTeam(newTeam);
            setMessage('Equipo creado');
            setNewTeam({ nombre: '', deporte_id: '', codigo: '' });
            loadData();
        } catch (err) {
            setError(err.response?.data?.error || 'Error');
        }
    };

    const handleDeleteTeam = async (teamId) => {
        if (!window.confirm('¿Eliminar este equipo?')) return;
        try {
            await deleteAdminTeam(teamId);
            setMessage('Equipo eliminado');
            loadData();
        } catch (err) {
            setError(err.response?.data?.error || 'Error');
        }
    };

    const handleCreateMatch = async (e) => {
        e.preventDefault();
        try {
            await createAdminMatch(newMatch);
            setMessage('Partido creado');
            setNewMatch({ equipo_local_id: '', equipo_visitante_id: '', fecha_hora: '', liga: '' });
            loadData();
        } catch (err) {
            setError(err.response?.data?.error || 'Error');
        }
    };

    const handleUpdateMatch = async (matchId, estado) => {
        try {
            await updateAdminMatch(matchId, { estado });
            setMessage('Partido actualizado');
            loadData();
        } catch (err) {
            setError(err.response?.data?.error || 'Error');
        }
    };

    const handleDeleteMatch = async (matchId) => {
        if (!window.confirm('¿Eliminar este partido?')) return;
        try {
            await deleteAdminMatch(matchId);
            setMessage('Partido eliminado');
            loadData();
        } catch (err) {
            setError(err.response?.data?.error || 'Error');
        }
    };

<<<<<<< HEAD
<<<<<<< HEAD

=======
    const handleDeletePrediction = async (predId) => {
        if (!window.confirm('¿Eliminar esta predicción?')) return;
        try {
            await deleteAdminPrediction(predId);
            setMessage('Predicción eliminada');
            loadData();
        } catch (err) {
            setError(err.response?.data?.error || 'Error');
        }
    };
>>>>>>> 4e74b6e (v1.0)
=======

>>>>>>> b5c841f (v1.1)

    const tabs = [
        { id: 'users', label: '👥 Usuarios' },
        { id: 'sports', label: '⚽ Deportes' },
        { id: 'teams', label: '🏆 Equipos' },
<<<<<<< HEAD
<<<<<<< HEAD
        { id: 'matches', label: '📅 Partidos' }
=======
        { id: 'matches', label: '📅 Partidos' },
        { id: 'predictions', label: '🎯 Predicciones' }
>>>>>>> 4e74b6e (v1.0)
=======
        { id: 'matches', label: '📅 Partidos' }
>>>>>>> b5c841f (v1.1)
    ];

    return (
        <div className="container" style={{ paddingTop: '2rem', paddingBottom: '4rem' }}>
            <h1 style={{ marginBottom: '2rem' }}>⚙️ Panel de Administración</h1>

            {/* Tabs */}
            <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '2rem', borderBottom: '2px solid #e2e8f0' }}>
                {tabs.map(tab => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        style={{
                            padding: '0.75rem 1.5rem',
                            border: 'none',
                            background: activeTab === tab.id ? 'var(--primary)' : 'transparent',
                            color: activeTab === tab.id ? 'white' : 'var(--text-primary)',
                            borderRadius: '0.5rem 0.5rem 0 0',
                            cursor: 'pointer',
                            fontWeight: activeTab === tab.id ? 'bold' : 'normal'
                        }}
                    >
                        {tab.label}
                    </button>
                ))}
            </div>

            {/* Messages */}
            {message && (
                <div style={{ padding: '1rem', background: '#c6f6d5', color: '#22543d', borderRadius: '0.5rem', marginBottom: '1rem' }}>
                    {message}
                </div>
            )}
            {error && (
                <div style={{ padding: '1rem', background: '#fed7d7', color: '#c53030', borderRadius: '0.5rem', marginBottom: '1rem' }}>
                    {error}
                </div>
            )}

            {loading ? (
                <div style={{ textAlign: 'center', padding: '2rem' }}>Cargando...</div>
            ) : (
                <>
                    {/* USERS TAB */}
                    {activeTab === 'users' && (
                        <div className="card">
                            <h2 style={{ marginBottom: '1rem' }}>Usuarios ({users.length})</h2>
                            <div style={{ overflowX: 'auto' }}>
                                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                                    <thead>
                                        <tr style={{ borderBottom: '2px solid #e2e8f0' }}>
                                            <th style={{ padding: '0.75rem', textAlign: 'left' }}>ID</th>
                                            <th style={{ padding: '0.75rem', textAlign: 'left' }}>Username</th>
                                            <th style={{ padding: '0.75rem', textAlign: 'left' }}>Email</th>
                                            <th style={{ padding: '0.75rem', textAlign: 'left' }}>Puntos</th>
                                            <th style={{ padding: '0.75rem', textAlign: 'left' }}>Suscripción</th>
                                            <th style={{ padding: '0.75rem', textAlign: 'left' }}>Acciones</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {users.map(user => (
                                            <tr key={user.id} style={{ borderBottom: '1px solid #e2e8f0' }}>
                                                <td style={{ padding: '0.75rem' }}>{user.id}</td>
                                                <td style={{ padding: '0.75rem' }}>{user.username}</td>
                                                <td style={{ padding: '0.75rem' }}>{user.email}</td>
                                                <td style={{ padding: '0.75rem' }}>{user.puntos_totales}</td>
                                                <td style={{ padding: '0.75rem' }}>{user.tipo_suscripcion || 'FREE'}</td>
                                                <td style={{ padding: '0.75rem' }}>
                                                    <button
                                                        onClick={() => handleDeleteUser(user.id)}
                                                        style={{ padding: '0.5rem 1rem', background: '#e53e3e', color: 'white', border: 'none', borderRadius: '0.25rem', cursor: 'pointer' }}
                                                    >
                                                        Eliminar
                                                    </button>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    )}

                    {/* SPORTS TAB */}
                    {activeTab === 'sports' && (
                        <div className="card">
                            <h2 style={{ marginBottom: '1rem' }}>Deportes ({sports.length})</h2>
                            <form onSubmit={handleCreateSport} style={{ marginBottom: '2rem', display: 'flex', gap: '1rem' }}>
                                <input
                                    type="text"
                                    placeholder="Nombre del deporte"
                                    value={newSport}
                                    onChange={(e) => setNewSport(e.target.value)}
                                    required
                                    style={{ flex: 1, padding: '0.75rem', border: '1px solid #e2e8f0', borderRadius: '0.25rem' }}
                                />
                                <button type="submit" className="btn btn-primary">Crear Deporte</button>
                            </form>
                            <div style={{ display: 'grid', gap: '1rem' }}>
                                {sports.map(sport => (
                                    <div key={sport.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem', background: '#f7fafc', borderRadius: '0.5rem' }}>
                                        <div>
                                            <strong>{sport.nombre}</strong>
                                            <span style={{ marginLeft: '1rem', color: '#718096' }}>ID: {sport.id}</span>
                                        </div>
                                        <button
                                            onClick={() => handleDeleteSport(sport.id)}
                                            style={{ padding: '0.5rem 1rem', background: '#e53e3e', color: 'white', border: 'none', borderRadius: '0.25rem', cursor: 'pointer' }}
                                        >
                                            Eliminar
                                        </button>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* TEAMS TAB */}
                    {activeTab === 'teams' && (
                        <div className="card">
                            <h2 style={{ marginBottom: '1rem' }}>Equipos ({teams.length})</h2>
                            <form onSubmit={handleCreateTeam} style={{ marginBottom: '2rem', display: 'grid', gap: '1rem' }}>
                                <input
                                    type="text"
                                    placeholder="Nombre del equipo"
                                    value={newTeam.nombre}
                                    onChange={(e) => setNewTeam({ ...newTeam, nombre: e.target.value })}
                                    required
                                    style={{ padding: '0.75rem', border: '1px solid #e2e8f0', borderRadius: '0.25rem' }}
                                />
                                <select
                                    value={newTeam.deporte_id}
                                    onChange={(e) => setNewTeam({ ...newTeam, deporte_id: e.target.value })}
                                    required
                                    style={{ padding: '0.75rem', border: '1px solid #e2e8f0', borderRadius: '0.25rem' }}
                                >
                                    <option value="">Seleccionar deporte</option>
                                    {sports.map(sport => (
                                        <option key={sport.id} value={sport.id}>{sport.nombre}</option>
                                    ))}
                                </select>
                                <input
                                    type="text"
                                    placeholder="Código (ej: BAR, RMA)"
                                    value={newTeam.codigo}
                                    onChange={(e) => setNewTeam({ ...newTeam, codigo: e.target.value })}
                                    required
                                    style={{ padding: '0.75rem', border: '1px solid #e2e8f0', borderRadius: '0.25rem' }}
                                />
                                <button type="submit" className="btn btn-primary">Crear Equipo</button>
                            </form>
                            <div style={{ display: 'grid', gap: '1rem' }}>
                                {teams.map(team => (
                                    <div key={team.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem', background: '#f7fafc', borderRadius: '0.5rem' }}>
                                        <div>
                                            <strong>{team.nombre}</strong>
                                            <span style={{ marginLeft: '1rem', color: '#718096' }}>
                                                {team.deporte_nombre || 'Deporte'} | Código: {team.codigo}
                                            </span>
                                        </div>
                                        <button
                                            onClick={() => handleDeleteTeam(team.id)}
                                            style={{ padding: '0.5rem 1rem', background: '#e53e3e', color: 'white', border: 'none', borderRadius: '0.25rem', cursor: 'pointer' }}
                                        >
                                            Eliminar
                                        </button>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* MATCHES TAB */}
                    {activeTab === 'matches' && (
                        <div className="card">
                            <h2 style={{ marginBottom: '1rem' }}>Partidos ({matches.length})</h2>
                            <form onSubmit={handleCreateMatch} style={{ marginBottom: '2rem', display: 'grid', gap: '1rem' }}>
                                <select
                                    value={newMatch.equipo_local_id}
                                    onChange={(e) => setNewMatch({ ...newMatch, equipo_local_id: e.target.value })}
                                    required
                                    style={{ padding: '0.75rem', border: '1px solid #e2e8f0', borderRadius: '0.25rem' }}
                                >
                                    <option value="">Equipo Local</option>
                                    {teams.map(team => (
                                        <option key={team.id} value={team.id}>{team.nombre}</option>
                                    ))}
                                </select>
                                <select
                                    value={newMatch.equipo_visitante_id}
                                    onChange={(e) => setNewMatch({ ...newMatch, equipo_visitante_id: e.target.value })}
                                    required
                                    style={{ padding: '0.75rem', border: '1px solid #e2e8f0', borderRadius: '0.25rem' }}
                                >
                                    <option value="">Equipo Visitante</option>
                                    {teams.map(team => (
                                        <option key={team.id} value={team.id}>{team.nombre}</option>
                                    ))}
                                </select>
                                <input
                                    type="datetime-local"
                                    value={newMatch.fecha_hora}
                                    onChange={(e) => setNewMatch({ ...newMatch, fecha_hora: e.target.value })}
                                    required
                                    style={{ padding: '0.75rem', border: '1px solid #e2e8f0', borderRadius: '0.25rem' }}
                                />
                                <input
                                    type="text"
                                    placeholder="Liga"
                                    value={newMatch.liga}
                                    onChange={(e) => setNewMatch({ ...newMatch, liga: e.target.value })}
                                    required
                                    style={{ padding: '0.75rem', border: '1px solid #e2e8f0', borderRadius: '0.25rem' }}
                                />
                                <button type="submit" className="btn btn-primary">Crear Partido</button>
                            </form>
                            <div style={{ display: 'grid', gap: '1rem' }}>
                                {matches.map(match => (
                                    <div key={match.id} style={{ padding: '1rem', background: '#f7fafc', borderRadius: '0.5rem' }}>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                            <strong>{match.equipo_local_nombre} vs {match.equipo_visitante_nombre}</strong>
                                            <span style={{ color: '#718096' }}>{match.estado}</span>
                                        </div>
                                        <div style={{ fontSize: '0.9rem', color: '#718096', marginBottom: '0.5rem' }}>
                                            {new Date(match.fecha_hora).toLocaleString('es-ES')} | {match.liga}
                                        </div>
                                        <div style={{ display: 'flex', gap: '0.5rem' }}>
                                            <button onClick={() => handleUpdateMatch(match.id, 'EN_JUEGO')} style={{ padding: '0.5rem 1rem', background: '#48bb78', color: 'white', border: 'none', borderRadius: '0.25rem', cursor: 'pointer' }}>
                                                En Juego
                                            </button>
                                            <button onClick={() => handleUpdateMatch(match.id, 'FINALIZADO')} style={{ padding: '0.5rem 1rem', background: '#4299e1', color: 'white', border: 'none', borderRadius: '0.25rem', cursor: 'pointer' }}>
                                                Finalizado
                                            </button>
                                            <button onClick={() => handleDeleteMatch(match.id)} style={{ padding: '0.5rem 1rem', background: '#e53e3e', color: 'white', border: 'none', borderRadius: '0.25rem', cursor: 'pointer' }}>
                                                Eliminar
                                            </button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

<<<<<<< HEAD
<<<<<<< HEAD

=======
                    {/* PREDICTIONS TAB */}
                    {activeTab === 'predictions' && (
                        <div className="card">
                            <h2 style={{ marginBottom: '1rem' }}>Predicciones ({predictions.length})</h2>
                            <div style={{ overflowX: 'auto' }}>
                                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                                    <thead>
                                        <tr style={{ borderBottom: '2px solid #e2e8f0' }}>
                                            <th style={{ padding: '0.75rem', textAlign: 'left' }}>ID</th>
                                            <th style={{ padding: '0.75rem', textAlign: 'left' }}>Usuario</th>
                                            <th style={{ padding: '0.75rem', textAlign: 'left' }}>Partido</th>
                                            <th style={{ padding: '0.75rem', textAlign: 'left' }}>Predicción</th>
                                            <th style={{ padding: '0.75rem', textAlign: 'left' }}>Puntos</th>
                                            <th style={{ padding: '0.75rem', textAlign: 'left' }}>Acciones</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {predictions.map(pred => (
                                            <tr key={pred.id} style={{ borderBottom: '1px solid #e2e8f0' }}>
                                                <td style={{ padding: '0.75rem' }}>{pred.id}</td>
                                                <td style={{ padding: '0.75rem' }}>{pred.usuario_username || pred.usuario}</td>
                                                <td style={{ padding: '0.75rem' }}>{pred.partido_id}</td>
                                                <td style={{ padding: '0.75rem' }}>{pred.prediccion}</td>
                                                <td style={{ padding: '0.75rem' }}>{pred.puntos_obtenidos || 0}</td>
                                                <td style={{ padding: '0.75rem' }}>
                                                    <button
                                                        onClick={() => handleDeletePrediction(pred.id)}
                                                        style={{ padding: '0.5rem 1rem', background: '#e53e3e', color: 'white', border: 'none', borderRadius: '0.25rem', cursor: 'pointer' }}
                                                    >
                                                        Eliminar
                                                    </button>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    )}
>>>>>>> 4e74b6e (v1.0)
=======

>>>>>>> b5c841f (v1.1)
                </>
            )}
        </div>
    );
};

export default Admin;
