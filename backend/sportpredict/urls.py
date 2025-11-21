from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

# Importar las vistas desde views.py
from . import views  # ← AÑADE ESTA LÍNEA

def home_page(request):
    """Página de inicio simple"""
    return render(request, 'home.html', {
        'message': '🎉 SportPredict está funcionando!',
        'services': ['PostgreSQL', 'Redis', 'MongoDB', 'Neo4j']
    })

def health_check(request):
    """Endpoint de salud para verificar servicios"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'SportPredict API',
        'version': '1.0'
    })

def services_status(request):
    """Status de conexión a bases de datos"""
    status = {
        'django': 'running',
        'postgresql': 'configured', 
        'redis': 'configured',
        'mongodb': 'configured',
        'neo4j': 'configured'
    }
    return JsonResponse(status)

def test_api(request):
    """API test para React"""
    return JsonResponse({'message': '¡Backend Django funcionando correctamente con React!'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health'),
    path('status/', services_status, name='status'),
    path('', home_page, name='home'),
    
    # ========== NUEVAS RUTAS API ==========
    
    # APIs públicas - Partidos
    path('api/partidos/proximos/', views.api_partidos_proximos, name='api_partidos_proximos'),
    path('api/partidos/', views.lista_partidos, name='api_lista_partidos'),
    path('api/partidos/<int:partido_id>/', views.detalle_partido, name='api_detalle_partido'),
    
    # APIs públicas - Leaderboard y estadísticas
    path('api/leaderboard/', views.leaderboard, name='api_leaderboard'),
    path('api/estadisticas-globales/', views.estadisticas_globales, name='api_estadisticas_globales'),
    
    # APIs públicas - Deportes y equipos
    path('api/deportes/', views.lista_deportes, name='api_lista_deportes'),
    path('api/deportes/<int:deporte_id>/', views.detalle_deporte, name='api_detalle_deporte'),
    path('api/equipos/', views.lista_equipos, name='api_lista_equipos'),
    path('api/equipos/<int:equipo_id>/', views.detalle_equipo, name='api_detalle_equipo'),
    
    # APIs autenticadas - Predicciones
    path('api/predicciones/crear/<int:partido_id>/', views.hacer_prediccion, name='api_crear_prediccion'),
    path('api/predicciones/mis/', views.mis_predicciones, name='api_mis_predicciones'),
    path('api/predicciones/<int:prediccion_id>/eliminar/', views.eliminar_prediccion, name='api_eliminar_prediccion'),
    
    # APIs autenticadas - Usuario
    path('api/usuario/dashboard/', views.dashboard, name='api_dashboard'),
    path('api/usuario/estadisticas/', views.api_estadisticas_usuario, name='api_estadisticas_usuario'),
    path('api/recomendaciones/', views.recomendaciones, name='api_recomendaciones'),
    
    # ========== FIN NUEVAS RUTAS ==========
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
