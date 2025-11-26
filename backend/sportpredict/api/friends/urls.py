from django.urls import path
from . import views

urlpatterns = [
    # Lista de amigos
    path('', views.get_friends, name='friends-list'),
    
    # Solicitudes pendientes recibidas
    path('pending/', views.get_pending_requests, name='friends-pending'),
    
    # Solicitudes enviadas
    path('sent/', views.get_sent_requests, name='friends-sent'),
    
    # Enviar solicitud de amistad
    path('request/', views.send_friend_request, name='friends-request'),
    
    # Aceptar solicitud de amistad
    path('accept/<int:user_id>/', views.accept_friend_request, name='friends-accept'),
    
    # Rechazar solicitud de amistad
    path('reject/<int:user_id>/', views.reject_friend_request, name='friends-reject'),
    
    # Eliminar amigo
    path('<int:user_id>/', views.remove_friend, name='friends-remove'),
    
    # Buscar usuarios
    path('search/', views.search_users, name='friends-search'),
    
    # Estado de amistad con un usuario
    path('status/<int:user_id>/', views.get_friendship_status, name='friends-status'),
]
