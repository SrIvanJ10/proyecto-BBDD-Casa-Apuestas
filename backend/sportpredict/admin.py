# backend/sportpredict/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Deporte, Equipo, Partido, Prediccion

# Registro básico - MÍNIMO NECESARIO
admin.site.register(Usuario)
admin.site.register(Deporte)
admin.site.register(Equipo)
admin.site.register(Partido)
admin.site.register(Prediccion)