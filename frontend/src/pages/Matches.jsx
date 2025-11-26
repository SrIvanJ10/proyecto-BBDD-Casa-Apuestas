import React, { useState, useEffect } from 'react';
import MatchCard from '../components/MatchCard';
import { getMatches } from '../services/matchService';

const Matches = () => {
    const [sportFilter, setSportFilter] = useState('all');
    const [statusFilter, setStatusFilter] = useState('all');
    const [matches, setMatches] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchMatches = async () => {
            setLoading(true);
            try {
                const data = await getMatches({
                    sport: sportFilter !== 'all' ? sportFilter : null,
                    status: statusFilter !== 'all' ? statusFilter : 'all'
                });
                setMatches(data);
            } catch (error) {
                console.error("Error fetching matches:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchMatches();
    }, [sportFilter, statusFilter]);

    if (loading) return <div className="container" style={{ padding: '4rem', textAlign: 'center' }}>Cargando partidos...</div>;

    return (
        <div className="container" style={{ paddingTop: '2rem', paddingBottom: '4rem' }}>
            <h2 className="text-gradient" style={{ marginBottom: '2rem' }}>Partidos Disponibles</h2>

            {/* Filtros de Estado */}
            <div style={{ marginBottom: '1.5rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600', color: 'var(--text-primary)' }}>
                    Filtrar por Estado:
                </label>
                <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                    <button
                        className={`btn ${statusFilter === 'all' ? 'btn-primary' : 'btn-secondary'}`}
                        onClick={() => setStatusFilter('all')}
                        style={statusFilter !== 'all' ? { color: 'var(--text-primary)', borderColor: '#e2e8f0' } : {}}
                    >
                        Todos
                    </button>
                    <button
                        className={`btn ${statusFilter === 'incoming' ? 'btn-primary' : 'btn-secondary'}`}
                        onClick={() => setStatusFilter('incoming')}
                        style={statusFilter !== 'incoming' ? { color: 'var(--text-primary)', borderColor: '#e2e8f0' } : {}}
                    >
                        Próximos (&lt;24h)
                    </button>
                    <button
                        className={`btn ${statusFilter === 'upcoming' ? 'btn-primary' : 'btn-secondary'}`}
                        onClick={() => setStatusFilter('upcoming')}
                        style={statusFilter !== 'upcoming' ? { color: 'var(--text-primary)', borderColor: '#e2e8f0' } : {}}
                    >
                        Esta Semana
                    </button>
                    <button
                        className={`btn ${statusFilter === 'live' ? 'btn-primary' : 'btn-secondary'}`}
                        onClick={() => setStatusFilter('live')}
                        style={statusFilter !== 'live' ? { color: 'var(--text-primary)', borderColor: '#e2e8f0' } : {}}
                    >
                        En Vivo
                    </button>
                    <button
                        className={`btn ${statusFilter === 'finished' ? 'btn-primary' : 'btn-secondary'}`}
                        onClick={() => setStatusFilter('finished')}
                        style={statusFilter !== 'finished' ? { color: 'var(--text-primary)', borderColor: '#e2e8f0' } : {}}
                    >
                        Terminados
                    </button>
                    <button
                        className={`btn ${statusFilter === 'future' ? 'btn-primary' : 'btn-secondary'}`}
                        onClick={() => setStatusFilter('future')}
                        style={statusFilter !== 'future' ? { color: 'var(--text-primary)', borderColor: '#e2e8f0' } : {}}
                    >
                        Futuros (&gt;7días)
                    </button>
                </div>
            </div>

            {/* Filtros de Deporte */}
            <div style={{ marginBottom: '2rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600', color: 'var(--text-primary)' }}>
                    Filtrar por Deporte:
                </label>
                <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                    <button
                        className={`btn ${sportFilter === 'all' ? 'btn-primary' : 'btn-secondary'}`}
                        onClick={() => setSportFilter('all')}
                        style={sportFilter !== 'all' ? { color: 'var(--text-primary)', borderColor: '#e2e8f0' } : {}}
                    >
                        Todos
                    </button>
                    <button
                        className={`btn ${sportFilter === 'fútbol' ? 'btn-primary' : 'btn-secondary'}`}
                        onClick={() => setSportFilter('fútbol')}
                        style={sportFilter !== 'fútbol' ? { color: 'var(--text-primary)', borderColor: '#e2e8f0' } : {}}
                    >
                        Fútbol
                    </button>
                    <button
                        className={`btn ${sportFilter === 'baloncesto' ? 'btn-primary' : 'btn-secondary'}`}
                        onClick={() => setSportFilter('baloncesto')}
                        style={sportFilter !== 'baloncesto' ? { color: 'var(--text-primary)', borderColor: '#e2e8f0' } : {}}
                    >
                        Baloncesto
                    </button>
                </div>
            </div>

            {matches.length > 0 ? (
                <div className="matches-grid" style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
                    gap: '2rem'
                }}>
                    {matches.map(match => (
                        <MatchCard key={match.id} match={match} />
                    ))}
                </div>
            ) : (
                <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
                    <p style={{ color: 'var(--text-secondary)' }}>No se encontraron partidos para este filtro.</p>
                </div>
            )}
        </div>
    );
};

export default Matches;
