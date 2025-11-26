import React from 'react';

const RankingTable = ({ users }) => {
    return (
        <div className="card" style={{ overflowX: 'auto', padding: 0 }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                    <tr style={{ background: 'var(--secondary)', color: 'white' }}>
                        <th style={{ padding: '1rem', textAlign: 'left' }}>Posición</th>
                        <th style={{ padding: '1rem', textAlign: 'left' }}>Usuario</th>
                        <th style={{ padding: '1rem', textAlign: 'left' }}>Aciertos</th>
                        <th style={{ padding: '1rem', textAlign: 'left' }}>% Acierto</th>
                        <th style={{ padding: '1rem', textAlign: 'left' }}>Puntos</th>
                    </tr>
                </thead>
                <tbody>
                    {users.map((user, index) => (
                        <tr key={user.username} style={{ borderBottom: '1px solid #edf2f7', transition: 'background 0.2s' }}>
                            <td style={{ padding: '1rem', fontWeight: 'bold', color: index < 3 ? 'var(--primary)' : 'inherit' }}>
                                {index + 1}
                            </td>
                            <td style={{ padding: '1rem', fontWeight: '600' }}>{user.username}</td>
                            <td style={{ padding: '1rem' }}>{user.correct_predictions || 0}</td>
                            <td style={{ padding: '1rem' }}>{user.success_rate || 0}%</td>
                            <td style={{ padding: '1rem', fontWeight: 'bold' }}>{user.puntos_totales || 0}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default RankingTable;
