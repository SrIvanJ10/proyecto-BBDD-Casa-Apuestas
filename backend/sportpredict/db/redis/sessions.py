import redis
from datetime import datetime, date

class SessionManager:
    def __init__(self):
        self.redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
    
    def _reset_if_new_day(self, session_data: dict) -> dict:
        """Resetea predicciones_hoy si es un nuevo día basado en last_activity"""
        if not session_data:
            return session_data
            
        last_activity_str = session_data.get("last_activity")
        if not last_activity_str:
            # Si no hay last_activity, crear uno nuevo
            session_data["last_activity"] = datetime.now().isoformat()
            session_data["predicciones_hoy"] = "0"
            return session_data
        
        try:
            # Verificar si last_activity es de otro día
            last_activity_date = datetime.fromisoformat(last_activity_str).date()
            today = date.today()
            
            if last_activity_date < today:
                # ¡Es un nuevo día! Resetear contador
                session_data["predicciones_hoy"] = "0"
                session_data["last_activity"] = datetime.now().isoformat()
                
        except ValueError:
            # Si hay error en el formato, resetear por seguridad
            session_data["predicciones_hoy"] = "0"
            session_data["last_activity"] = datetime.now().isoformat()
        
        return session_data
    
    def _update_session(self, session_key: str, session_data: dict):
        """Guarda sesión y actualiza TTL"""
        self.redis_client.hmset(session_key, session_data)
        self.redis_client.expire(session_key, 86400)
    
    def create_user_session(self, user):
        """Crea una sesión de usuario en Redis"""
        session_key = f"SESSION:{user.id}"
        
        session_data = {
            "user_id": str(user.id),
            "username": user.username,
            "email": user.email,
            "puntos_totales": str(user.puntos_totales),
            "nivel_experto": str(user.nivel_experto),
            "predicciones_hoy": "0",
            "last_activity": datetime.now().isoformat()
        }
        
        self._update_session(session_key, session_data)
        return session_key
    
    def get_user_session(self, user_id):
        """Recupera la sesión de un usuario con reset automático diario"""
        session_key = f"SESSION:{user_id}"
        session_data = self.redis_client.hgetall(session_key)
        
        if session_data:
            # Verificar reset diario y actualizar last_activity
            session_data = self._reset_if_new_day(session_data)
            self._update_session(session_key, session_data)
        
        return session_data

    def refresh_session(self, user):
        """Actualiza datos de PostgreSQL con reset automático diario"""
        session_key = f"SESSION:{user.id}"
        
        # Obtener datos actuales con reset automático
        session_data = self.get_user_session(user.id)
        if not session_data:
            return self.create_user_session(user)
        
        # Actualizar datos de PostgreSQL (manteniendo predicciones_hoy y last_activity)
        session_data.update({
            "user_id": str(user.id),
            "username": user.username,
            "email": user.email,
            "puntos_totales": str(user.puntos_totales),
            "nivel_experto": str(user.nivel_experto)
        })
        
        self._update_session(session_key, session_data)
        return session_data
     
    def increment_predictions(self, user_id):
        """Incrementa el contador de predicciones de hoy con verificación de límite"""
        session_key = f"SESSION:{user_id}"
        
        # Obtener sesión (ya hace reset automático si es nuevo día)
        session_data = self.get_user_session(user_id)
        if not session_data:
            raise Exception("Sesión no encontrada")
        
        # Incrementar
        new_value = str(int(session_data["predicciones_hoy"]) + 1)
        session_data["predicciones_hoy"] = new_value
        session_data["last_activity"] = datetime.now().isoformat()
        
        self._update_session(session_key, session_data)
        return int(new_value)
    
    # RATE LIMITING FUNCTIONS
    
    def can_make_prediction(self, user_id: str) -> bool:
        """Verifica si el usuario puede hacer más predicciones hoy (máximo 10)"""
        session_data = self.get_user_session(user_id)
        if not session_data:
            return False
        
        predicciones_hoy = int(session_data.get("predicciones_hoy", 0))
        return predicciones_hoy < 10
    
    def get_today_predictions(self, user_id: str) -> int:
        """Obtiene el número de predicciones hechas hoy"""
        session_data = self.get_user_session(user_id)
        if not session_data:
            return 0
        
        return int(session_data.get("predicciones_hoy", 0))
    
    def get_remaining_predictions(self, user_id: str) -> int:
        """Obtiene cuántas predicciones le quedan hoy"""
        session_data = self.get_user_session(user_id)
        if not session_data:
            return 0
        
        predicciones_hoy = int(session_data.get("predicciones_hoy", 0))
        return max(0, 10 - predicciones_hoy)