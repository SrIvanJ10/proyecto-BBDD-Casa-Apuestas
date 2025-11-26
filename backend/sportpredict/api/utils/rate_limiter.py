"""
Rate Limiter usando Redis para controlar predicciones diarias
"""
from sportpredict.db.redis.sessions import SessionManager


class RateLimiter:
    """Rate limiter para predicciones usando Redis SessionManager"""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.session_manager = SessionManager()
        self.max_predictions_per_day = 10
    
    def can_make_prediction(self):
        """Verificar si el usuario puede hacer más predicciones hoy"""
        return self.session_manager.can_make_prediction(str(self.user_id))
    
    def record_prediction(self):
        """Registrar una nueva predicción"""
        return self.session_manager.increment_predictions(str(self.user_id))
    
    def get_remaining_predictions(self):
        """Obtener predicciones restantes para hoy"""
        return self.session_manager.get_remaining_predictions(str(self.user_id))
    
    def get_today_predictions(self):
        """Obtener número de predicciones hechas hoy"""
        return self.session_manager.get_today_predictions(str(self.user_id))
    
    def get_remaining_time(self):
        """Obtener tiempo restante hasta el reset (en segundos)"""
        # Calcular segundos hasta medianoche
        from datetime import datetime, timedelta
        now = datetime.now()
        tomorrow = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        remaining_seconds = int((tomorrow - now).total_seconds())
        return remaining_seconds
    
    def refund_prediction(self):
        """Devolver una predicción (cuando se elimina)"""
        # Decrementar el contador de predicciones
        session_data = self.session_manager.get_user_session(str(self.user_id))
        if session_data:
            current = int(session_data.get('predicciones_hoy', 0))
            if current > 0:
                session_data['predicciones_hoy'] = str(current - 1)
                self.session_manager._update_session(
                    f"SESSION:{self.user_id}", 
                    session_data
                )
                return True
        return False
