from django.db import models
from django.contrib.auth.models import AbstractUser

class Partido(models.Model):
    """Partidos disponibles para predecir"""
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_JUEGO', 'En juego'),
        ('FINALIZADO', 'Finalizado'),
        ('CANCELADO', 'Cancelado'),
    ]

    equipo_local = models.ForeignKey(Equipo, related_name='partidos_local', on_delete=models.CASCADE)
    equipo_visitante = models.ForeignKey(Equipo, related_name='partidos_visitante', on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    resultado_final = models.CharField(max_length=10, blank=True, null=True)  # "2-1", "0-0"
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    liga = models.CharField(max_length=100, blank=True)
    temporada = models.CharField(max_length=50, default="2025-2026")

    class Meta:
        ordering = ['fecha_hora']

    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante}"

