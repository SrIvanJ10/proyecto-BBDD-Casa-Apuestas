"""
Sistema de puntuación para predicciones avanzadas
"""

def calcular_puntos_prediccion(prediccion, partido):
    """
    Calcula puntos solo para las categorías que el usuario predijo
    
    Sistema de puntos:
    - Resultado exacto: 10 puntos
    - Solo ganador correcto: 5 puntos
    - Cada tarjeta/expulsión exacta: 2 puntos
    - MVP correcto: 5 puntos
    
    Args:
        prediccion (Prediccion): Objeto de predicción del usuario
        partido (Partido): Objeto de partido con resultados reales
    
    Returns:
        dict: Puntos por categoría y total
    """
    puntos = {
        'resultado': 0,
        'tarjetas': 0,
        'mvp': 0,
        'total': 0
    }
    
    # RESULTADO EXACTO
    if prediccion.pred_goles_local is not None and prediccion.pred_goles_visitante is not None:
        if partido.goles_local is not None and partido.goles_visitante is not None:
            # Resultado exacto: 10 puntos
            if (prediccion.pred_goles_local == partido.goles_local and 
                prediccion.pred_goles_visitante == partido.goles_visitante):
                puntos['resultado'] = 10
            # Solo ganador correcto (sin exacto): 5 puntos
            elif ganador_correcto(prediccion, partido):
                puntos['resultado'] = 5
    
    # TARJETAS AMARILLAS - FÚTBOL (2 puntos cada acierto)
    if prediccion.pred_amarillas_local is not None and partido.amarillas_local is not None:
        if prediccion.pred_amarillas_local == partido.amarillas_local:
            puntos['tarjetas'] += 2
    
    if prediccion.pred_amarillas_visitante is not None and partido.amarillas_visitante is not None:
        if prediccion.pred_amarillas_visitante == partido.amarillas_visitante:
            puntos['tarjetas'] += 2
    
    # TARJETAS ROJAS - FÚTBOL (2 puntos cada acierto)
    if prediccion.pred_rojas_local is not None and partido.rojas_local is not None:
        if prediccion.pred_rojas_local == partido.rojas_local:
            puntos['tarjetas'] += 2
    
    if prediccion.pred_rojas_visitante is not None and partido.rojas_visitante is not None:
        if prediccion.pred_rojas_visitante == partido.rojas_visitante:
            puntos['tarjetas'] += 2
    
    # EXPULSIONES - BALONCESTO (2 puntos cada acierto)
    if prediccion.pred_expulsiones_local is not None and partido.expulsiones_local is not None:
        if prediccion.pred_expulsiones_local == partido.expulsiones_local:
            puntos['tarjetas'] += 2
    
    if prediccion.pred_expulsiones_visitante is not None and partido.expulsiones_visitante is not None:
        if prediccion.pred_expulsiones_visitante == partido.expulsiones_visitante:
            puntos['tarjetas'] += 2
    
    # MVP (5 puntos)
    if prediccion.pred_mvp_jugador and partido.mvp_jugador:
        # Comparación case-insensitive y normalizada
        pred_mvp = prediccion.pred_mvp_jugador.strip().lower()
        real_mvp = partido.mvp_jugador.strip().lower()
        if pred_mvp == real_mvp:
            puntos['mvp'] = 5
    
    # TOTAL
    puntos['total'] = puntos['resultado'] + puntos['tarjetas'] + puntos['mvp']
    
    return puntos


def ganador_correcto(prediccion, partido):
    """
    Verifica si el usuario acertó el ganador (sin importar resultado exacto)
    
    Returns:
        bool: True si acertó el ganador o empate
    """
    pred_local = prediccion.pred_goles_local
    pred_visitante = prediccion.pred_goles_visitante
    real_local = partido.goles_local
    real_visitante = partido.goles_visitante
    
    # Predicción: local gana
    if pred_local > pred_visitante and real_local > real_visitante:
        return True
    
    # Predicción: visitante gana
    if pred_local < pred_visitante and real_local < real_visitante:
        return True
    
    # Predicción: empate
    if pred_local == pred_visitante and real_local == real_visitante:
        return True
    
    return False


def evaluar_prediccion(prediccion, partido):
    """
    Evalúa una predicción y actualiza sus puntos
    
    Args:
        prediccion (Prediccion): Predicción a evaluar
        partido (Partido): Partido con resultados reales
    
    Returns:
        Prediccion: Predicción actualizada con puntos
    """
    if prediccion.evaluada:
        return prediccion  # Ya fue evaluada
    
    puntos = calcular_puntos_prediccion(prediccion, partido)
    
    prediccion.puntos_resultado = puntos['resultado']
    prediccion.puntos_tarjetas = puntos['tarjetas']
    prediccion.puntos_mvp = puntos['mvp']
    prediccion.puntos_totales = puntos['total']
    prediccion.evaluada = True
    
    # Actualizar campo legacy
    prediccion.correcta = (puntos['total'] > 0)
    
    prediccion.save()
    
    # Actualizar puntos del usuario
    usuario = prediccion.usuario
    usuario.puntos_totales += puntos['total']
    usuario.save()
    
    return prediccion


def evaluar_todas_predicciones_partido(partido):
    """
    Evalúa todas las predicciones de un partido
    
    Args:
        partido (Partido): Partido finalizado
    
    Returns:
        int: Número de predicciones evaluadas
    """
    from sportpredict.models import Prediccion
    
    predicciones = Prediccion.objects.filter(
        partido=partido,
        evaluada=False
    )
    
    count = 0
    for pred in predicciones:
        evaluar_prediccion(pred, partido)
        count += 1
    
    return count
