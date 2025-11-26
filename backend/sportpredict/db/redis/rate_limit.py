import redis
from django.conf import settings

class LoginRateLimiter:
    def __init__(self):
        # Usar la misma configuración de conexión que OTPManager
        self.redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
        self.max_attempts = 5
        self.lockout_time = 3600  # 1 hora en segundos
        self.attempt_ttl = 600    # 10 minutos para resetear contador si no hay más fallos

    def _get_key(self, identifier: str) -> str:
        """Genera la clave para Redis basada en el identificador (email/username)"""
        return f"login_attempts:{identifier.lower()}"

    def increment_attempts(self, identifier: str) -> int:
        """
        Incrementa el contador de intentos fallidos.
        Si llega al límite, establece el TTL de bloqueo (1 hora).
        Retorna el número actual de intentos.
        """
        key = self._get_key(identifier)
        attempts = self.redis_client.incr(key)
        
        if attempts == 1:
            # Primer intento fallido, establecer TTL corto
            self.redis_client.expire(key, self.attempt_ttl)
        elif attempts >= self.max_attempts:
            # Límite alcanzado, establecer TTL de bloqueo (si no estaba ya bloqueado)
            # Solo actualizamos el TTL si acabamos de cruzar el umbral
            if attempts == self.max_attempts:
                self.redis_client.expire(key, self.lockout_time)
        
        return attempts

    def is_locked(self, identifier: str) -> bool:
        """Verifica si el usuario está bloqueado"""
        key = self._get_key(identifier)
        attempts = self.redis_client.get(key)
        
        if attempts and int(attempts) >= self.max_attempts:
            return True
        return False

    def reset_attempts(self, identifier: str):
        """Resetea el contador de intentos (login exitoso)"""
        key = self._get_key(identifier)
        self.redis_client.delete(key)

    def get_remaining_time(self, identifier: str) -> int:
        """Obtiene el tiempo restante de bloqueo en segundos"""
        key = self._get_key(identifier)
        ttl = self.redis_client.ttl(key)
        return max(0, ttl)
