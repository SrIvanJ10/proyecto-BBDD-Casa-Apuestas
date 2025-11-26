import React, { useState, useEffect } from 'react';
import RecommendationCard from '../components/RecommendationCard';
import { getRecommendedMatches } from '../services/recommendationService';

const Recommendations = () => {
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchRecommendations = async () => {
            try {
                const data = await getRecommendedMatches();
                setRecommendations(data.recommended_matches || []);
            } catch (error) {
                console.error("Error fetching recommendations:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchRecommendations();
    }, []);

    if (loading) return <div className="container" style={{ padding: '4rem', textAlign: 'center' }}>Cargando recomendaciones...</div>;

    return (
        <div className="container" style={{ paddingTop: '2rem', paddingBottom: '4rem' }}>
            <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
                <h2 className="text-gradient" style={{ marginBottom: '1rem' }}>Recomendaciones</h2>
                <p style={{ color: 'var(--text-secondary)', maxWidth: '600px', margin: '0 auto' }}>
                    Nuestros algoritmos analizan miles de datos para ofrecerte las mejores predicciones.
                </p>
            </div>

            {recommendations.length > 0 ? (
                <div className="recommendations-grid" style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
                    gap: '2rem'
                }}>
                    {recommendations.map((rec, index) => (
                        <RecommendationCard key={index} recommendation={rec} />
                    ))}
                </div>
            ) : (
                <p style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>
                    No hay recomendaciones disponibles en este momento. ¡Vuelve más tarde!
                </p>
            )}
        </div>
    );
};

export default Recommendations;
