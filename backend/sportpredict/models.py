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
    
    # RESULTADOS DETALLADOS - Goles/Puntos
    goles_local = models.IntegerField(null=True, blank=True, help_text="Goles o puntos del equipo local")
    goles_visitante = models.IntegerField(null=True, blank=True, help_text="Goles o puntos del equipo visitante")
    
    # TARJETAS - Fútbol
    amarillas_local = models.IntegerField(null=True, blank=True, help_text="Tarjetas amarillas equipo local (fútbol)")
    amarillas_visitante = models.IntegerField(null=True, blank=True, help_text="Tarjetas amarillas equipo visitante (fútbol)")
    rojas_local = models.IntegerField(null=True, blank=True, help_text="Tarjetas rojas equipo local (fútbol)")
    rojas_visitante = models.IntegerField(null=True, blank=True, help_text="Tarjetas rojas equipo visitante (fútbol)")
    
    # EXPULSIONES - Baloncesto
    expulsiones_local = models.IntegerField(null=True, blank=True, help_text="Expulsiones por falta equipo local (baloncesto)")
    expulsiones_visitante = models.IntegerField(null=True, blank=True, help_text="Expulsiones por falta equipo visitante (baloncesto)")
    
    # MVP
    mvp_jugador = models.CharField(max_length=100, null=True, blank=True, help_text="Nombre del MVP del partido")

    class Meta:
        ordering = ['fecha_hora']

    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante}"

class Prediccion(models.Model):
    """Predicciones avanzadas de los usuarios"""
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    fecha_prediccion = models.DateTimeField(auto_now_add=True)
    
    # PREDICCIONES INDEPENDIENTES (todas opcionales)
    # Resultado exacto
    pred_goles_local = models.IntegerField(null=True, blank=True, help_text="Predicción goles/puntos equipo local")
    pred_goles_visitante = models.IntegerField(null=True, blank=True, help_text="Predicción goles/puntos equipo visitante")
    
    # Tarjetas fútbol
    pred_amarillas_local = models.IntegerField(null=True, blank=True, help_text="Predicción amarillas equipo local")
    pred_amarillas_visitante = models.IntegerField(null=True, blank=True, help_text="Predicción amarillas equipo visitante")
    pred_rojas_local = models.IntegerField(null=True, blank=True, help_text="Predicción rojas equipo local")
    pred_rojas_visitante = models.IntegerField(null=True, blank=True, help_text="Predicción rojas equipo visitante")
    
    # Expulsiones baloncesto
    pred_expulsiones_local = models.IntegerField(null=True, blank=True, help_text="Predicción expulsiones equipo local")
    pred_expulsiones_visitante = models.IntegerField(null=True, blank=True, help_text="Predicción expulsiones equipo visitante")
    
    # MVP
    pred_mvp_jugador = models.CharField(max_length=100, null=True, blank=True, help_text="Predicción del MVP")
    
    # PUNTOS POR CATEGORÍA
    puntos_resultado = models.IntegerField(default=0, help_text="Puntos por acertar resultado")
    puntos_tarjetas = models.IntegerField(default=0, help_text="Puntos por acertar tarjetas/expulsiones")
    puntos_mvp = models.IntegerField(default=0, help_text="Puntos por acertar MVP")
    puntos_totales = models.IntegerField(default=0, help_text="Puntos totales de esta predicción")
    
    # Estado
    evaluada = models.BooleanField(default=False, help_text="Si ya se calcularon los puntos")
    
    # COMPATIBILIDAD CON SISTEMA ANTERIOR
    prediccion = models.CharField(max_length=10, blank=True, help_text="[LEGACY] Predicción simple antigua")
    puntos_obtenidos = models.IntegerField(default=0, help_text="[LEGACY] Alias de puntos_totales")
    correcta = models.BooleanField(default=False, help_text="[LEGACY] Si acertó completamente")

    class Meta:
        unique_together = ['usuario', 'partido']
        ordering = ['-fecha_prediccion']

    def __str__(self):
        preds = []
        if self.pred_goles_local is not None:
            preds.append(f"{self.pred_goles_local}-{self.pred_goles_visitante}")
        if self.pred_mvp_jugador:
            preds.append(f"MVP:{self.pred_mvp_jugador}")
        pred_str = ", ".join(preds) if preds else "Sin predicciones"
        return f"{self.usuario.username}: {pred_str}"
    
    def save(self, *args, **kwargs):
        # Mantener sincronizado puntos_obtenidos con puntos_totales (compatibilidad)
        self.puntos_obtenidos = self.puntos_totales
        super().save(*args, **kwargs)