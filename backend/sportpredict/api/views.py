from rest_framework.decorators import api_view
from rest_framework.response import Response

try:
    from .mongo_client import mongo_db, log_user_activity
except ImportError:
    from mongo_client import mongo_db, log_user_activity

@api_view(['GET'])
def test_api(request):
    """
    Endpoint de prueba para verificar que el backend está funcionando
    GET /api/test/
    """
    # ✅ OPCIONAL: Registrar actividad si el usuario está autenticado
    if request.user.is_authenticated:
        try:
            log_user_activity(
                user_id=request.user.id,
                action='test_api_accessed',
                metadata={'path': request.path}
            )
        except Exception as e:
            # Si falla el logging, continuamos sin romper el endpoint
            print(f"⚠️ Error registrando actividad: {e}")
    
    return Response({
        'message': '¡Backend Django funcionando correctamente! 🚀',
        'status': 'active',
        'endpoints_available': [
            'GET /api/test/',
            'POST /api/auth/register/',
            'POST /api/auth/verify-otp/',
            'POST /api/auth/login/',
            'POST /api/auth/logout/',
            'POST /api/auth/forgot-password/',
            'POST /api/auth/reset-password/',
            'GET /api/matches/',
            'GET /api/matches/upcoming/',
            'GET /api/matches/live/',
            'GET /api/matches/finished/',
            'GET /api/predictions/',
            'POST /api/predictions/create/',
            'GET /api/users/profile/',
            'GET /api/users/leaderboard/',
            'GET /api/analytics/dashboard/'
        ],
        'project': 'SportPredict',
        'version': '1.0.0',
        'database_status': 'MongoDB integrado'  # ✅ Confirmación de la integración
    })
