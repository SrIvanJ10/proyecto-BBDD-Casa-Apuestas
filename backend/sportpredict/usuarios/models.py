from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    """Modelo de usuario personalizado"""
    puntos_totales = models.IntegerField(default=0)
    nivel_experto = models.IntegerField(default=1)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    avatar = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.username
