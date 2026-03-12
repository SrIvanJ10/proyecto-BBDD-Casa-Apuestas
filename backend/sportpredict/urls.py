from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from . import views


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
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
