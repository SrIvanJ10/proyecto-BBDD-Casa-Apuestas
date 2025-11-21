import redis
import random
import string
from datetime import datetime, timedelta

class OTPManager:
    def __init__(self):
        self.redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
        self.otp_length = 6
        self.otp_ttl = 600  # 10 minutos en segundos
    
    def _generate_otp_code(self) -> str:
        """Genera un código OTP de 6 dígitos"""
        return ''.join(random.choices(string.digits, k=self.otp_length))
    
    def generate_otp(self, email: str) -> str:
        """
        Genera y almacena un OTP para un email
        Returns: código OTP para enviar por email
        """
        # Limpiar OTPs anteriores para este email
        self.redis_client.delete(f"otp:{email}")
        
        # Generar nuevo código
        otp_code = self._generate_otp_code()
        
        # Almacenar en Redis con TTL de 10 minutos
        otp_key = f"otp:{email}"
        self.redis_client.setex(otp_key, self.otp_ttl, otp_code)
        
        return otp_code
    
    def verify_otp(self, email: str, code: str) -> bool:
        """
        Verifica si un código OTP es válido para un email
        Si es válido, elimina el OTP para evitar reuso
        """
        otp_key = f"otp:{email}"
        stored_code = self.redis_client.get(otp_key)
        
        if not stored_code:
            return False  # No existe OTP o expiró
        
        if stored_code == code:
            # Código válido - eliminar para evitar reuso
            self.redis_client.delete(otp_key)
            return True
        
        return False
    
    def is_otp_active(self, email: str) -> bool:
        """Verifica si hay un OTP activo para un email"""
        return self.redis_client.exists(f"otp:{email}") == 1
    
    def get_remaining_time(self, email: str) -> int:
        """Obtiene segundos restantes para que expire el OTP"""
        return self.redis_client.ttl(f"otp:{email}")