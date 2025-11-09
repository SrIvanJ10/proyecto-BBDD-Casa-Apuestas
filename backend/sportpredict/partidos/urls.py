from django.urls import path
from . import views

app_name = 'partidos'

urlpatterns = [
    # Listados con filtros
    path('', views.lista_partidos, name='lista_partidos'),
    path('proximos/', views.partidos_proximos, name='partidos_proximos'),
    path('pasados/', views.partidos_pasados, name='partidos_pasados'),
    path('en-vivo/', views.partidos_en_vivo, name='partidos_en_vivo'),
    path('hoy/', views.partidos_hoy, name='partidos_hoy'),
    
    # Detalles
    path('<int:partido_id>/', views.detalle_partido, name='detalle_partido'),
    path('<int:partido_id>/estadisticas/', views.estadisticas_partido, name='estadisticas_partido'),
    path('<int:partido_id>/predicciones/', views.predicciones_partido, name='predicciones_partido'),
    
    # Búsqueda y filtros
    path('buscar/', views.buscar_partidos, name='buscar_partidos'),
    path('por-fecha/', views.partidos_por_fecha, name='partidos_por_fecha'),
    path('por-deporte/<int:deporte_id>/', views.partidos_por_deporte, name='partidos_por_deporte'),
    path('por-equipo/<int:equipo_id>/', views.partidos_por_equipo, name='partidos_por_equipo'),
    path('por-liga/<str:liga>/', views.partidos_por_liga, name='partidos_por_liga'),
    
    # Gestión (solo staff)
    path('crear/', views.crear_partido, name='crear_partido'),
    path('<int:partido_id>/editar/', views.editar_partido, name='editar_partido'),
    path('<int:partido_id>/eliminar/', views.eliminar_partido, name='eliminar_partido'),
    path('<int:partido_id>/actualizar-resultado/', views.actualizar_resultado, name='actualizar_resultado'),
    path('<int:partido_id>/cambiar-estado/', views.cambiar_estado, name='cambiar_estado'),
    
    # APIs
    path('api/partidos-proximos/', views.api_partidos_proximos, name='api_partidos_proximos'),
    path('api/partidos-en-vivo/', views.api_partidos_en_vivo, name='api_partidos_en_vivo'),
    path('api/<int:partido_id>/detalle/', views.api_detalle_partido, name='api_detalle_partido'),
    path('api/<int:partido_id>/predicciones-usuarios/', views.api_predicciones_usuarios, name='api_predicciones_usuarios'),
]
