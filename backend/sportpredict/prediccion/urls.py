from django.urls import path
from . import views

app_name = 'predicciones'

urlpatterns = [
    # Página principal
    path('', views.inicio, name='inicio'),
    
    # Predicciones del usuario
    path('mis-predicciones/', views.mis_predicciones, name='mis_predicciones'),
    path('hacer-prediccion/<int:partido_id>/', views.hacer_prediccion, name='hacer_prediccion'),
    path('editar-prediccion/<int:prediccion_id>/', views.editar_prediccion, name='editar_prediccion'),
    path('eliminar-prediccion/<int:prediccion_id>/', views.eliminar_prediccion, name='eliminar_prediccion'),
    
    # Dashboard y analytics
    path('dashboard/', views.dashboard, name='dashboard'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('mis-estadisticas/', views.mis_estadisticas, name='mis_estadisticas'),
    
    # Recomendaciones
    path('recomendaciones/', views.recomendaciones, name='recomendaciones'),
    path('recomendaciones/partidos/', views.recomendaciones_partidos, name='recomendaciones_partidos'),
    path('recomendaciones/usuarios-similares/', views.usuarios_similares, name='usuarios_similares'),
    
    # APIs para AJAX
    path('api/partidos-proximos/', views.api_partidos_proximos, name='api_partidos_proximos'),
    path('api/estadisticas-usuario/', views.api_estadisticas_usuario, name='api_estadisticas_usuario'),
]
