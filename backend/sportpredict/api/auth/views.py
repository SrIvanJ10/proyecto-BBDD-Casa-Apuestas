"""
API de Autenticación - Usando PostgreSQL + Redis OTP + JWT
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.db import IntegrityError

from sportpredict.models import Usuario
from sportpredict.serializers import UsuarioSerializer, UsuarioRegistroSerializer
from sportpredict.db.redis.otp import OTPManager
from sportpredict.db.redis.sessions import SessionManager
from sportpredict.db.mongodb.analytics import AnalyticsManager
from ..utils.authentication import generate_jwt_token


from sportpredict.db.redis.rate_limit import LoginRateLimiter

# Inicializar managers
otp_manager = OTPManager()
session_manager = SessionManager()
analytics_manager = AnalyticsManager()
rate_limiter = LoginRateLimiter()


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Registrar nuevo usuario y enviar OTP
    POST /api/auth/register/
    Body: {email, username, password, first_name, last_name}
    """
    try:
        serializer = UsuarioRegistroSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'error': 'Datos inválidos', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar si el email ya existe
        email = serializer.validated_data['email']
        if Usuario.objects.filter(email=email).exists():
            return Response(
                {'error': 'El email ya está registrado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar si el username ya existe
        username = serializer.validated_data['username']
        if Usuario.objects.filter(username=username).exists():
            return Response(
                {'error': 'El username ya está en uso'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Crear usuario (inactivo hasta verificar OTP)
        user = serializer.save()
        user.is_active = False  # Desactivar hasta verificar OTP
        user.save()
        
        # Generar y guardar OTP en Redis
        otp_code = otp_manager.generate_otp(email)
        
        # Log en MongoDB
        analytics_manager.registrar_actividad_usuario(
            user_id=user.id,
            action='user_registered',
            metadata={
                'email': email,
                'username': username
            }
        )
        
        # En producción, aquí enviarías el OTP por email
        # Por ahora lo mostramos en la respuesta (solo desarrollo)
        return Response({
            'message': 'Usuario registrado. Verifica tu email para el código OTP.',
            'user_id': user.id,
            'email': email,
            'otp_code': otp_code,  # SOLO PARA DESARROLLO - Eliminar en producción
            'otp_expires_in': otp_manager.otp_ttl
        }, status=status.HTTP_201_CREATED)
        
    except IntegrityError as e:
        return Response(
            {'error': f'Error de integridad: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'Error en registro: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    """
    Verificar OTP y activar usuario
    POST /api/auth/verify-otp/
    Body: {email, otp}
    """
    try:
        email = request.data.get('email')
        otp = request.data.get('otp')
        
        if not email or not otp:
            return Response(
                {'error': 'Email y OTP son requeridos'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar OTP en Redis
        if not otp_manager.verify_otp(email, otp):
            return Response(
                {'error': 'OTP inválido o expirado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Buscar usuario y activarlo
        try:
            user = Usuario.objects.get(email=email)
            user.is_active = True
            user.save()
        except Usuario.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Generar token JWT
        token = generate_jwt_token(user)
        
        # Crear sesión en Redis
        session_manager.create_user_session(user)
        
        # Log en MongoDB
        analytics_manager.registrar_actividad_usuario(
            user_id=user.id,
            action='otp_verified',
            metadata={'email': email}
        )
        
        # Serializar usuario
        user_serializer = UsuarioSerializer(user)
        
        return Response({
            'message': 'Email verificado exitosamente',
            'token': token,
            'user': user_serializer.data
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error verificando OTP: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Login de usuario con email/username y password
    POST /api/auth/login/
    Body: {email_or_username, password}
    """
    try:
        email_or_username = request.data.get('email_or_username') or request.data.get('email') or request.data.get('username')
        password = request.data.get('password')
        
        if not email_or_username or not password:
            return Response(
                {'error': 'Email/username y password son requeridos'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Verificar si el usuario está bloqueado por demasiados intentos fallidos
        if rate_limiter.is_locked(email_or_username):
            return Response(
                {'error': 'Fallaste demasiado la contraseña demasiadas veces vuelve a intentarlo dentro de 1 hora'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Buscar usuario por email o username (case-insensitive)
        user = None
        if '@' in email_or_username:
            try:
                user = Usuario.objects.get(email__iexact=email_or_username)
            except Usuario.DoesNotExist:
                pass
        else:
            try:
                user = Usuario.objects.get(username__iexact=email_or_username)
            except Usuario.DoesNotExist:
                pass
        
        if not user:
            # Registrar intento fallido
            rate_limiter.increment_attempts(email_or_username)
            return Response(
                {'error': 'Credenciales inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Verificar password
        if not user.check_password(password):
            # Registrar intento fallido
            rate_limiter.increment_attempts(email_or_username)
            return Response(
                {'error': 'Credenciales inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Verificar que el usuario esté activo
        if not user.is_active:
            return Response(
                {'error': 'Usuario no activado. Verifica tu email.'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        # Login exitoso - resetear contador de intentos
        rate_limiter.reset_attempts(email_or_username)
        
        # Generar token JWT
        token = generate_jwt_token(user)
        
        # Actualizar/crear sesión en Redis
        session_manager.refresh_session(user)
        
        # Log en MongoDB
        analytics_manager.registrar_actividad_usuario(
            user_id=user.id,
            action='user_logged_in',
            metadata={
                'email': user.email,
                'login_method': 'password'
            }
        )
        
        # Serializar usuario
        user_serializer = UsuarioSerializer(user)
        
        return Response({
            'message': 'Login exitoso',
            'token': token,
            'user': user_serializer.data
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error en login: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Logout de usuario
    POST /api/auth/logout/
    Headers: Authorization: Bearer <token>
    """
    try:
        user = request.user
        
        # Log en MongoDB
        analytics_manager.registrar_actividad_usuario(
            user_id=user.id,
            action='user_logged_out',
            metadata={}
        )
        
        # En producción, aquí invalidarías el token en Redis
        # Por ahora solo registramos la actividad
        
        return Response({
            'message': 'Logout exitoso'
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error en logout: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    """
    Solicitar restablecimiento de contraseña
    POST /api/auth/forgot-password/
    Body: {email}
    """
    try:
        email = request.data.get('email')
        
        if not email:
            return Response(
                {'error': 'Email es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar si el usuario existe
        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            # Por seguridad, no revelamos si el email existe o no
            return Response({
                'message': 'Si el email existe, se ha enviado un código de verificación'
            })
        
        # Generar OTP para restablecimiento
        otp_code = otp_manager.generate_otp(email)
        
        # Log en MongoDB
        analytics_manager.registrar_actividad_usuario(
            user_id=user.id,
            action='password_reset_requested',
            metadata={'email': email}
        )
        
        # En producción, enviarías el OTP por email
        return Response({
            'message': 'Si el email existe, se ha enviado un código de verificación',
            'email': email,
            'otp_code': otp_code,  # SOLO PARA DESARROLLO
            'otp_expires_in': otp_manager.otp_ttl
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error en forgot-password: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    """
    Restablecer contraseña con OTP
    POST /api/auth/reset-password/
    Body: {email, otp, new_password}
    """
    try:
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')
        
        if not all([email, otp, new_password]):
            return Response(
                {'error': 'Email, OTP y nueva contraseña son requeridos'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validar longitud de contraseña
        if len(new_password) < 8:
            return Response(
                {'error': 'La contraseña debe tener al menos 8 caracteres'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar OTP
        if not otp_manager.verify_otp(email, otp):
            return Response(
                {'error': 'OTP inválido o expirado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Buscar usuario y cambiar contraseña
        try:
            user = Usuario.objects.get(email=email)
            user.set_password(new_password)
            user.save()
        except Usuario.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Log en MongoDB
        analytics_manager.registrar_actividad_usuario(
            user_id=user.id,
            action='password_reset_completed',
            metadata={'email': email}
        )
        
        return Response({
            'message': 'Contraseña restablecida exitosamente'
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error en reset-password: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
