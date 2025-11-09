from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Autenticación
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Perfil de usuario
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    
    # Gestión de cuenta
    path('cambiar-password/', views.cambiar_password, name='cambiar_password'),
    path('eliminar-cuenta/', views.eliminar_cuenta, name='eliminar_cuenta'),
    
    # Verificación OTP
    path('verificar-email/', views.verificar_email, name='verificar_email'),
    path('verificar-codigo/<str:token>/', views.verificar_codigo, name='verificar_codigo'),
    
    # Recuperación
    path('recuperar-password/', views.recuperar_password, name='recuperar_password'),
    path('restablecer-password/<str:token>/', views.restablecer_password, name='restablecer_password'),
]
