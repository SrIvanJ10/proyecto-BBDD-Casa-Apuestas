# SportPredict - Planificación Completa del Proyecto

## Tabla de Contenidos
- [Descripción del Proyecto](#descripción-del-proyecto)
- [Stack Tecnológico](#stack-tecnológico)
- [Arquitectura del Sistema](#arquitectura-del-sistema)
- [División de Roles](#división-de-roles)
- [Planificación por Sprints](#planificación-por-sprints)
- [Configuración Técnica](#configuración-técnica)
- [Gestión del Proyecto](#gestión-del-proyecto)
- [Criterios de Evaluación](#criterios-de-evaluación)
- [Entregables](#entregables)
- [Gestión de Riesgos](#gestión-de-riesgos)

## Descripción del Proyecto

### Objetivo General
Desarrollar una plataforma web completa de predicciones deportivas utilizando Django integrado con múltiples sistemas de bases de datos avanzadas, contenerizada con Docker.

### Objetivos Específicos
- Demostrar competencia en el uso de bases de datos NoSQL
- Implementar casos de uso reales para cada tecnología
- Desarrollar habilidades de integración entre sistemas heterogéneos
- Aplicar buenas prácticas de desarrollo y despliegue

### Casos de Uso por Tecnología

#### Redis
- Gestión de sesiones y tokens de usuarios
- Sistema OTP (One-Time Password)
- Sistema de caché para consultas frecuentes
- Rate limiting de predicciones
- Operaciones en tiempo real (Pub/Sub)

#### MongoDB
- Almacenamiento de datos no estructurados (logs, analytics)
- Sistema de dashboards con métricas en tiempo real
- Agregaciones complejas para análisis
- CRUD completo con PyMongo

#### Neo4j
- Sistema de recomendaciones basado en grafos
- Modelado de relaciones usuario-contenido
- Consultas Cypher para análisis de patrones
- Algoritmos de recomendación colaborativa

## Stack Tecnológico

### Backend
- **Framework**: Django 4.x + Django REST Framework
- **Lenguaje**: Python 3.11
- **ORM**: Django ORM para PostgreSQL

### Frontend
- **Templates**: Django Templates
- **Estilos**: CSS3 + Bootstrap 5
- **Interactividad**: JavaScript vanilla
- **Gráficos**: Chart.js

### Bases de Datos
- **Principal**: PostgreSQL
- **Cache/Sesiones**: Redis
- **Analytics**: MongoDB
- **Recomendaciones**: Neo4j

### DevOps
- **Contenerización**: Docker + Docker Compose
- **Control de Versiones**: Git + GitHub
- **Comunicación**: Discord/Teams
- **Gestión de Proyecto**: Trello/Notion

## Arquitectura del Sistema

### Diagrama de Arquitectura

Cliente Web  
↓  
Django Application (Gunicorn)  
↓  
┌─────────────────────────────────┐  
│ PostgreSQL (Datos estructurados)│  
│ Redis (Cache/Sesiones/Colas)    │  
│ MongoDB (Analytics/Logs)        │  
│ Neo4j (Recomendaciones/Grafos)  │  
└─────────────────────────────────┘  


### Modelado de Datos

#### PostgreSQL (Modelos Django)
```python
class Usuario(AbstractUser):
    puntos_totales = models.IntegerField(default=0)
    nivel_experto = models.IntegerField(default=1)
    fecha_registro = models.DateTimeField(auto_now_add=True)

class Deporte(models.Model):
    nombre = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    deporte = models.ForeignKey(Deporte, on_delete=models.CASCADE)
    logo_url = models.URLField(blank=True)

class Partido(models.Model):
    equipo_local = models.ForeignKey(Equipo, related_name='partidos_local')
    equipo_visitante = models.ForeignKey(Equipo, related_name='partidos_visitante')
    fecha_hora = models.DateTimeField()
    resultado_final = models.CharField(max_length=10, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_PARTIDO)

class Prediccion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    prediccion = models.CharField(max_length=10)
    puntos_obtenidos = models.IntegerField(default=0)
    fecha_prediccion = models.DateTimeField(auto_now_add=True)
```

#### Redis (Estructuras de Datos)
``` python
SESSION:{user_id} → Datos de sesión usuario
PREDICTION_LIMIT:{user_id}:{date} → Contador predicciones diarias
MATCH_CACHE:{match_id} → Cache de partidos
LEADERBOARD → Sorted Set con top usuarios
OTP:{email} → Códigos de verificación
```

#### MongoDB (Colecciones)

``` javascript
// user_activity_logs
{
  user_id: ObjectId,
  action: "login|prediction|view_match",
  timestamp: ISODate(),
  metadata: { match_id: "...", prediction: "..." }
}

// analytics_dashboard
{
  date: "2025-09-15",
  total_predictions: 1500,
  success_rate: 62.5,
  active_users: 342
}
```

#### Neo4j (Modelo de Grafo)

``` cypher
(User {id: "123", name: "Luis"})-[:PREDICTED]->(Match {id: "M1"})
(User)-[:SIMILAR_TO {score: 0.85}]->(User)
(Team)-[:PLAYED_IN]->(Match)
```

## División de Roles
### Iván - Especialista BD NoSQL & DevOps
**Responsabilidades:**

- Configuración Docker y docker-compose.yml

- Redis: sesiones, OTP, cache, rate limiting

- MongoDB: agregaciones, dashboards, analytics

- Neo4j: modelado grafos, consultas Cypher, recomendaciones

- Optimización performance y troubleshooting

### Luis - Backend Lead
**Responsabilidades:**

- Desarrollo Django y APIs REST

- Modelos PostgreSQL y lógica de negocio

- Sistema de autenticación y autorización

- Integración con servicios de bases de datos

- Tests y documentación backend

### Rodrii - Frontend & UX/UI Lead
**Responsabilidades:**

- Templates Django y diseño responsive

- Experiencia de usuario e interfaz

- Integración con APIs backend

- Gráficos y visualizaciones

- Presentaciones y documentación usuario

## Planificación por Sprints
### Fase 0: Preparación (Semana 1)
**Objetivo: Aprobación del proyecto y configuración inicial**

#### Lunes
- Crear repositorio GitHub y configurar acceso

- Establecer herramientas de comunicación

- Configurar tablero de proyecto (Trello/Notion)

#### Martes
- Iván: Investigar docker-compose para múltiples BD

- Luis: Diseñar modelos iniciales PostgreSQL

- Rodrii: Crear wireframes de la aplicación

#### Miércoles
- Rodrii + Luis: Desarrollar presentación (15 slides)

- Preparar diagramas de arquitectura

- Definir casos de uso específicos

#### Jueves
- Iván: Tener docker-compose básico funcionando

- Ensayo general de presentación

- Preparar respuestas a preguntas técnicas

#### Viernes
- Presentación ante profesor (15-20 minutos)

- Recibir feedback y ajustar planificación

- Celebrar aprobación

### Sprint 1: Cimientos (Semana 2)
**Objetivo: Sistema básico funcionando con autenticación**

#### Iván:

- feat/docker-production-ready

- feat/redis-basic-setup

#### Luis:

- feat/django-initial-setup

- feat/basic-views

#### Rodrii:

- feat/base-templates

- feat/home-dashboard

#### Criterios de Aceptación
- Docker compose levanta 4 servicios sin errores

- Usuarios pueden registrarse y hacer login

- Sesiones se almacenan en Redis

- Templates base se visualizan correctamente

### Sprint 2: Core Functionality (Semana 3)
**Objetivo: Sistema de predicciones operativo + Integración MongoDB**

#### Iván:

- feat/mongodb-integration

- feat/redis-advanced

#### Luis:

- feat/prediction-system

- feat/apis-completion

#### Rodrii:

- feat/prediction-interface

- feat/analytics-ui

#### Criterios de Aceptación
- Usuarios pueden hacer predicciones (máximo 10/día)

- Sistema calcula puntos automáticamente

- MongoDB recoge logs de actividad

- Dashboard muestra métricas básicas

### Sprint 3: Inteligencia (Semana 4)
**Objetivo: Sistema de recomendaciones + Analytics avanzado + OTP**

#### Iván:

- feat/neo4j-recommendations

- feat/redis-otp-security

- feat/mongodb-advanced-analytics

#### Luis:

- feat/recommendation-apis

- feat/advanced-business-logic

#### Rodrii:

- feat/recommendations-ui

- feat/advanced-dashboard

#### Criterios de Aceptación
- Sistema recomienda partidos relevantes

- OTP funciona para registro y recuperación

- Dashboard muestra analytics avanzadas

- Consultas Cypher devuelven resultados útiles

### Sprint 4: Pulido Final (Semana 5)
**Objetivo: Sistema completo, estable y listo para entrega**

#### Iván:

- feat/performance-optimization

- feat/docker-production

#### Luis:

- feat/final-apis

- feat/code-quality

#### Rodrii:

- feat/final-ui-polish

- feat/presentation-preparation

#### Todos:

- feat/final-documentation

#### Criterios de Aceptación
- Sistema completo y estable en producción

- Performance optimizada (respuestas < 200ms)

- Documentación completa y profesional

- Presentación de defensa preparada

## Configuración Técnica
### Docker Compose

``` yaml
version: '3.8'
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: sportpredict
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  mongodb:
    image: mongo:6
    ports:
      - "27017:27017"

  neo4j:
    image: neo4j:5
    environment:
      NEO4J_AUTH: neo4j/password
    ports:
      - "7474:7474"
      - "7687:7687"

  web:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
      - mongodb
      - neo4j
```

### Estructura del Proyecto

```
sportpredict/
├── docker-compose.yml
├── .env.example
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   └── sportpredict/
│       ├── settings.py
│       ├── models.py
│       ├── views/
│       └── api/
├── frontend/
│   ├── templates/
│   ├── static/
│   └── assets/
├── documentation/
└── README.md
```

## Gestión del Proyecto
### Flujo de Trabajo Git

```
main (solo releases estables)
develop (integración continua)
├── feat/backend-* (Luis)
├── feat/frontend-* (Rodrii)
└── feat/db-* (Iván)
```

### Comandos Git Diarios
```
# Inicio del día
git checkout develop
git pull origin develop
git checkout -b feat/nombre-feature

# Durante desarrollo
git add .
git commit -m "feat: descripción concisa"
git push origin feat/nombre-feature

# Finalización
# Crear Pull Request en GitHub
# Review de 1 compañero
# Merge a develop
```

### Reuniones

#### Daily Standup (15 min diarios):

- ¿Qué hice ayer?

- ¿Qué voy a hacer hoy?

- ¿Qué problemas tengo?

#### Reuniones Técnicas (2x/semana, 30 min):

- Iván + Luis

- Coordinación modelos datos

- Problemas integración

#### Reunión Equipo (Viernes, 1 hora):

- Demo semanal

- Revisión progreso

- Planificación siguiente sprint

## Criterios de Evaluación

### Implementación Técnica (40%)
- Correcta implementación de todos los CRUD

- Integración adecuada entre sistemas

- Calidad del código y buenas prácticas

- Funcionamiento de casos de uso

### Funcionalidad (30%)
- Sistema de autenticación y sesiones

- Sistema de predicciones y puntos

- Dashboard de analytics

- Sistema de recomendaciones

### Documentación y Presentación (30%)
- Memoria técnica completa

- Documentación de arquitectura

- Presentación de defensa clara

- Calidad de exposición

## Entregables
### Código Fuente
- Repositorio GitHub con todo el código

- Docker-compose.yml funcionando

- Scripts de despliegue

- Tests automatizados

### Documentación
- Memoria técnica (15-20 páginas)

- Presentación de defensa (15-20 slides)

- README.md con guías de instalación

- Documentación de APIs

### Evidencias
- Screenshots de funcionalidades

- Videos demo de la aplicación

- Logs de ejecución sin errores

- Resultados de tests de performance

## Gestión de Riesgos
### Riesgos Técnicos
#### Docker no funciona en todas las máquinas:

- Probabilidad: Media

- Impacto: Alto

- Mitigación: Iván ayuda en configuración

- Contingencia: Desarrollo local temporal

#### Problemas de integración entre BD:

- Probabilidad: Alta

- Impacto: Alto

- Mitigación: Comunicación constante Iván-Luis

- Contingencia: APIs mock temporales

### Riesgos de Equipo
#### Falta de comunicación:

- Probabilidad: Media

- Impacto: Alto

- Mitigación: Reuniones diarias obligatorias

- Contingencia: Reasignación de tareas

#### Desfase en cronograma:

- Probabilidad: Alta

- Impacto: Alto

- Mitigación: Sprints cortos, features pequeñas

- Contingencia: Priorización features críticas

## Checklist Inicial
### Para Empezar (Día 1)
- Iván: Crear repositorio GitHub

- Iván: Invitar a Luis y Rodrii como colaboradores

- Todos: Clonar repositorio localmente

- Iván: Crear estructura inicial de carpetas

- Rodrii + Luis: Crear carpeta "presentacion_inicial"

- Iván: Empezar docker-compose.yml básico

- Todos: Configurar herramientas comunicación

### Primer Commit

``` bash
git add .
git commit -m "feat: initial project structure and docker setup"
git push origin main
```

## Consejos Finales
### Para el Éxito
- Comunicación > Perfección

- Features pequeñas > ramas gigantes

- Demo temprana > sorpresas finales

- Documentación constante > documentación última hora

### Recordatorio
**¡Vais a hacer un proyecto increíble! Este plan os garantiza:**

- Aprovechamiento máximo del tiempo

- Aprendizaje equilibrado de todas las tecnologías

- Entregable profesional y completo

- Experiencia de trabajo en equipo real