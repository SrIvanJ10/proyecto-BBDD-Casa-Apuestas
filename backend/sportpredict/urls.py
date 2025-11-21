from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

from sportpredict.api.views import (
    api_partidos_proximos, lista_partidos, detalle_partido, 
    leaderboard, estadisticas_globales, lista_deportes, 
    detalle_deporte, lista_equipos, detalle_equipo, 
    hacer_prediccion, mis_predicciones, eliminar_prediccion,
    dashboard, api_estadisticas_usuario, recomendaciones,
    inicio
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
    
    path('api/partidos/proximos/', api_partidos_proximos, name='api_partidos_proximos'),
    path('api/partidos/', lista_partidos, name='api_lista_partidos'),
    path('api/partidos/<int:partido_id>/', detalle_partido, name='api_detalle_partido'),
    path('api/leaderboard/', leaderboard, name='api_leaderboard'),
    path('api/estadisticas-globales/', estadisticas_globales, name='api_estadisticas_globales'),
    path('api/deportes/', lista_deportes, name='api_lista_deportes'),
    path('api/deportes/<int:deporte_id>/', detalle_deporte, name='api_detalle_deporte'),
    path('api/equipos/', lista_equipos, name='api_lista_equipos'),
    path('api/equipos/<int:equipo_id>/', detalle_equipo, name='api_detalle_equipo'),
    path('api/predicciones/crear/<int:partido_id>/', hacer_prediccion, name='api_crear_prediccion'),
    path('api/predicciones/mis/', mis_predicciones, name='api_mis_predicciones'),
    path('api/predicciones/<int:prediccion_id>/eliminar/', eliminar_prediccion, name='api_eliminar_prediccion'),
    path('api/usuario/dashboard/', dashboard, name='api_dashboard'),
    path('api/usuario/estadisticas/', api_estadisticas_usuario, name='api_estadisticas_usuario'),
    path('api/recomendaciones/', recomendaciones, name='api_recomendaciones'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)