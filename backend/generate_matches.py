#!/usr/bin/env python
"""
Script para generar 20 partidos de prueba
- 10 partidos de fútbol
- 10 partidos de baloncesto
- Mezcla de estados: PENDIENTE, EN_JUEGO, FINALIZADO
- Resultados aleatorios
"""
import os
import django
import random
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sportpredict.settings')
django.setup()

from sportpredict.models import Deporte, Equipo, Partido
from django.utils import timezone


def generar_partidos():
    """Genera 20 partidos de prueba"""
    
    # Obtener deportes
    try:
        futbol = Deporte.objects.get(nombre__icontains='fútbol')
    except Deporte.DoesNotExist:
        futbol = Deporte.objects.create(nombre='Fútbol', activo=True)
    
    try:
        baloncesto = Deporte.objects.get(nombre__icontains='baloncesto')
    except Deporte.DoesNotExist:
        baloncesto = Deporte.objects.create(nombre='Baloncesto', activo=True)
    
    # Obtener equipos de fútbol
    equipos_futbol = list(Equipo.objects.filter(deporte=futbol))
    if len(equipos_futbol) < 4:
        print("No hay suficientes equipos de fútbol. Creando equipos...")
        equipos_futbol = []
        nombres_futbol = ['FC Barcelona', 'Real Madrid', 'Atlético de Madrid', 'Sevilla FC', 
                         'Valencia CF', 'Real Betis', 'Real Sociedad', 'Athletic Bilbao']
        for i, nombre in enumerate(nombres_futbol):
            if not Equipo.objects.filter(nombre=nombre).exists():
                equipo = Equipo.objects.create(
                    nombre=nombre,
                    deporte=futbol,
                    codigo=f'F{i+1:02d}'
                )
                equipos_futbol.append(equipo)
    
    # Obtener equipos de baloncesto
    equipos_baloncesto = list(Equipo.objects.filter(deporte=baloncesto))
    if len(equipos_baloncesto) < 4:
        print("No hay suficientes equipos de baloncesto. Creando equipos...")
        equipos_baloncesto = []
        nombres_baloncesto = ['Real Madrid Baloncesto', 'FC Barcelona Basket', 'Baskonia', 
                             'Valencia Basket', 'Unicaja', 'Joventut', 'Gran Canaria', 'Manresa']
        for i, nombre in enumerate(nombres_baloncesto):
            if not Equipo.objects.filter(nombre=nombre).exists():
                equipo = Equipo.objects.create(
                    nombre=nombre,
                    deporte=baloncesto,
                    codigo=f'B{i+1:02d}'
                )
                equipos_baloncesto.append(equipo)
    
    # Estados posibles
    estados = ['PENDIENTE', 'EN_JUEGO', 'FINALIZADO']
    
    # Generar 10 partidos de fútbol
    print("Generando 10 partidos de fútbol...")
    for i in range(10):
        # Seleccionar equipos aleatorios
        local, visitante = random.sample(equipos_futbol, 2)
        
        # Generar fecha aleatoria (entre ayer y dentro de 7 días)
        dias_offset = random.randint(-1, 7)
        fecha_hora = timezone.now() + timedelta(days=dias_offset, hours=random.randint(0, 23))
        
        # Seleccionar estado
        estado = random.choice(estados)
        
        # Generar resultado si está finalizado o en juego
        goles_local = None
        goles_visitante = None
        resultado_final = None
        
        if estado in ['FINALIZADO', 'EN_JUEGO']:
            goles_local = random.randint(0, 5)
            goles_visitante = random.randint(0, 5)
            resultado_final = f'{goles_local}-{goles_visitante}'
        
        partido = Partido.objects.create(
            equipo_local=local,
            equipo_visitante=visitante,
            fecha_hora=fecha_hora,
            estado=estado,
            goles_local=goles_local,
            goles_visitante=goles_visitante,
            resultado_final=resultado_final,
            liga='La Liga',
            temporada='2025-2026'
        )
        print(f"  ✓ {local.nombre} vs {visitante.nombre} - {estado} - {resultado_final or 'Sin resultado'}")
    
    # Generar 10 partidos de baloncesto
    print("\nGenerando 10 partidos de baloncesto...")
    for i in range(10):
        # Seleccionar equipos aleatorios
        local, visitante = random.sample(equipos_baloncesto, 2)
        
        # Generar fecha aleatoria
        dias_offset = random.randint(-1, 7)
        fecha_hora = timezone.now() + timedelta(days=dias_offset, hours=random.randint(0, 23))
        
        # Seleccionar estado
        estado = random.choice(estados)
        
        # Generar resultado si está finalizado o en juego
        goles_local = None
        goles_visitante = None
        resultado_final = None
        
        if estado in ['FINALIZADO', 'EN_JUEGO']:
            goles_local = random.randint(60, 110)
            goles_visitante = random.randint(60, 110)
            resultado_final = f'{goles_local}-{goles_visitante}'
        
        partido = Partido.objects.create(
            equipo_local=local,
            equipo_visitante=visitante,
            fecha_hora=fecha_hora,
            estado=estado,
            goles_local=goles_local,
            goles_visitante=goles_visitante,
            resultado_final=resultado_final,
            liga='Liga ACB',
            temporada='2025-2026'
        )
        print(f"  ✓ {local.nombre} vs {visitante.nombre} - {estado} - {resultado_final or 'Sin resultado'}")
    
    print("\n✅ 20 partidos generados exitosamente!")
    print(f"   - Fútbol: 10 partidos")
    print(f"   - Baloncesto: 10 partidos")
    print(f"   - Estados: PENDIENTE, EN_JUEGO, FINALIZADO (aleatorio)")


if __name__ == '__main__':
    generar_partidos()
