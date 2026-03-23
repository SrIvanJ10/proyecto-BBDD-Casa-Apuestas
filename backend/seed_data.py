"""
seed_data.py — Datos de ejemplo completos para SportPredict

Crea:
  - 5 usuarios de prueba con distintos niveles y suscripciones
  - Relaciones de amistad en Neo4j (directamente, sin request/accept)
  - 20 equipos de fútbol + 15 de baloncesto reales
  - Partidos reales: Jornada 29 La Liga + Jornadas 23-24 ACB (18 mar – 1 abr 2026)
  - Estadísticas de partidos finalizados en MongoDB
  - Mensajes de chat de ejemplo entre amigos
"""

import os
import random
from datetime import datetime

import django
from django.db.models import Q
from django.utils.timezone import make_aware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sportpredict.settings')
django.setup()

from sportpredict.db.mongodb.partidos import PartidoStatsManager  # noqa: E402
from sportpredict.db.neo4j_utils import Neo4jClient               # noqa: E402
from sportpredict.models import ChatMessage, Deporte, Equipo, Partido, Usuario  # noqa: E402


# ─────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────

def make_dt(date_str, time_str="12:00"):
    """Crea un datetime timezone-aware (Europe/Madrid) a partir de strings."""
    return make_aware(datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M"))


def hacer_amigos(neo4j, uid1, uid2, username1, username2):
    """Crea relación FRIENDS bidireccional en Neo4j directamente (para seeding)."""
    query = """
    MATCH (u1:User {id: $id1})
    MATCH (u2:User {id: $id2})
    MERGE (u1)-[:FRIENDS {created_at: datetime()}]->(u2)
    MERGE (u2)-[:FRIENDS {created_at: datetime()}]->(u1)
    RETURN u1.username AS a, u2.username AS b
    """
    with neo4j._driver.session() as session:
        session.run(query, id1=str(uid1), id2=str(uid2))
    print(f"  👥 {username1} ↔ {username2}")


# ─────────────────────────────────────────────────────────────────────
# DATOS: USUARIOS
# ─────────────────────────────────────────────────────────────────────

USUARIOS = [
    {
        'username': 'carlos_madrid',   'email': 'carlos@sportpredict.com',
        'password': 'Sportpredict2026!', 'first_name': 'Carlos', 'last_name': 'García',
        'tipo_suscripcion': 'PREMIUM',  'puntos_totales': 750, 'nivel_experto': 3,
    },
    {
        'username': 'lucia_blaugrana', 'email': 'lucia@sportpredict.com',
        'password': 'Sportpredict2026!', 'first_name': 'Lucía', 'last_name': 'Martínez',
        'tipo_suscripcion': 'FREE',     'puntos_totales': 120, 'nivel_experto': 1,
    },
    {
        'username': 'miguel_atletico', 'email': 'miguel@sportpredict.com',
        'password': 'Sportpredict2026!', 'first_name': 'Miguel', 'last_name': 'Torres',
        'tipo_suscripcion': 'PREMIUM',  'puntos_totales': 580, 'nivel_experto': 2,
    },
    {
        'username': 'ana_sevillista',  'email': 'ana@sportpredict.com',
        'password': 'Sportpredict2026!', 'first_name': 'Ana',    'last_name': 'Ruiz',
        'tipo_suscripcion': 'FREE',     'puntos_totales': 45,  'nivel_experto': 1,
    },
    {
        'username': 'pablo_atletxe',   'email': 'pablo@sportpredict.com',
        'password': 'Sportpredict2026!', 'first_name': 'Pablo',  'last_name': 'Fernández',
        'tipo_suscripcion': 'FREE',     'puntos_totales': 200, 'nivel_experto': 2,
    },
]

# Pares de amistad (username1, username2)
AMISTADES = [
    ('carlos_madrid',   'lucia_blaugrana'),
    ('carlos_madrid',   'miguel_atletico'),
    ('carlos_madrid',   'pablo_atletxe'),
    ('lucia_blaugrana', 'ana_sevillista'),
    ('miguel_atletico', 'pablo_atletxe'),
]


# ─────────────────────────────────────────────────────────────────────
# DATOS: EQUIPOS
# ─────────────────────────────────────────────────────────────────────

EQUIPOS_FUTBOL = [
    ('Real Madrid',          'RMA'), ('FC Barcelona',        'BAR'),
    ('Atlético de Madrid',   'ATM'), ('Athletic Club',       'ATH'),
    ('Villarreal CF',        'VIL'), ('Real Sociedad',       'RSO'),
    ('Sevilla FC',           'SEV'), ('Real Betis',          'BET'),
    ('Valencia CF',          'VAL'), ('CA Osasuna',          'OSA'),
    ('RC Celta',             'CEL'), ('Girona FC',           'GIR'),
    ('Rayo Vallecano',       'RAY'), ('Deportivo Alavés',    'ALA'),
    ('RCD Mallorca',         'MAL'), ('RCD Espanyol',        'ESP'),
    ('Getafe CF',            'GET'), ('UD Las Palmas',       'LPA'),
    ('Real Valladolid',      'VLD'), ('CD Leganés',          'LEG'),
]

EQUIPOS_BASKET = [
    ('Real Madrid Baloncesto', 'RMB'), ('FC Barcelona Basket',  'FCB'),
    ('Saski Baskonia',         'BKN'), ('Unicaja Málaga',        'UNI'),
    ('Valencia Basket',        'VBC'), ('BC Andorra',            'AND'),
    ('Bilbao Basket',          'BIL'), ('Joventut Badalona',     'JOV'),
    ('Gran Canaria',           'GRN'), ('Río Breogán',           'BRE'),
    ('Basquet Girona',         'BGI'), ('CB Granada',            'CBG'),
    ('San Pablo Burgos',       'SPB'), ('UCAM Murcia',           'UCM'),
    ('Força Lleida',           'LLE'),
]


# ─────────────────────────────────────────────────────────────────────
# DATOS: PARTIDOS
#
# Fútbol  → (local, visitante, fecha, hora, estado, goles_l, goles_v,
#             amarillas_l, amarillas_v, rojas_l, rojas_v, mvp)
# Basket  → (local, visitante, fecha, hora, estado, pts_l, pts_v,
#             exps_l, exps_v, mvp)
# ─────────────────────────────────────────────────────────────────────

# Fuente: Real Madrid official / La Liga / ACB · resultados del 20-22 mar 2026
PARTIDOS_LALIGA = [
    #  Jornada 29
    ('Villarreal CF',      'Real Sociedad',      '2026-03-20','21:00','FINALIZADO', 2,1, 2,3, 0,0, 'Dani Parejo'),
    ('RCD Espanyol',       'Getafe CF',          '2026-03-21','16:15','FINALIZADO', 1,1, 3,2, 1,0, None),
    ('CA Osasuna',         'Girona FC',          '2026-03-21','18:30','FINALIZADO', 2,0, 1,4, 0,1, 'Budimir'),
    ('Sevilla FC',         'Valencia CF',        '2026-03-21','21:00','FINALIZADO', 1,2, 2,1, 0,0, 'Hugo Duro'),
    ('FC Barcelona',       'Rayo Vallecano',     '2026-03-22','14:00','FINALIZADO', 3,0, 1,3, 0,1, 'Raphinha'),
    ('RC Celta',           'Deportivo Alavés',   '2026-03-22','16:15','FINALIZADO', 1,0, 2,2, 0,0, 'Iago Aspas'),
    ('Athletic Club',      'Real Betis',         '2026-03-22','18:30','FINALIZADO', 2,1, 3,2, 0,0, 'Nico Williams'),
    # Derbi madrileño — aún no jugado (hoy 22 mar, 21:00)
    ('Real Madrid',        'Atlético de Madrid', '2026-03-22','21:00','PENDIENTE',  None,None,None,None,None,None, None),
    # Jornada 30 — semana del 4-6 abril (fuera del rango pero añadidos como pendientes)
    ('Real Madrid',        'RC Celta',           '2026-04-05','16:15','PENDIENTE',  None,None,None,None,None,None, None),
    ('FC Barcelona',       'Sevilla FC',         '2026-04-05','18:30','PENDIENTE',  None,None,None,None,None,None, None),
    ('Atlético de Madrid', 'Villarreal CF',      '2026-04-06','21:00','PENDIENTE',  None,None,None,None,None,None, None),
]

PARTIDOS_ACB = [
    #  Jornada 23 — resultado confirmado: AND 98-102 BIL (sportytrader.com)
    ('BC Andorra',           'Bilbao Basket',          '2026-03-21','18:00','FINALIZADO', 98,102, 2,3, 'Jelínek'),
    ('Saski Baskonia',       'Basquet Girona',         '2026-03-22','12:30','FINALIZADO', 89, 76, 1,2, 'Sedekerskis'),
    ('Valencia Basket',      'CB Granada',             '2026-03-22','17:00','FINALIZADO', 82, 71, 0,3, 'Prepelič'),
    # Clásico del baloncesto — en juego ahora mismo (22 mar, 19:00)
    ('FC Barcelona Basket',  'Real Madrid Baloncesto', '2026-03-22','19:00','EN_JUEGO',   None,None,None,None, None),
    #  Jornada 24
    ('Real Madrid Baloncesto','Saski Baskonia',        '2026-03-28','20:30','PENDIENTE',  None,None,None,None, None),
    ('San Pablo Burgos',     'Valencia Basket',        '2026-03-29','18:00','PENDIENTE',  None,None,None,None, None),
    ('FC Barcelona Basket',  'Unicaja Málaga',         '2026-03-29','19:00','PENDIENTE',  None,None,None,None, None),
    ('Gran Canaria',         'Joventut Badalona',      '2026-03-29','19:00','PENDIENTE',  None,None,None,None, None),
    ('Bilbao Basket',        'UCAM Murcia',            '2026-03-30','18:00','PENDIENTE',  None,None,None,None, None),
]


# ─────────────────────────────────────────────────────────────────────
# DATOS: MENSAJES DE CHAT DE EJEMPLO
# ─────────────────────────────────────────────────────────────────────

CHATS = [
    ('carlos_madrid', 'lucia_blaugrana', [
        "¿Viste los resultados del Barça ayer?",
        "Sí! 3-0 al Rayo, brutal el Raphinha",
        "Le vais a quitar la liga al Madrid...",
        "Eso espero jaja, ¿has apostado ya por el derbi de esta noche?",
        "Sí, Madrid 2-1. Tú?",
        "Yo Atlético 1-0, el Simeone siempre aparece en el Bernabéu",
        "Jajaja ya veremos quién paga las cañas",
    ]),
    ('carlos_madrid', 'miguel_atletico', [
        "Migueeel, esta noche derbi 😈",
        "Preparate para sufrir jajaja, el Cholo tiene algo preparado",
        "En el Bernabéu no pasáis",
        "Igual que la temporada pasada que ganamos 0-1 😏",
        "Eso fue suerte, hoy es diferente",
        "El que pierde invita a las cañas del sábado",
        "Hecho. Aunque sabes que vas a pagar tú",
    ]),
    ('lucia_blaugrana', 'ana_sevillista', [
        "Ana, ¿cómo lleváis la temporada?",
        "Bastante mal la verdad, el Sevilla está irregular",
        "Ánimo! Todavía queda Liga",
        "Oye, ¿te has apuntado a la liga de predicciones?",
        "Sí! Tengo 45 puntos, estoy aprendiendo",
        "Yo ya tengo 120, vamos mejorando las dos",
        "Cuéntame cómo predices bien los resultados",
    ]),
]


# ─────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────

def run_seed():
    print("🌱 Iniciando seeding completo (PostgreSQL + MongoDB + Neo4j)...\n")

    stats_manager = PartidoStatsManager()
    neo4j = Neo4jClient()

    # ── 1. USUARIOS ──────────────────────────────────────────────────
    print("👤 Creando usuarios de prueba...")
    usuarios = {}
    for data in USUARIOS:
        user, created = Usuario.objects.get_or_create(
            username=data['username'],
            defaults={
                'email':             data['email'],
                'first_name':        data['first_name'],
                'last_name':         data['last_name'],
                'tipo_suscripcion':  data['tipo_suscripcion'],
                'puntos_totales':    data['puntos_totales'],
                'nivel_experto':     data['nivel_experto'],
            }
        )
        if created:
            user.set_password(data['password'])
            user.save()
            print(f"  ✅ {user.username:25s} [{data['tipo_suscripcion']:7s}] | pass: {data['password']}")
        else:
            print(f"  ℹ️  Ya existe: {user.username}")
        usuarios[data['username']] = user
        neo4j.create_user(user.id, user.username, user.email)

    # ── 2. AMISTADES ─────────────────────────────────────────────────
    print("\n👥 Creando amistades en Neo4j...")
    for u1_name, u2_name in AMISTADES:
        hacer_amigos(neo4j, usuarios[u1_name].id, usuarios[u2_name].id, u1_name, u2_name)

    # ── 3. DEPORTES Y EQUIPOS ─────────────────────────────────────────
    print("\n⚽🏀 Creando deportes y equipos...")
    futbol, _ = Deporte.objects.get_or_create(nombre='Fútbol')
    basket, _ = Deporte.objects.get_or_create(nombre='Baloncesto')

    equipos = {}
    for nombre, codigo in EQUIPOS_FUTBOL:
        e, created = Equipo.objects.get_or_create(
            codigo=codigo, defaults={'nombre': nombre, 'deporte': futbol}
        )
        equipos[nombre] = e
        if created:
            print(f"  ✅ [Fútbol]     {nombre}")

    for nombre, codigo in EQUIPOS_BASKET:
        e, created = Equipo.objects.get_or_create(
            codigo=codigo, defaults={'nombre': nombre, 'deporte': basket}
        )
        equipos[nombre] = e
        if created:
            print(f"  ✅ [Baloncesto] {nombre}")

    # ── 4. PARTIDOS LA LIGA ───────────────────────────────────────────
    print("\n🏟️  Creando partidos La Liga (Jornada 29 + próximos)...")
    for row in PARTIDOS_LALIGA:
        local_nm, vis_nm, fecha, hora, estado, gl, gv, al, av, rl, rv, mvp = row
        local = equipos.get(local_nm)
        vis   = equipos.get(vis_nm)
        if not local or not vis:
            print(f"  ⚠️  Equipo no encontrado: {local_nm!r} o {vis_nm!r}")
            continue

        resultado = f"{gl}-{gv}" if gl is not None else None
        partido, created = Partido.objects.get_or_create(
            equipo_local=local,
            equipo_visitante=vis,
            fecha_hora=make_dt(fecha, hora),
            defaults=dict(
                estado=estado, resultado_final=resultado,
                goles_local=gl, goles_visitante=gv,
                amarillas_local=al, amarillas_visitante=av,
                rojas_local=rl, rojas_visitante=rv,
                mvp_jugador=mvp,
                liga='La Liga EA Sports', temporada='2025-2026',
            )
        )
        if created:
            print(f"  ✅ {local_nm:22s} vs {vis_nm:22s} | {estado:10s} | {resultado or '---'}")
            if estado == 'FINALIZADO':
                pos_local = random.randint(40, 65)
                stats_manager.guardar_estadisticas_futbol(partido.id, {
                    'posesion':         {'local': pos_local, 'visitante': 100 - pos_local},
                    'tiros_puerta':     {'local': random.randint(4,14), 'visitante': random.randint(2,10)},
                    'tarjetas_amarillas':{'local': al or 0, 'visitante': av or 0},
                    'corners':          {'local': random.randint(2,9),  'visitante': random.randint(1,7)},
                })
            neo4j.create_match(partido.id, local_nm, vis_nm, 'Fútbol', partido.fecha_hora)
        else:
            print(f"  ℹ️  Ya existe: {local_nm} vs {vis_nm}")

    # ── 5. PARTIDOS ACB ───────────────────────────────────────────────
    print("\n🏀 Creando partidos Liga Endesa ACB (Jornadas 23-24)...")
    for row in PARTIDOS_ACB:
        local_nm, vis_nm, fecha, hora, estado, pl, pv, el, ev, mvp = row
        local = equipos.get(local_nm)
        vis   = equipos.get(vis_nm)
        if not local or not vis:
            print(f"  ⚠️  Equipo no encontrado: {local_nm!r} o {vis_nm!r}")
            continue

        resultado = f"{pl}-{pv}" if pl is not None else None
        partido, created = Partido.objects.get_or_create(
            equipo_local=local,
            equipo_visitante=vis,
            fecha_hora=make_dt(fecha, hora),
            defaults=dict(
                estado=estado, resultado_final=resultado,
                goles_local=pl, goles_visitante=pv,
                expulsiones_local=el, expulsiones_visitante=ev,
                mvp_jugador=mvp,
                liga='Liga Endesa ACB', temporada='2025-2026',
            )
        )
        if created:
            print(f"  ✅ {local_nm:25s} vs {vis_nm:25s} | {estado:10s} | {resultado or '---'}")
            if estado == 'FINALIZADO':
                stats_manager.guardar_estadisticas_baloncesto(partido.id, {
                    'tiros_campo_pct': {'local': random.randint(42,60), 'visitante': random.randint(38,55)},
                    'triples_pct':     {'local': random.randint(28,45), 'visitante': random.randint(25,42)},
                    'rebotes':         {'local': random.randint(25,45), 'visitante': random.randint(22,42)},
                    'asistencias':     {'local': random.randint(14,28), 'visitante': random.randint(12,25)},
                })
            neo4j.create_match(partido.id, local_nm, vis_nm, 'Baloncesto', partido.fecha_hora)
        else:
            print(f"  ℹ️  Ya existe: {local_nm} vs {vis_nm}")

    # ── 6. MENSAJES DE CHAT ───────────────────────────────────────────
    print("\n💬 Creando mensajes de chat de ejemplo...")
    for sender_name, receiver_name, mensajes in CHATS:
        sender   = usuarios.get(sender_name)
        receiver = usuarios.get(receiver_name)
        if not sender or not receiver:
            continue

        # Solo crear si no hay mensajes previos entre estos dos usuarios
        ya_existen = ChatMessage.objects.filter(
            Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)
        ).exists()
        if ya_existen:
            print(f"  ℹ️  Chat {sender_name} ↔ {receiver_name}: ya tiene mensajes")
            continue

        alternates = [sender, receiver]
        for i, texto in enumerate(mensajes):
            autor   = alternates[i % 2]
            destino = alternates[(i + 1) % 2]
            ChatMessage.objects.create(sender=autor, receiver=destino, content=texto, is_read=True)
        print(f"  ✅ Chat {sender_name} ↔ {receiver_name}: {len(mensajes)} mensajes")

    # ── RESUMEN ───────────────────────────────────────────────────────
    print("\n" + "─" * 60)
    print("🎉 Seeding completado! Resumen de accesos:")
    print("─" * 60)
    print(f"  {'Usuario':<25} {'Contraseña':<22} {'Plan'}")
    print("  " + "-" * 55)
    for d in USUARIOS:
        print(f"  {d['username']:<25} {d['password']:<22} {d['tipo_suscripcion']}")
    print("─" * 60)


if __name__ == '__main__':
    run_seed()
