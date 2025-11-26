import api from './api';

/**
 * Crear nueva predicción para un partido
 * @param {number} partidoId - ID del partido
 * @param {string} prediccion - Predicción en formato "X-Y" (ej: "2-1", "1-0")
 */
/**
 * Crear nueva predicción para un partido
 * @param {number} partidoId - ID del partido
 * @param {string|object} predictionData - Predicción en formato "X-Y" o objeto con campos avanzados
 */
export const makePrediction = async (partidoId, predictionData) => {
    let payload = { partido_id: partidoId };

    if (typeof predictionData === 'string') {
        // Legacy format
        payload.prediccion = predictionData;
    } else {
        // Advanced format
        payload = { ...payload, ...predictionData };
    }

    const response = await api.post('/predictions/create/', payload);
    return response.data;
};

/**
 * Obtener predicciones del usuario
 */
export const getUserPredictions = async () => {
    const response = await api.get('/predictions/');
    return response.data;
};

/**
 * Obtener estadísticas de predicciones del usuario
 */
export const getPredictionStats = async () => {
    const response = await api.get('/predictions/stats/');
    return response.data;
};

/**
 * Verificar si el usuario puede predecir en un partido específico
 * @param {number} matchId - ID del partido
 */
export const checkCanPredict = async (matchId) => {
    const response = await api.get(`/predictions/match/${matchId}/`);
    return response.data;
};

export default {
    makePrediction,
    getUserPredictions,
    getPredictionStats,
    checkCanPredict
};
