import React, { useState } from 'react';

const AdvancedBettingForm = ({ match, onSubmit, onCancel, loading }) => {
    const [activeTab, setActiveTab] = useState('resultado');
    const [predictions, setPredictions] = useState({
        pred_goles_local: '',
        pred_goles_visitante: '',
        pred_amarillas_local: '',
        pred_amarillas_visitante: '',
        pred_rojas_local: '',
        pred_rojas_visitante: '',
        pred_expulsiones_local: '',
        pred_expulsiones_visitante: '',
        pred_mvp_jugador: ''
    });
    const [errors, setErrors] = useState({});

    const sportName = match.equipo_local?.deporte_nombre || 'Deporte';
    const isFootball = sportName.toLowerCase() === 'fútbol';
    const isBasketball = sportName.toLowerCase() === 'baloncesto';

    const handleChange = (e) => {
        const { name, value } = e.target;
        setPredictions(prev => ({
            ...prev,
            [name]: value
        }));
        // Clear error when typing
        if (errors[name]) {
            setErrors(prev => ({ ...prev, [name]: null }));
        }
    };

    const validate = () => {
        const newErrors = {};
        let hasPrediction = false;

        // Limites
        const LIMITS = {
            goals: 20,
            points: 200,
            yellow: 16,
            red: 5,
            fouls: 5
        };

        // Validar Goles/Puntos
        if (predictions.pred_goles_local !== '' || predictions.pred_goles_visitante !== '') {
            hasPrediction = true;
            const limit = isBasketball ? LIMITS.points : LIMITS.goals;
            if (predictions.pred_goles_local > limit) newErrors.pred_goles_local = `Máx ${limit}`;
            if (predictions.pred_goles_visitante > limit) newErrors.pred_goles_visitante = `Máx ${limit}`;
        }

        // Validar Tarjetas (Solo Fútbol)
        if (isFootball) {
            if (predictions.pred_amarillas_local !== '' || predictions.pred_amarillas_visitante !== '') {
                hasPrediction = true;
                if (predictions.pred_amarillas_local > LIMITS.yellow) newErrors.pred_amarillas_local = `Máx ${LIMITS.yellow}`;
                if (predictions.pred_amarillas_visitante > LIMITS.yellow) newErrors.pred_amarillas_visitante = `Máx ${LIMITS.yellow}`;
            }
            if (predictions.pred_rojas_local !== '' || predictions.pred_rojas_visitante !== '') {
                hasPrediction = true;
                if (predictions.pred_rojas_local > LIMITS.red) newErrors.pred_rojas_local = `Máx ${LIMITS.red}`;
                if (predictions.pred_rojas_visitante > LIMITS.red) newErrors.pred_rojas_visitante = `Máx ${LIMITS.red}`;
            }
        }

        // Validar Expulsiones (Solo Baloncesto)
        if (isBasketball) {
            if (predictions.pred_expulsiones_local !== '' || predictions.pred_expulsiones_visitante !== '') {
                hasPrediction = true;
                if (predictions.pred_expulsiones_local > LIMITS.fouls) newErrors.pred_expulsiones_local = `Máx ${LIMITS.fouls}`;
                if (predictions.pred_expulsiones_visitante > LIMITS.fouls) newErrors.pred_expulsiones_visitante = `Máx ${LIMITS.fouls}`;
            }
        }

        // Validar MVP
        if (predictions.pred_mvp_jugador.trim() !== '') {
            hasPrediction = true;
        }

        if (!hasPrediction) {
            newErrors.general = "Debes rellenar al menos una predicción";
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (validate()) {
            // Filtrar campos vacíos
            const cleanPredictions = {};
            Object.keys(predictions).forEach(key => {
                if (predictions[key] !== '') {
                    cleanPredictions[key] = predictions[key];
                }
            });
            onSubmit(cleanPredictions);
        }
    };

    const tabStyle = (tabName) => ({
        padding: '0.5rem 1rem',
        cursor: 'pointer',
        borderBottom: activeTab === tabName ? '2px solid var(--primary)' : '2px solid transparent',
        color: activeTab === tabName ? 'var(--primary)' : '#718096',
        fontWeight: activeTab === tabName ? 'bold' : 'normal',
        flex: 1,
        textAlign: 'center'
    });

    const inputGroupStyle = {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        marginBottom: '1rem'
    };

    const inputStyle = {
        width: '60px',
        padding: '0.5rem',
        borderRadius: '0.25rem',
        border: '1px solid #e2e8f0',
        textAlign: 'center'
    };

    return (
        <div className="advanced-betting-form" style={{ background: '#f7fafc', padding: '1rem', borderRadius: '0.5rem', marginTop: '1rem' }}>
            <div className="tabs" style={{ display: 'flex', marginBottom: '1rem', borderBottom: '1px solid #e2e8f0' }}>
                <div onClick={() => setActiveTab('resultado')} style={tabStyle('resultado')}>
                    Resultado
                </div>
                <div onClick={() => setActiveTab('stats')} style={tabStyle('stats')}>
                    {isBasketball ? 'Expulsiones' : 'Tarjetas'}
                </div>
                <div onClick={() => setActiveTab('mvp')} style={tabStyle('mvp')}>
                    MVP
                </div>
            </div>

            <form onSubmit={handleSubmit}>
                {activeTab === 'resultado' && (
                    <div className="tab-content">
                        <div style={{ textAlign: 'center', marginBottom: '1rem', fontSize: '0.9rem', color: '#718096' }}>
                            Predice el marcador exacto (10 pts) o solo el ganador (5 pts)
                        </div>
                        <div style={inputGroupStyle}>
                            <label>{match.equipo_local?.nombre}</label>
                            <input
                                type="number"
                                name="pred_goles_local"
                                value={predictions.pred_goles_local}
                                onChange={handleChange}
                                placeholder="0"
                                style={{ ...inputStyle, borderColor: errors.pred_goles_local ? 'red' : '#e2e8f0' }}
                                min="0"
                            />
                        </div>
                        {errors.pred_goles_local && <div style={{ color: 'red', fontSize: '0.8rem', textAlign: 'right' }}>{errors.pred_goles_local}</div>}

                        <div style={inputGroupStyle}>
                            <label>{match.equipo_visitante?.nombre}</label>
                            <input
                                type="number"
                                name="pred_goles_visitante"
                                value={predictions.pred_goles_visitante}
                                onChange={handleChange}
                                placeholder="0"
                                style={{ ...inputStyle, borderColor: errors.pred_goles_visitante ? 'red' : '#e2e8f0' }}
                                min="0"
                            />
                        </div>
                        {errors.pred_goles_visitante && <div style={{ color: 'red', fontSize: '0.8rem', textAlign: 'right' }}>{errors.pred_goles_visitante}</div>}
                    </div>
                )}

                {activeTab === 'stats' && (
                    <div className="tab-content">
                        <div style={{ textAlign: 'center', marginBottom: '1rem', fontSize: '0.9rem', color: '#718096' }}>
                            2 puntos por cada acierto exacto
                        </div>

                        {isFootball ? (
                            <>
                                <h4 style={{ fontSize: '0.9rem', marginBottom: '0.5rem', color: '#d69e2e' }}>Tarjetas Amarillas</h4>
                                <div style={inputGroupStyle}>
                                    <label>{match.equipo_local?.codigo || 'Local'}</label>
                                    <input
                                        type="number"
                                        name="pred_amarillas_local"
                                        value={predictions.pred_amarillas_local}
                                        onChange={handleChange}
                                        placeholder="0"
                                        style={inputStyle}
                                        min="0"
                                    />
                                    <label>{match.equipo_visitante?.codigo || 'Visitante'}</label>
                                    <input
                                        type="number"
                                        name="pred_amarillas_visitante"
                                        value={predictions.pred_amarillas_visitante}
                                        onChange={handleChange}
                                        placeholder="0"
                                        style={inputStyle}
                                        min="0"
                                    />
                                </div>
                                {errors.pred_amarillas_local && <div style={{ color: 'red', fontSize: '0.8rem' }}>{errors.pred_amarillas_local}</div>}

                                <h4 style={{ fontSize: '0.9rem', marginBottom: '0.5rem', marginTop: '1rem', color: '#e53e3e' }}>Tarjetas Rojas</h4>
                                <div style={inputGroupStyle}>
                                    <label>{match.equipo_local?.codigo || 'Local'}</label>
                                    <input
                                        type="number"
                                        name="pred_rojas_local"
                                        value={predictions.pred_rojas_local}
                                        onChange={handleChange}
                                        placeholder="0"
                                        style={inputStyle}
                                        min="0"
                                    />
                                    <label>{match.equipo_visitante?.codigo || 'Visitante'}</label>
                                    <input
                                        type="number"
                                        name="pred_rojas_visitante"
                                        value={predictions.pred_rojas_visitante}
                                        onChange={handleChange}
                                        placeholder="0"
                                        style={inputStyle}
                                        min="0"
                                    />
                                </div>
                                {errors.pred_rojas_local && <div style={{ color: 'red', fontSize: '0.8rem' }}>{errors.pred_rojas_local}</div>}
                            </>
                        ) : isBasketball ? (
                            <>
                                <h4 style={{ fontSize: '0.9rem', marginBottom: '0.5rem' }}>Expulsiones por Falta</h4>
                                <div style={inputGroupStyle}>
                                    <label>{match.equipo_local?.codigo || 'Local'}</label>
                                    <input
                                        type="number"
                                        name="pred_expulsiones_local"
                                        value={predictions.pred_expulsiones_local}
                                        onChange={handleChange}
                                        placeholder="0"
                                        style={inputStyle}
                                        min="0"
                                    />
                                    <label>{match.equipo_visitante?.codigo || 'Visitante'}</label>
                                    <input
                                        type="number"
                                        name="pred_expulsiones_visitante"
                                        value={predictions.pred_expulsiones_visitante}
                                        onChange={handleChange}
                                        placeholder="0"
                                        style={inputStyle}
                                        min="0"
                                    />
                                </div>
                                {errors.pred_expulsiones_local && <div style={{ color: 'red', fontSize: '0.8rem' }}>{errors.pred_expulsiones_local}</div>}
                            </>
                        ) : (
                            <div>No hay estadísticas disponibles para este deporte</div>
                        )}
                    </div>
                )}

                {activeTab === 'mvp' && (
                    <div className="tab-content">
                        <div style={{ textAlign: 'center', marginBottom: '1rem', fontSize: '0.9rem', color: '#718096' }}>
                            Adivina el MVP del partido (5 pts)
                        </div>
                        <input
                            type="text"
                            name="pred_mvp_jugador"
                            value={predictions.pred_mvp_jugador}
                            onChange={handleChange}
                            placeholder="Nombre del jugador"
                            style={{
                                width: '100%',
                                padding: '0.75rem',
                                borderRadius: '0.25rem',
                                border: '1px solid #e2e8f0',
                                marginBottom: '1rem'
                            }}
                        />
                    </div>
                )}

                {errors.general && (
                    <div style={{ color: '#c53030', background: '#fed7d7', padding: '0.5rem', borderRadius: '0.25rem', marginBottom: '1rem', fontSize: '0.9rem', textAlign: 'center' }}>
                        {errors.general}
                    </div>
                )}

                <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1.5rem' }}>
                    <button
                        type="button"
                        onClick={onCancel}
                        style={{
                            flex: 1,
                            padding: '0.75rem',
                            border: '1px solid #e2e8f0',
                            background: 'white',
                            borderRadius: '0.25rem',
                            cursor: 'pointer'
                        }}
                    >
                        Cancelar
                    </button>
                    <button
                        type="submit"
                        disabled={loading}
                        className="btn btn-primary"
                        style={{
                            flex: 1,
                            padding: '0.75rem',
                            borderRadius: '0.25rem',
                            cursor: loading ? 'not-allowed' : 'pointer',
                            opacity: loading ? 0.7 : 1
                        }}
                    >
                        {loading ? 'Enviando...' : 'Confirmar Apuesta'}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default AdvancedBettingForm;
