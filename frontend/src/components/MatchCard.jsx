import React, { useState, useEffect } from 'react';
import { makePrediction, checkCanPredict } from '../services/predictionService';

import AdvancedBettingForm from './AdvancedBettingForm';

const MatchCard = ({ match, live = false, onPredictionSuccess }) => {
    const [showBettingForm, setShowBettingForm] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);
    const [existingPrediction, setExistingPrediction] = useState(null);
    const [checkingPrediction, setCheckingPrediction] = useState(true);

    // Check if user already has a prediction for this match
    useEffect(() => {
        const checkExistingPrediction = async () => {
            try {
                const data = await checkCanPredict(match.id);
                if (data.user_prediction) {
                    setExistingPrediction(data.user_prediction);
                    setSuccess(true); // Mark as already bet
                }
            } catch (err) {
                console.error('Error checking prediction:', err);
            } finally {
                setCheckingPrediction(false);
            }
        };

        if (match.id) {
            checkExistingPrediction();
        }
    }, [match.id]);

    const formatDate = (dateString) => {
        if (!dateString) return 'Fecha por confirmar';
        const options = { weekday: 'short', day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' };
        return new Date(dateString).toLocaleDateString('es-ES', options);
    };

    // Extract team names and sport from the API response structure
    const team1Name = match.equipo_local?.nombre || 'Equipo 1';
    const team2Name = match.equipo_visitante?.nombre || 'Equipo 2';
    const sportName = match.equipo_local?.deporte_nombre || 'Deporte';

    // Handler para enviar la predicción avanzada
    const handleAdvancedSubmit = async (predictionData) => {
        setLoading(true);
        setError('');

        try {
            const response = await makePrediction(match.id, predictionData);

            // Only set success if we got a successful response
            if (response && (response.prediction || response.message)) {
                setSuccess(true);
                setExistingPrediction(response.prediction);
                setShowBettingForm(false);

                // Mostrar mensaje de éxito temporal
                setTimeout(() => {
                    if (onPredictionSuccess) {
                        onPredictionSuccess(response);
                    }
                }, 1500);
            } else {
                setError('Respuesta inesperada del servidor');
            }

        } catch (err) {
            const errorMsg = err.response?.data?.error || err.response?.data?.message || 'Error al realizar la apuesta';
            setError(errorMsg);

            // Auto-cerrar error después de 5 segundos
            setTimeout(() => setError(''), 5000);
        } finally {
            setLoading(false);
        }
    };

    // Determine match status
    const isFinished = match.estado === 'FINALIZADO';
    const isLive = match.estado === 'EN_JUEGO';
    const isPending = match.estado === 'PENDIENTE';

    // Get final result for display
    const finalResult = match.resultado_final || (match.goles_local !== null && match.goles_visitante !== null
        ? `${match.goles_local}-${match.goles_visitante}`
        : null);

    return (
        <div className="card match-card" style={{ borderColor: isLive ? '#fc8181' : isFinished ? '#cbd5e0' : success ? '#48bb78' : '#e2e8f0' }}>
            <div className="match-header" style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem', borderBottom: '1px solid #edf2f7', paddingBottom: '0.5rem' }}>
                <span className="sport-badge" style={{ background: isLive ? '#fed7d7' : isFinished ? '#e2e8f0' : success ? '#c6f6d5' : '#bee3f8', color: isLive ? '#c53030' : isFinished ? '#718096' : success ? '#2f855a' : '#2b6cb0', padding: '0.2rem 0.8rem', borderRadius: '20px', fontSize: '0.8rem', fontWeight: '600' }}>
                    {isLive ? 'EN VIVO' : isFinished ? 'FINALIZADO' : success ? '✓ APOSTADO' : sportName}
                </span>
                <span className="match-date" style={{ fontSize: '0.9rem', color: '#718096' }}>
                    {formatDate(match.fecha_hora || match.date)}
                </span>
            </div>

            <div className="teams" style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
                <h3 style={{ fontSize: '1.2rem', marginBottom: '0.5rem' }}>
                    {team1Name} <span style={{ color: '#cbd5e0' }}>vs</span> {team2Name}
                </h3>
                {(isLive || isFinished) && finalResult && (
                    <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: isFinished ? '#2d3748' : 'var(--primary)' }}>
                        {finalResult}
                    </div>
                )}
            </div>

            {/* Mensajes de error y éxito */}
            {error && (
                <div style={{
                    background: '#fed7d7',
                    color: '#c53030',
                    padding: '0.75rem',
                    borderRadius: '0.5rem',
                    marginBottom: '1rem',
                    fontSize: '0.9rem'
                }}>
                    {error}
                </div>
            )}

            {success && (
                <div style={{
                    background: '#c6f6d5',
                    color: '#2f855a',
                    padding: '0.75rem',
                    borderRadius: '0.5rem',
                    marginBottom: '1rem',
                    fontSize: '0.9rem',
                    textAlign: 'center'
                }}>
                    <div style={{ fontWeight: 'bold', marginBottom: '0.5rem' }}>✓ Apuesta Realizada</div>
                    {existingPrediction && (
                        <div style={{ fontSize: '0.8rem', textAlign: 'left' }}>
                            {existingPrediction.pred_goles_local !== null && (
                                <div>Resultado: {existingPrediction.pred_goles_local}-{existingPrediction.pred_goles_visitante}</div>
                            )}
                            {existingPrediction.pred_mvp_jugador && (
                                <div>MVP: {existingPrediction.pred_mvp_jugador}</div>
                            )}
                        </div>
                    )}
                </div>
            )}

            {/* Show betting form only for pending matches */}
            {isPending && !success && !showBettingForm && (
                <button
                    className="btn btn-primary"
                    style={{ width: '100%' }}
                    onClick={() => setShowBettingForm(true)}
                >
                    Realizar Predicción
                </button>
            )}

            {showBettingForm && (
                <AdvancedBettingForm
                    match={match}
                    onSubmit={handleAdvancedSubmit}
                    onCancel={() => setShowBettingForm(false)}
                    loading={loading}
                />
            )}

            {/* Show "JUGANDO" label for live matches */}
            {isLive && (
                <div style={{
                    background: 'linear-gradient(135deg, #fc8181 0%, #f56565 100%)',
                    color: 'white',
                    padding: '1rem',
                    borderRadius: '0.5rem',
                    textAlign: 'center',
                    fontSize: '1.1rem',
                    fontWeight: 'bold',
                    textTransform: 'uppercase',
                    letterSpacing: '1px',
                    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
                }}>
                    ⚽ Jugando
                </div>
            )}

            {/* Show result display for finished matches */}
            {isFinished && finalResult && (
                <div style={{
                    background: '#f7fafc',
                    border: '2px solid #e2e8f0',
                    padding: '1rem',
                    borderRadius: '0.5rem',
                    textAlign: 'center'
                }}>
                    <div style={{ fontSize: '0.85rem', color: '#718096', marginBottom: '0.5rem', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                        Resultado Final
                    </div>
                    <div style={{ fontSize: '1.8rem', fontWeight: 'bold', color: '#2d3748' }}>
                        {finalResult}
                    </div>
                </div>
            )}
        </div>
    );
};

export default MatchCard;
