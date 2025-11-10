import redis
from datetime import datetime

class SessionManager:
    def __init__(self):
        self.redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
    
    def create_user_session(self, user):
        """Crea una sesión de usuario en Redis"""
        session_key = f"SESSION:{user.id}"
        
        session_data = {
            "user_id": str(user.id),
            "username": user.username,
            "email": user.email,
            "puntos_totales": str(user.puntos_totales),
            "nivel_experto": str(user.nivel_experto),
            "predicciones_hoy": "0"
        }
        
        self.redis_client.hmset(session_key, session_data)
        self.redis_client.expire(session_key, 86400)
        
        return session_key
    
    def get_user_session(self, user_id):
        """Recupera la sesión de un usuario"""
        session_key = f"SESSION:{user_id}"
        return self.redis_client.hgetall(session_key)

    def refresh_session(self, user):
        """
        Actualiza solo los datos de PostgreSQL en Redis
        Mantiene los datos propios de Redis (predicciones_hoy, etc.)
        """

        session_key = f"SESSION:{user.id}"
        
        # Mantener los datos propios de Redis
        predicciones_hoy = self.redis_client.hget(session_key, "predicciones_hoy") or "0"
        last_activity = self.redis_client.hget(session_key, "last_activity") or datetime.now().isoformat()
        
        session_data = {
            # Datos de PostgreSQL (actualizados)
            "user_id": str(user.id),
            "username": user.username,
            "email": user.email,
            "puntos_totales": str(user.puntos_totales),
            "nivel_experto": str(user.nivel_experto),
            # Datos propios de Redis (mantenidos)
            "last_activity": last_activity,
            "predicciones_hoy": predicciones_hoy
        }
        
        self.redis_client.hmset(session_key, session_data)
        return session_data
     
    def increment_predictions(self, user_id):
        """Incrementa SOLO el contador de predicciones de hoy"""
        
        session_key = f"SESSION:{user_id}"
        
        current = self.redis_client.hget(session_key, "predicciones_hoy") or "0"
        new_value = str(int(current) + 1)
        
        self.redis_client.hset(session_key, "predicciones_hoy", new_value)
        return new_value