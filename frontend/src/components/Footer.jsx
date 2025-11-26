import React from 'react';

const Footer = () => {
    return (
        <footer className="footer" style={{ backgroundColor: 'var(--secondary)', color: 'var(--text-light)', padding: '3rem 0 1rem', marginTop: 'auto' }}>
            <div className="container">
                <div style={{ display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: '2rem', marginBottom: '2rem' }}>
                    <div style={{ flex: 1, minWidth: '200px' }}>
                        <h3 style={{ color: 'var(--primary)', marginBottom: '1rem' }}>Sport 365</h3>
                        <p>Plataforma líder en apuestas deportivas.</p>
                    </div>
                    <div style={{ flex: 1, minWidth: '200px' }}>
                        <h3 style={{ color: 'var(--primary)', marginBottom: '1rem' }}>Enlaces</h3>
                        <ul style={{ listStyle: 'none' }}>
                            <li style={{ marginBottom: '0.5rem' }}><a href="/">Inicio</a></li>
                            <li style={{ marginBottom: '0.5rem' }}><a href="/matches">Partidos</a></li>
                            <li style={{ marginBottom: '0.5rem' }}><a href="/leaderboard">Ranking</a></li>
                        </ul>
                    </div>
                </div>
                <div style={{ textAlign: 'center', borderTop: '1px solid var(--secondary-dark)', paddingTop: '2rem' }}>
                    <p>&copy; 2025 Sport 365. Todos los derechos reservados.</p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
