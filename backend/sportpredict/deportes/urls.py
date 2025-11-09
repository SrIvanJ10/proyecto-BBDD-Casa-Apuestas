from django.urls import path
from . import views

app_name = 'deportes'

urlpatterns = [
    # Listados
    path('', views.lista_deportes, name='lista_deportes'),
    path('activos/', views.deportes_activos, name='deportes_activos'),
    
    # Detalles
    path('<int:deporte_id>/', views.detalle_deporte, name='detalle_deporte'),
    path('<slug:deporte_slug>/', views.detalle_deporte_slug, name='detalle_deporte_slug'),
    
    # Relaciones
    path('<int:deporte_id>/equipos/', views.equipos_por_deporte, name='equipos_por_deporte'),
    path('<int:deporte_id>/partidos/', views.partidos_por_deporte, name='partidos_por_deporte'),
    path('<int:deporte_id>/partidos/proximos/', views.partidos_proximos_por_deporte, name='partidos_proximos_por_deporte'),
    path('<int:deporte_id>/partidos/pasados/', views.partidos_pasados_por_deporte, name='partidos_pasados_por_deporte'),
    
    # Gestión (solo staff)
    path('crear/', views.crear_deporte, name='crear_deporte'),
    path('<int:deporte_id>/editar/', views.editar_deporte, name='editar_deporte'),
    path('<int:deporte_id>/eliminar/', views.eliminar_deporte, name='eliminar_deporte'),
    
    # APIs
    path('api/deportes/', views.api_deportes, name='api_deportes'),
    path('api/<int:deporte_id>/estadisticas/', views.api_estadisticas_deporte, name='api_estadisticas_deporte'),
]
