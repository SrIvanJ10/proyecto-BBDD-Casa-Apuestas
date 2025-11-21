from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

<<<<<<< HEAD
<<<<<<< HEAD
from sportpredict.api.views import (
    api_partidos_proximos, lista_partidos, detalle_partido, 
    leaderboard, estadisticas_globales, lista_deportes, 
    detalle_deporte, lista_equipos, detalle_equipo, 
    hacer_prediccion, mis_predicciones, eliminar_prediccion,
    dashboard, api_estadisticas_usuario, recomendaciones,
    inicio
)
=======
# Importar las vistas desde views.py
from . import views  # ← AÑADE ESTA LÍNEA
>>>>>>> 4e7fe49 (crear rama backend)

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
=======
# Importar las vistas desde views.py
from . import views  # ← AÑADE ESTA LÍNEA
>>>>>>> 4e7fe49 (crear rama backend)

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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
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
=======
    
=======
    
>>>>>>> 4e7fe49 (crear rama backend)
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
<<<<<<< HEAD
>>>>>>> 4e7fe49 (crear rama backend)
=======
    path('api/', include('sportpredict.api.urls')),  # ← Ruta completa del módulo
    path('trigger-sync/', views.trigger_sync, name='trigger_sync'),
    
    # Swagger Documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
>>>>>>> d381094 (v0.14)
=======
>>>>>>> 4e7fe49 (crear rama backend)
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)