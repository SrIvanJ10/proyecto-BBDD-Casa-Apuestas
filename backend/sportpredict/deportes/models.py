from django.db import models
from django.contrib.auth.models import AbstractUser

class Deporte(models.Model):
    """Deportes disponibles en la plataforma"""
    nombre = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
