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


class Deporte(models.Model):
    """Deportes disponibles en la plataforma"""
    nombre = models.CharField(max_length=50)
    activo = models.BooleanField(default=True) #por si quieres activar el deporte

    def __str__(self):
        return self.nombre


class Equipo(models.Model):
    """Equipos deportivos"""
    nombre = models.CharField(max_length=100)
    deporte = models.ForeignKey(Deporte, on_delete=models.CASCADE)
    logo_url = models.URLField(blank=True, null=True)
    codigo = models.CharField(max_length=10, unique=True)  # Ej: "BAR", "RMA"

    def __str__(self):
        return self.nombre

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

class Prediccion(models.Model):
    """Predicciones de los usuarios"""
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    prediccion = models.CharField(max_length=10)  # "2-1", "0-0"
    puntos_obtenidos = models.IntegerField(default=0)
    fecha_prediccion = models.DateTimeField(auto_now_add=True)
    correcta = models.BooleanField(default=False)

    class Meta:
        unique_together = ['usuario', 'partido']  # Un usuario solo una predicción por partido
        ordering = ['-fecha_prediccion']

    def __str__(self):
        return f"{self.usuario}: {self.prediccion}"