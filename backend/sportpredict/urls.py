from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

# Importar las vistas desde views.py
from . import views  # ← AÑADE ESTA LÍNEA

from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="SportPredict API",
      default_version='v1',
      description="API documentation for SportPredict",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

def home_page(request):
    return render(request, 'home.html', {
        'message': '🎉 SportPredict está funcionando!',
        'services': ['PostgreSQL', 'Redis', 'MongoDB', 'Neo4j']
    })

def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'service': 'SportPredict API',
        'version': '1.0'
    })

def services_status(request):
    return JsonResponse({
        'django': 'running',
        'postgresql': 'configured', 
        'redis': 'configured',
        'mongodb': 'configured',
        'neo4j': 'configured'
    })

def test_api(request):
    return JsonResponse({'message': '¡Backend Django funcionando correctamente con React!'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health'),
    path('status/', services_status, name='status'),
    path('', home_page, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)