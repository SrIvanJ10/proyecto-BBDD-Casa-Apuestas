from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.shortcuts import render

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
    path('', home_page, name='home'),
    path('health/', health_check, name='health'),
    path('status/', services_status, name='status'),
    path('api/test/', test_api),
]