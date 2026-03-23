from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count, Sum
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
import re
import json

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
    if request.user.is_authenticated and log_user_activity:
        try:
            log_user_activity(
                user_id=request.user.id,
                action='test_api_accessed',
                metadata={'path': request.path}
            )
        except Exception:
            pass

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
    })
