import React from 'react';

const RecommendationCard = ({ recommendation }) => {
    // La API devuelve un objeto Partido, no un objeto con confidence/reason
    // Adaptamos la visualización para mostrar el partido recomendado

    const formatDate = (dateString) => {
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
        return new Date(dateString).toLocaleDateString('es-ES', options);
    };

    // Función para renderizar el botón/estado según el estado del partido
    const renderActionArea = () => {
        const estado = recommendation.estado;

        if (estado === 'FINALIZADO') {
            return (
                <div>
                    <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Resultado Final</p>
                    <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--primary)' }}>
                        {recommendation.resultado_final || 'N/A'}
                    </p>
                </div>
            );
        } else if (estado === 'EN_JUEGO') {
            return (
                <div style={{
                    backgroundColor: '#fef3c7',
                    color: '#92400e',
                    padding: '0.5rem 1rem',
                    borderRadius: '0.5rem',
                    fontWeight: 'bold',
                    textAlign: 'center',
                    fontSize: '0.9rem',
                    textTransform: 'uppercase',
                    border: '2px solid #fbbf24'
                }}>
                    🔴 Jugando
                </div>
            );
        } else {
            // PENDIENTE
            return (
                <button className="btn btn-sm btn-outline" style={{ padding: '0.25rem 0.75rem', fontSize: '0.8rem' }}>
                    Predecir Ahora
                </button>
            );
        }
    };

    return (
        <div className="card recommendation-card" style={{ borderLeft: '4px solid var(--primary)' }}>
            <div style={{ marginBottom: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{
                    backgroundColor: '#e6fffa',
                    color: '#2c7a7b',
                    padding: '0.25rem 0.75rem',
                    borderRadius: '9999px',
                    fontSize: '0.75rem',
                    fontWeight: 'bold',
                    textTransform: 'uppercase'
                }}>
                    Recomendado para ti
                </span>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                    {recommendation.deporte_nombre || 'Deporte'}
                </span>
            </div>

            <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>
                {recommendation.equipo_local_nombre} vs {recommendation.equipo_visitante_nombre}
            </h3>

            <div style={{ marginBottom: '1rem' }}>
                <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Fecha:</p>
                <p style={{ fontSize: '1rem', fontWeight: '500' }}>{formatDate(recommendation.fecha_hora)}</p>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '1rem' }}>
                <div>
                    <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Liga</p>
                    <p style={{ fontWeight: '600' }}>{recommendation.liga || 'General'}</p>
                </div>
                {renderActionArea()}
            </div>
        </div>
    );
};

export default RecommendationCard;
