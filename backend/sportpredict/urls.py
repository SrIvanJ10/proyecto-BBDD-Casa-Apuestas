from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

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
    #path('usuarios/', include('sportpredict.usuarios.urls')),
    #path('predicciones/', include('sportpredict.predicciones.urls')),
    #path('deportes/', include('sportpredict.deportes.urls')),
    #path('equipos/', include('sportpredict.equipos.urls')),
    #path('partidos/', include('sportpredict.partidos.urls')),
    
    # Página principal
    #path('', include('sportpredict.predicciones.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
