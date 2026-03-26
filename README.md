# Sport365 🏆

Plataforma de predicciones deportivas con sistema social entre usuarios. Permite predecir resultados de partidos de fútbol y baloncesto, acumular puntos, seguir a amigos y chatear con ellos en tiempo real.

Proyecto universitario de la asignatura **Calidad y Auditoría de Sistemas de Información**.

---

## Tabla de contenidos

- [Características](#características)
- [Arquitectura](#arquitectura)
- [Stack tecnológico](#stack-tecnológico)
- [Requisitos previos](#requisitos-previos)
- [Instalación y arranque](#instalación-y-arranque)
- [Datos de ejemplo](#datos-de-ejemplo)
- [Usuarios de prueba](#usuarios-de-prueba)
- [Estructura del proyecto](#estructura-del-proyecto)
- [API REST](#api-rest)
- [Chat en tiempo real](#chat-en-tiempo-real)
- [Organización del equipo](#organización-del-equipo)

---

## Características

- **Predicciones deportivas** — Predice resultados de La Liga y Liga ACB con sistema de puntuación por categorías (resultado, tarjetas, MVP).
- **Sistema de niveles** — Acumula puntos para subir de nivel experto.
- **Suscripciones FREE / PREMIUM** — Los usuarios FREE tienen un límite de 5 predicciones; los PREMIUM acceden sin límite con 500+ puntos.
- **Red social** — Envía y acepta solicitudes de amistad, busca usuarios.
- **Recomendaciones inteligentes** — El sistema sugiere partidos en los que apuestan tus amigos (filtrado colaborativo sobre Neo4j).
- **Chat en tiempo real** — Mensajería instantánea entre amigos mediante WebSockets (Django Channels).
- **Panel de administración** — Gestión de partidos, usuarios y resultados.

---

## Arquitectura

El proyecto utiliza una arquitectura **políglota de bases de datos**, donde cada motor resuelve el problema para el que está optimizado:

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                             │
│               React + Vite  (puerto 3000)                   │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP REST / WebSocket
┌────────────────────────▼────────────────────────────────────┐
│                        BACKEND                              │
│         Django 4.2 + DRF + Django Channels (puerto 8000)    │
└──┬──────────────┬──────────────┬──────────────┬────────────┘
   │              │              │              │
   ▼              ▼              ▼              ▼
PostgreSQL      Neo4j         MongoDB         Redis
Usuarios        Amistades     Estadísticas    Caché / Sesiones
Partidos        Grafo social  de partidos     Channel Layer
Predicciones    Recomen-      (posesión,      (WebSockets)
Mensajes        daciones      tiros, etc.)
```

### ¿Por qué cada base de datos?

| Motor | Uso | Justificación |
|---|---|---|
| **PostgreSQL** | Usuarios, partidos, predicciones, mensajes | Datos relacionales con integridad referencial |
| **Neo4j** | Amistades, recomendaciones | Las relaciones son ciudadanos de primera clase en grafos |
| **MongoDB** | Estadísticas de partido | Esquema flexible, documentos variables por deporte |
| **Redis** | Sesiones, caché, Channel Layer | Velocidad en datos efímeros y pub/sub para WebSockets |

---

## Stack tecnológico

### Backend
- Python 3.11 / Django 4.2
- Django REST Framework 3.14
- Django Channels 4.1 + Daphne (WebSockets ASGI)
- PyJWT (autenticación stateless)
- neo4j-driver, pymongo, redis, django-redis

### Frontend
- React 18 + Vite
- React Router v6
- Axios
- WebSocket API nativa del navegador

### Infraestructura
- Docker + Docker Compose
- PostgreSQL 13
- Neo4j 5 Community + APOC
- MongoDB 4.4
- Redis 7

---

## Requisitos previos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (o Docker Engine + Compose v2)
- Git

---

## Instalación y arranque

### 1. Clonar el repositorio

```bash
git clone https://github.com/SrIvanJ10/proyecto-BBDD-Casa-Apuestas.git
cd proyecto-BBDD-Casa-Apuestas
```

### 2. Arrancar todos los servicios

```bash
docker-compose up --build
```

Esto levanta: PostgreSQL, Neo4j, MongoDB, Redis, backend Django y frontend React.

| Servicio | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000/api/ |
| Documentación Swagger | http://localhost:8000/swagger/ |
| Panel de Admin Django | http://localhost:8000/admin/ |
| Neo4j Browser | http://localhost:7474 |

### 3. Verificar que todo funciona

```bash
curl http://localhost:8000/health/
# → {"status": "healthy", "service": "SportPredict API"}
```

### Desarrollo frontend en local (recomendado)

Para ver cambios en React al instante sin reconstruir Docker:

```bash
cd frontend
npm install
npm run dev        # http://localhost:5173
```

---

## Datos de ejemplo

Ejecutar el script de seeding para poblar todas las bases de datos con datos reales:

```bash
docker exec sportpredict_web python seed_data.py
```

El script crea:
- 5 usuarios de prueba con distintos niveles y suscripciones
- Relaciones de amistad entre ellos en Neo4j
- 20 equipos de fútbol (La Liga completa) + 15 de baloncesto (ACB)
- Partidos reales de la **Jornada 29 de La Liga** y **Jornadas 23-24 de la Liga ACB** (marzo–abril 2026), con resultados y estadísticas en MongoDB
- Mensajes de chat de ejemplo entre amigos

Para reiniciar desde cero:

```bash
docker exec sportpredict_web python manage.py flush --no-input
docker exec sportpredict_web python manage.py migrate
docker exec sportpredict_web python seed_data.py
```

---

## Usuarios de prueba

Todos usan la contraseña `Sportpredict2026!`

| Usuario | Nombre | Plan | Puntos | Nivel |
|---|---|---|---|---|
| `carlos_madrid` | Carlos García | PREMIUM | 750 | 3 |
| `lucia_blaugrana` | Lucía Martínez | FREE | 120 | 1 |
| `miguel_atletico` | Miguel Torres | PREMIUM | 580 | 2 |
| `ana_sevillista` | Ana Ruiz | FREE | 45 | 1 |
| `pablo_atletxe` | Pablo Fernández | FREE | 200 | 2 |

**Superusuario admin** (Django Admin): `Dios` / `PorElPadreElHijoYElEspirituSanto`

### Grafo de amistades

```
carlos_madrid ──── lucia_blaugrana ──── ana_sevillista
      │
      ├──── miguel_atletico ──── pablo_atletxe
      │
      └──── pablo_atletxe
```

---

## Estructura del proyecto

```
proyecto-BBDD-Casa-Apuestas/
├── backend/
│   ├── sportpredict/
│   │   ├── api/
│   │   │   ├── admin/          # Gestión de partidos y resultados
│   │   │   ├── analytics/      # Estadísticas y análisis
│   │   │   ├── auth/           # Login, registro, JWT
│   │   │   ├── chat/           # WebSocket consumer + endpoints REST
│   │   │   │   ├── consumers.py   ← WebSocket en tiempo real
│   │   │   │   ├── routing.py     ← URL routing WS
│   │   │   │   └── views.py       ← Historial + conversaciones
│   │   │   ├── friends/        # Solicitudes y gestión de amigos
│   │   │   ├── matches/        # CRUD de partidos
│   │   │   ├── predictions/    # CRUD de predicciones
│   │   │   ├── recommendations/# Recomendaciones basadas en amigos
│   │   │   └── users/          # Perfil de usuario
│   │   ├── db/
│   │   │   ├── neo4j_utils.py  # Cliente Neo4j (amistades, recomendaciones)
│   │   │   ├── mongodb/        # Cliente MongoDB (estadísticas)
│   │   │   └── redis/          # Sesiones, OTP, rate limiting
│   │   ├── models.py           # Usuario, Partido, Prediccion, ChatMessage
│   │   ├── serializers.py
│   │   ├── settings.py
│   │   └── asgi.py             # Channels + HTTP routing
│   ├── seed_data.py            # Script de datos de ejemplo
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   └── src/
│       ├── components/         # Navbar, FriendCard, UserSearchCard
│       ├── context/            # AuthContext (JWT en localStorage)
│       ├── pages/
│       │   ├── Chat.jsx        # Chat en tiempo real (WebSocket)
│       │   ├── Friends.jsx     # Gestión de amigos
│       │   ├── Home.jsx
│       │   └── ...
│       └── services/
│           ├── api.js          # Axios con interceptor JWT
│           ├── chatService.js
│           └── friendService.js
└── docker-compose.yml
```

---

## API REST

La documentación completa está en **http://localhost:8000/swagger/**

### Autenticación

Todos los endpoints protegidos requieren el header:
```
Authorization: Bearer <jwt_token>
```

### Endpoints principales

| Módulo | Método | Endpoint | Descripción |
|---|---|---|---|
| **Auth** | POST | `/api/auth/login/` | Login → devuelve JWT |
| | POST | `/api/auth/register/` | Registro de usuario |
| **Friends** | GET | `/api/friends/` | Lista de amigos |
| | POST | `/api/friends/request/` | Enviar solicitud |
| | POST | `/api/friends/accept/<id>/` | Aceptar solicitud |
| | GET | `/api/friends/search/` | Buscar usuarios |
| **Chat** | GET | `/api/chat/conversations/` | Conversaciones con último mensaje |
| | GET | `/api/chat/<id>/messages/` | Historial de mensajes |
| | POST | `/api/chat/<id>/messages/` | Enviar mensaje (REST fallback) |
| **Matches** | GET | `/api/matches/` | Listado de partidos |
| **Predictions** | GET/POST | `/api/predictions/` | Ver / crear predicciones |
| **Recommendations** | GET | `/api/recommendations/` | Partidos recomendados |

---

## Chat en tiempo real

El chat usa **WebSockets** mediante Django Channels con Redis como channel layer.

### Conexión desde el cliente

```javascript
const ws = new WebSocket(`ws://localhost:8000/ws/chat/<other_user_id>/?token=<jwt>`);

ws.onmessage = (event) => {
    const { type, message } = JSON.parse(event.data);
    // type === 'message' → nuevo mensaje recibido
};

ws.send(JSON.stringify({ content: 'Hola!' }));
```

### Flujo

```
Cliente A                  Django Channels              Cliente B
    │                           │                           │
    │── WS connect ──────────►  │                           │
    │                    autentica JWT                      │
    │                    verifica amistad (Neo4j)           │
    │                    une al grupo chat_A_B              │
    │                           │  ◄─── WS connect ─────── │
    │                           │  une al grupo chat_A_B    │
    │── send {content} ───────► │                           │
    │                    guarda en PostgreSQL               │
    │                    group_send(chat_A_B)               │
    │ ◄── {type:message} ──────  │ ──── {type:message} ──► │
```

---

## Organización del equipo

- 📋 Tablero Trello: https://trello.com/b/Ssf3yjV7/casino
- 📖 Wiki del proyecto: https://github.com/SrIvanJ10/proyecto-BBDD-Casa-Apuestas/wiki
