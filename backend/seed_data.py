import os
import django
import random
from datetime import datetime, timedelta
from django.utils import timezone

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sportpredict.settings')
django.setup()

from sportpredict.models import Deporte, Equipo, Partido, Usuario
from sportpredict.db.mongodb.partidos import PartidoStatsManager

def run_seed():
    print("🌱 Iniciando proceso de seeding completo (PostgreSQL + MongoDB + Neo4j)...")
    
    # Inicializar manager de MongoDB
    stats_manager = PartidoStatsManager()

    # 1. Crear Deportes
    deportes = ['Fútbol', 'Baloncesto']
    deporte_objs = {}
    
    for nombre in deportes:
        obj, created = Deporte.objects.get_or_create(nombre=nombre)
        deporte_objs[nombre] = obj
        if created:
            print(f"✅ Deporte creado: {nombre}")
        else:
            print(f"ℹ️ Deporte ya existe: {nombre}")

    # 2. Crear Equipos
    equipos_data = {
        'Fútbol': [
            ('Real Madrid', 'RMA'), ('FC Barcelona', 'BAR'), ('Atlético de Madrid', 'ATM'),
            ('Valencia CF', 'VAL'), ('Sevilla FC', 'SEV'), ('Real Betis', 'BET'),
            ('Athletic Club', 'ATH'), ('Real Sociedad', 'RSO')
        ],
        'Baloncesto': [
            ('Real Madrid Baloncesto', 'RMB'), ('FC Barcelona Basket', 'FCB'), 
            ('Baskonia', 'BKN'), ('Unicaja', 'UNI'), ('Valencia Basket', 'VBC')
        ]
    }

    equipo_objs = []

    for deporte_nombre, equipos in equipos_data.items():
        deporte = deporte_objs[deporte_nombre]
        for nombre, codigo in equipos:
            equipo, created = Equipo.objects.get_or_create(
                codigo=codigo,
                defaults={'nombre': nombre, 'deporte': deporte}
            )
            equipo_objs.append(equipo)
            if created:
                print(f"✅ Equipo creado: {nombre}")

    # 3. Crear Partidos y Estadísticas
    
    estados = ['PENDIENTE', 'EN_JUEGO', 'FINALIZADO']
    
    futbol_teams = [e for e in equipo_objs if e.deporte.nombre == 'Fútbol']
    basket_teams = [e for e in equipo_objs if e.deporte.nombre == 'Baloncesto']

    def generar_stats_futbol():
        return {
            'posesion': {'local': random.randint(30, 70), 'visitante': 0}, # Se ajusta abajo
            'tiros_puerta': {'local': random.randint(0, 15), 'visitante': random.randint(0, 15)},
            'tarjetas_amarillas': {'local': random.randint(0, 5), 'visitante': random.randint(0, 5)},
            'corners': {'local': random.randint(0, 10), 'visitante': random.randint(0, 10)}
        }

    def generar_stats_basket():
        return {
            'tiros_campo_pct': {'local': random.randint(35, 60), 'visitante': random.randint(35, 60)},
            'triples_pct': {'local': random.randint(25, 45), 'visitante': random.randint(25, 45)},
            'rebotes': {'local': random.randint(20, 50), 'visitante': random.randint(20, 50)},
            'asistencias': {'local': random.randint(10, 30), 'visitante': random.randint(10, 30)}
        }

    def crear_partidos_liga(teams, liga_nombre, deporte_tipo):
        print(f"\nGenerando partidos para {liga_nombre}...")
        for _ in range(15): # Crear 15 partidos aleatorios
            local = random.choice(teams)
            visitante = random.choice([t for t in teams if t != local])
            
            estado = random.choice(estados)
            fecha_base = timezone.now()
            
            if estado == 'PENDIENTE':
                fecha = fecha_base + timedelta(days=random.randint(1, 7))
                resultado = None
            elif estado == 'EN_JUEGO':
                fecha = fecha_base
                if deporte_tipo == 'futbol':
                    resultado = f"{random.randint(0,3)}-{random.randint(0,3)}"
                else:
                    resultado = f"{random.randint(60,100)}-{random.randint(60,100)}"
            else: # FINALIZADO
                fecha = fecha_base - timedelta(days=random.randint(1, 7))
                if deporte_tipo == 'futbol':
                    resultado = f"{random.randint(0,5)}-{random.randint(0,5)}"
                else:
                    resultado = f"{random.randint(70,120)}-{random.randint(70,120)}"

            # Crear en PostgreSQL (Dispara señal a Neo4j automáticamente)
            partido = Partido.objects.create(
                equipo_local=local,
                equipo_visitante=visitante,
                fecha_hora=fecha,
                estado=estado,
                resultado_final=resultado,
                liga=liga_nombre,
                temporada="2025-2026"
            )
            print(f"✅ [PG+Neo4j] Partido creado: {local} vs {visitante} ({estado})")

            # Crear estadísticas en MongoDB
            if deporte_tipo == 'futbol':
                stats = generar_stats_futbol()
                stats['posesion']['visitante'] = 100 - stats['posesion']['local']
                stats_manager.guardar_estadisticas_futbol(partido.id, stats)
            else:
                stats = generar_stats_basket()
                stats_manager.guardar_estadisticas_baloncesto(partido.id, stats)
            
            print(f"✅ [MongoDB] Stats generadas para partido {partido.id}")

    crear_partidos_liga(futbol_teams, "La Liga", "futbol")
    crear_partidos_liga(basket_teams, "Liga ACB", "baloncesto")

    print("\n🎉 Seeding completado! Datos sincronizados en PostgreSQL, MongoDB y Neo4j.")

if __name__ == '__main__':
    run_seed()
