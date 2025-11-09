from django.urls import path
from . import views

app_name = 'equipos'

urlpatterns = [
    # Listados
    path('', views.lista_equipos, name='lista_equipos'),
    path('por-deporte/<int:deporte_id>/', views.equipos_por_deporte, name='equipos_por_deporte'),
    
    # Detalles
    path('<int:equipo_id>/', views.detalle_equipo, name='detalle_equipo'),
    path('<slug:equipo_slug>/', views.detalle_equipo_slug, name='detalle_equipo_slug'),
    
    # Partidos del equipo
    path('<int:equipo_id>/partidos/', views.partidos_por_equipo, name='partidos_por_equipo'),
    path('<int:equipo_id>/partidos/proximos/', views.partidos_proximos_equipo, name='partidos_proximos_equipo'),
    path('<int:equipo_id>/partidos/pasados/', views.partidos_pasados_equipo, name='partidos_pasados_equipo'),
    path('<int:equipo_id>/partidos/en-vivo/', views.partidos_en_vivo_equipo, name='partidos_en_vivo_equipo'),
    
    # Estadísticas
    path('<int:equipo_id>/estadisticas/', views.estadisticas_equipo, name='estadisticas_equipo'),
    path('<int:equipo_id>/rivalidades/', views.rivalidades_equipo, name='rivalidades_equipo'),
    
    # Gestión (solo staff)
    path('crear/', views.crear_equipo, name='crear_equipo'),
    path('<int:equipo_id>/editar/', views.editar_equipo, name='editar_equipo'),
    path('<int:equipo_id>/eliminar/', views.eliminar_equipo, name='eliminar_equipo'),
    
    # APIs
    path('api/equipos/', views.api_equipos, name='api_equipos'),
    path('api/<int:equipo_id>/partidos-proximos/', views.api_partidos_proximos_equipo, name='api_partidos_proximos_equipo'),
]
