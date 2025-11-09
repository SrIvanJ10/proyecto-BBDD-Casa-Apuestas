from django.db import models
from django.contrib.auth.models import AbstractUser

class Equipo(models.Model):
    """Equipos deportivos"""
    nombre = models.CharField(max_length=100)
    deporte = models.ForeignKey(Deporte, on_delete=models.CASCADE)
    logo_url = models.URLField(blank=True, null=True)
    codigo = models.CharField(max_length=10, unique=True)  # Ej: "BAR", "RMA"

    def __str__(self):
        return self.nombre

