from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import views

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
    path('api/test/', test_api, name='api_test'),

    # Todas las rutas API delegadas al módulo api/
    path('api/', include('sportpredict.api.urls')),

    # Sync manual de Neo4j
    path('trigger-sync/', views.trigger_sync, name='trigger_sync'),

    # Documentación Swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
