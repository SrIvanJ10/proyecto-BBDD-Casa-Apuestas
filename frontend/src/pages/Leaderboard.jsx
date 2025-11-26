import React, { useState, useEffect } from 'react';
import RankingTable from '../components/RankingTable';
import { getLeaderboard } from '../services/userService';

const Leaderboard = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchLeaderboard = async () => {
            try {
                const data = await getLeaderboard();
                setUsers(data.leaderboard || []);
            } catch (error) {
                console.error("Error fetching leaderboard:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchLeaderboard();
    }, []);

    if (loading) return <div className="container" style={{ padding: '4rem', textAlign: 'center' }}>Cargando ranking...</div>;

    return (
        <div className="container" style={{ paddingTop: '2rem', paddingBottom: '4rem' }}>
            <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
                <h2 className="text-gradient" style={{ marginBottom: '1rem' }}>Ranking de Usuarios</h2>
                <p style={{ color: 'var(--text-secondary)', maxWidth: '600px', margin: '0 auto' }}>
                    Compite con otros usuarios y demuestra quién sabe más de deportes.
                </p>
            </div>

            {users.length > 0 ? (
                <RankingTable users={users} />
            ) : (
                <p style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>Aún no hay usuarios en el ranking.</p>
            )}
        </div>
    );
};

export default Leaderboard;
