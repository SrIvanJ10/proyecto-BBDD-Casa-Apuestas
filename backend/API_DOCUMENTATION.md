# API Documentation

## Overview
SportPredict REST API - Sistema de predicciones deportivas con Django + PostgreSQL + Redis + MongoDB + Neo4j

## Base URL
```
http://localhost:8000/api/
```

## Authentication
La API usa JWT (JSON Web Tokens) para autenticación.

### Obtener Token
```http
POST /api/auth/login/
Content-Type: application/json

{
  "email_or_username": "usuario@example.com",
  "password": "password123"
}
```

### Usar Token
```http
GET /api/users/profile/
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### 🔐 Authentication (`/api/auth/`)
- `POST /register/` - Registrar nuevo usuario (envía OTP)
- `POST /verify-otp/` - Verificar OTP y activar cuenta
- `POST /login/` - Login (retorna JWT token)
- `POST /logout/` - Logout
- `POST /forgot-password/` - Solicitar reset de contraseña
- `POST /reset-password/` - Resetear contraseña con OTP

### ⚽ Matches (`/api/matches/`)
- `GET /` - Listar partidos (filtros: sport, status, league, team, page, page_size)
- `GET /<id>/` - Detalle de partido
- `GET /upcoming/` - Partidos próximos
- `GET /live/` - Partidos en vivo
- `GET /finished/` - Partidos finalizados

### 🎯 Predictions (`/api/predictions/`)
- `POST /create/` - Crear predicción (requiere auth, max 10/día)
- `GET /` - Listar predicciones del usuario (requiere auth)
- `GET /<id>/` - Detalle de predicción (requiere auth)
- `PUT /<id>/update/` - Actualizar predicción (requiere auth)
- `DELETE /<id>/delete/` - Eliminar predicción (requiere auth)
- `GET /stats/` - Estadísticas de predicciones (requiere auth)
- `GET /match/<match_id>/` - Predicción para un partido específico (requiere auth)

### 👤 Users (`/api/users/`)
- `GET /profile/` - Perfil del usuario (requiere auth)
- `PUT /profile/update/` - Actualizar perfil (requiere auth)
- `GET /leaderboard/` - Ranking de usuarios
- `GET /activity/` - Historial de actividad (requiere auth)

### 📊 Analytics (`/api/analytics/`)
- `GET /dashboard/` - Métricas del dashboard
- `GET /stats/` - Estadísticas avanzadas (requiere auth)
- `GET /historical/` - Histórico de métricas (requiere auth)
- `POST /update/` - Actualizar dashboard (requiere admin)

### 💡 Recommendations (`/api/recommendations/`)
- `GET /matches/` - Partidos recomendados (requiere auth)
- `GET /users/` - Usuarios similares (requiere auth)
- `GET /trending/` - Partidos en tendencia

## Database Usage

### PostgreSQL
- Usuarios, Deportes, Equipos, Partidos, Predicciones
- Datos relacionales principales

### Redis
- Sesiones de usuario
- OTP (códigos de verificación)
- Rate limiting (10 predicciones/día)
- Caché

### MongoDB
- Logs de actividad de usuarios
- Estadísticas de partidos
- Métricas del dashboard
- Analytics

### Neo4j
- Sistema de recomendaciones (pendiente de implementación)
- Relaciones entre usuarios y contenido

## Rate Limiting
- Máximo 10 predicciones por día por usuario
- El contador se resetea a medianoche
- Controlado por Redis

## Error Responses
```json
{
  "error": "Descripción del error"
}
```

## Success Responses
Varían por endpoint, pero generalmente incluyen:
```json
{
  "message": "Operación exitosa",
  "data": { ... }
}
```
