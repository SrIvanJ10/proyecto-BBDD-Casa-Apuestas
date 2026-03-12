from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    """Modelo de usuario personalizado"""
    TIPO_SUSCRIPCION_CHOICES = [
        ('FREE', 'Free'),
        ('PREMIUM', 'Premium'),
    ]
    
    puntos_totales = models.IntegerField(default=0)
    nivel_experto = models.IntegerField(default=1)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    avatar = models.URLField(blank=True, null=True)
    tipo_suscripcion = models.CharField(
        max_length=10,
        choices=TIPO_SUSCRIPCION_CHOICES,
        default='FREE'
    )
    racha_actual = models.IntegerField(default=0)
    mejor_racha = models.IntegerField(default=0)

    def __str__(self):
        return self.username

    @property
    def total_predicciones(self):
        return self.prediccion_set.count()

    @property
    def predicciones_correctas(self):
        return self.prediccion_set.filter(correcta=True).count()

    def porcentaje_aciertos(self):
        total = self.total_predicciones
        return round((self.predicciones_correctas / total * 100), 2) if total > 0 else 0
    
    def puede_apostar(self):
        """
        Verifica si el usuario puede realizar una apuesta.
        - FREE: máximo 5 predicciones totales
        - PREMIUM: requiere 500+ puntos, predicciones ilimitadas
        """
        from sportpredict.models import Prediccion
        
        # Si es premium, verificar que tenga al menos 500 puntos
        if self.tipo_suscripcion == 'PREMIUM':
            return self.puntos_totales >= 500
        
        # Si es free, verificar que no haya superado el límite de 5 predicciones
        predicciones_count = Prediccion.objects.filter(usuario=self).count()
        return predicciones_count < 5


class Deporte(models.Model):
    """Deportes disponibles en la plataforma"""
    nombre = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    icono = models.CharField(max_length=50, blank=True, default='🏆')
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    def partidos_proximos(self):
        from django.db.models import Q
        from django.utils import timezone
        return Partido.objects.filter(
            Q(equipo_local__deporte=self) | Q(equipo_visitante__deporte=self),
            estado='PENDIENTE',
            fecha_hora__gt=timezone.now()
        ).order_by('fecha_hora')


class Equipo(models.Model):
    """Equipos deportivos"""
    nombre = models.CharField(max_length=100)
    deporte = models.ForeignKey(Deporte, on_delete=models.CASCADE)
    logo_url = models.URLField(blank=True, null=True)
    codigo = models.CharField(max_length=10, unique=True)  # Ej: "BAR", "RMA"
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    def partidos_totales(self):
        from django.db.models import Q
        return Partido.objects.filter(
            Q(equipo_local=self) | Q(equipo_visitante=self)
        )

    def estadisticas(self):
        partidos = self.partidos_totales().filter(estado='FINALIZADO')
        victorias = partidos.filter(
            models.Q(equipo_local=self, goles_local__gt=models.F('goles_visitante')) |
            models.Q(equipo_visitante=self, goles_visitante__gt=models.F('goles_local'))
        ).count()
        derrotas = partidos.filter(
            models.Q(equipo_local=self, goles_local__lt=models.F('goles_visitante')) |
            models.Q(equipo_visitante=self, goles_visitante__lt=models.F('goles_local'))
        ).count()
        empates = partidos.filter(goles_local=models.F('goles_visitante')).count()
        return {
            'jugados': partidos.count(),
            'victorias': victorias,
            'derrotas': derrotas,
            'empates': empates,
        }

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

    @property
    def resultado_local(self):
        return self.goles_local

    @property
    def resultado_visitante(self):
        return self.goles_visitante

    def es_predecible(self):
        from django.utils import timezone
        return self.estado == 'PENDIENTE' and self.fecha_hora > timezone.now()

    def total_predicciones(self):
        return self.prediccion_set.count()

    def predicciones_usuarios(self):
        predicciones = self.prediccion_set.all()
        total = predicciones.count()
        if total == 0:
            return {'local': 0, 'empate': 0, 'visitante': 0, 'total': 0}
        local = predicciones.filter(
            pred_goles_local__gt=models.F('pred_goles_visitante')
        ).count()
        visitante = predicciones.filter(
            pred_goles_visitante__gt=models.F('pred_goles_local')
        ).count()
        empate = predicciones.filter(
            pred_goles_local=models.F('pred_goles_visitante'),
            pred_goles_local__isnull=False
        ).count()
        return {
            'local': round(local / total * 100, 1),
            'empate': round(empate / total * 100, 1),
            'visitante': round(visitante / total * 100, 1),
            'total': total,
        }

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

    def es_editable(self):
        from django.utils import timezone
        return self.partido.estado == 'PENDIENTE' and self.partido.fecha_hora > timezone.now()