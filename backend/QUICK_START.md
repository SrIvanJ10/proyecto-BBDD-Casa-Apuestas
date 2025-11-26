# 🚀 Guía Rápida de Inicio - SportPredict

## ✅ Problemas Corregidos

1. ✅ Import de `mongo_utils` comentado (no existe)
2. ✅ PyJWT añadido a requirements.txt
3. ✅ Todas las APIs implementadas y listas

## 📋 Pasos para Probar Django

### 1. Instalar Dependencias (si no lo has hecho)

```bash
cd backend
pip install -r requirements.txt
```

### 2. Ejecutar Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Crear Superusuario (Opcional)

```bash
python manage.py createsuperuser
```

### 4. Iniciar el Servidor

```bash
python manage.py runserver 0.0.0.0:8000
```

## 🧪 Probar las APIs

### Opción 1: Usando curl

```bash
# 1. Registrar usuario
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123",
    "first_name": "Test",
    "last_name": "User"
  }'

# Respuesta incluirá un OTP (solo en desarrollo)

# 2. Verificar OTP
curl -X POST http://localhost:8000/api/auth/verify-otp/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "otp": "CODIGO_RECIBIDO"
  }'

# Respuesta incluirá el token JWT

# 3. Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email_or_username": "test@example.com",
    "password": "password123"
  }'

# 4. Ver perfil (con token)
curl -X GET http://localhost:8000/api/users/profile/ \
  -H "Authorization: Bearer TU_TOKEN_AQUI"

# 5. Listar partidos
curl -X GET http://localhost:8000/api/matches/

# 6. Dashboard analytics
curl -X GET http://localhost:8000/api/analytics/dashboard/
```

### Opción 2: Usando Postman/Insomnia

1. Importa la colección desde `API_DOCUMENTATION.md`
2. Configura el base URL: `http://localhost:8000/api/`
3. Prueba los endpoints

### Opción 3: Navegador

- Admin: http://localhost:8000/admin/
- Health: http://localhost:8000/health/
- Matches: http://localhost:8000/api/matches/
- Dashboard: http://localhost:8000/api/analytics/dashboard/

## 📊 Endpoints Disponibles

### Auth (`/api/auth/`)
- ✅ POST `/register/` - Registro con OTP
- ✅ POST `/verify-otp/` - Verificar OTP
- ✅ POST `/login/` - Login con JWT
- ✅ POST `/logout/` - Logout
- ✅ POST `/forgot-password/` - Recuperar contraseña
- ✅ POST `/reset-password/` - Resetear contraseña

### Matches (`/api/matches/`)
- ✅ GET `/` - Listar partidos
- ✅ GET `/<id>/` - Detalle partido
- ✅ GET `/upcoming/` - Próximos
- ✅ GET `/live/` - En vivo
- ✅ GET `/finished/` - Finalizados

### Predictions (`/api/predictions/`)
- ✅ POST `/create/` - Crear predicción (requiere auth)
- ✅ GET `/` - Mis predicciones (requiere auth)
- ✅ GET `/<id>/` - Detalle (requiere auth)
- ✅ PUT `/<id>/update/` - Actualizar (requiere auth)
- ✅ DELETE `/<id>/delete/` - Eliminar (requiere auth)
- ✅ GET `/stats/` - Estadísticas (requiere auth)

### Users (`/api/users/`)
- ✅ GET `/profile/` - Mi perfil (requiere auth)
- ✅ PUT `/profile/update/` - Actualizar perfil (requiere auth)
- ✅ GET `/leaderboard/` - Ranking
- ✅ GET `/activity/` - Mi actividad (requiere auth)

### Analytics (`/api/analytics/`)
- ✅ GET `/dashboard/` - Métricas
- ✅ GET `/stats/` - Estadísticas avanzadas (requiere auth)
- ✅ GET `/historical/` - Histórico (requiere auth)

### Recommendations (`/api/recommendations/`)
- ✅ GET `/matches/` - Partidos recomendados (requiere auth)
- ✅ GET `/users/` - Usuarios similares (requiere auth)
- ✅ GET `/trending/` - Trending

## ⚠️ Notas Importantes

1. **OTP en Desarrollo**: Los códigos OTP se muestran en la respuesta JSON (solo desarrollo)
2. **JWT Token**: Guarda el token del login para usarlo en requests autenticados
3. **Rate Limiting**: Máximo 10 predicciones por día (controlado por Redis)
4. **Bases de Datos**: Asegúrate de que PostgreSQL, Redis y MongoDB estén corriendo

## 🐛 Si Hay Errores

### Error: "No module named 'PyJWT'"
```bash
pip install PyJWT==2.8.0
```

### Error: "Connection refused" (Redis/MongoDB)
```bash
# Verifica que los servicios estén corriendo
docker-compose up -d redis mongodb postgres
```

### Error: "Table doesn't exist"
```bash
python manage.py migrate
```

## ✨ Siguiente Paso

Una vez que Django arranque correctamente, puedes:

1. Crear datos de prueba desde el admin
2. Probar las APIs con curl/Postman
3. Conectar el frontend React
4. Implementar Neo4j para recomendaciones avanzadas

¡Todo está listo para funcionar! 🎉
