from django.db import models
from django.contrib.auth.models import AbstractUser

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
