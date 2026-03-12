"""
Utilidades de autenticación JWT para SportPredict
"""
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from sportpredict.models import Usuario


SECRET_KEY = settings.SECRET_KEY
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_DAYS = 7


def generate_jwt_token(user):
    """Generar token JWT para un usuario"""
    payload = {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(days=JWT_EXPIRATION_DAYS),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def decode_jwt_token(token):
    """Decodificar y validar token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token expirado')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Token inválido')


class JWTAuthentication(BaseAuthentication):
    """Clase de autenticación JWT para DRF"""
    
    def authenticate(self, request):
        # Obtener token del header Authorization
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        
        try:
            payload = decode_jwt_token(token)
            user = Usuario.objects.get(id=payload['user_id'])
            return (user, token)
        except Usuario.DoesNotExist:
            raise AuthenticationFailed('Usuario no encontrado')
        except Exception as e:
            raise AuthenticationFailed(f'Error de autenticación: {str(e)}')
    
    def authenticate_header(self, request):
        return 'Bearer'


def get_user_from_token(token):
    """Obtener usuario desde un token JWT"""
    try:
        payload = decode_jwt_token(token)
        user = Usuario.objects.get(id=payload['user_id'])
        return user
    except Usuario.DoesNotExist:
        return None
    except Exception:
        return None
