# Events Service API Documentation

## 📋 Descripción General

El **Servicio de Eventos** es el núcleo del Sistema de Gestión de Banda Musical. Gestiona todos los eventos musicales (conciertos, ensayos, grabaciones) y controla la participación de músicos en cada evento.

## 🎯 Responsabilidades

- **Gestión de Eventos**: Crear, actualizar, eliminar y consultar eventos musicales
- **Control de Participantes**: Invitar músicos y gestionar confirmaciones
- **Estados de Evento**: Manejar el ciclo de vida de eventos (planificación → ensayando → completado)
- **Catálogos**: Mantener tipos de evento y estados disponibles

## 🏗️ Arquitectura

### Componentes Principales

```
┌─────────────────────────────────────────────────────────┐
│                    Events Service                       │
├─────────────────────────────────────────────────────────┤
│  📡 API Layer (FastAPI)                                │
│   └── /api/v1/events/                                  │
├─────────────────────────────────────────────────────────┤
│  🧠 Service Layer                                      │
│   └── EventsService (Business Logic)                   │
├─────────────────────────────────────────────────────────┤
│  🗃️ Repository Layer                                   │
│   └── EventsRepository (Data Access)                   │
├─────────────────────────────────────────────────────────┤
│  🗄️ Database Layer (PostgreSQL)                       │
│   └── Schema: servicio_eventos                         │
└─────────────────────────────────────────────────────────┘
```

### Patrones Implementados

- **Repository Pattern**: Separación de lógica de acceso a datos
- **Service Layer**: Lógica de negocio centralizada
- **DTO Pattern**: Schemas Pydantic para validación
- **Dependency Injection**: FastAPI dependencies

## 🌐 Endpoints

### Base URL
```
http://localhost:8001/api/v1/events
```

### Autenticación
```http
Authorization: Bearer <jwt_token>
```

---

## 📊 Eventos

### `POST /`
Crear un nuevo evento musical.

**Request Body:**
```json
{
  "nombre": "Concierto de Primavera 2024",
  "descripcion": "Concierto anual de primavera en el teatro municipal",
  "lugar": "Teatro Municipal",
  "fecha_presentacion": "2024-03-21T20:00:00Z",
  "tipo_codigo": "concierto",
  "creado_por": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response (201):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "nombre": "Concierto de Primavera 2024",
  "descripcion": "Concierto anual de primavera en el teatro municipal",
  "lugar": "Teatro Municipal",
  "fecha_presentacion": "2024-03-21T20:00:00Z",
  "tipo": {
    "id": 1,
    "codigo": "concierto",
    "nombre": "Concierto",
    "descripcion": "Presentación musical en vivo"
  },
  "estado": {
    "id": 1,
    "codigo": "planificacion",
    "nombre": "En Planificación",
    "descripcion": "Evento en fase de planificación"
  },
  "creado_por": "550e8400-e29b-41d4-a716-446655440000",
  "creado_en": "2024-01-15T10:30:00Z",
  "actualizado_en": "2024-01-15T10:30:00Z",
  "eliminado_en": null
}
```

---

### `GET /`
Obtener lista de eventos con paginación.

**Query Parameters:**
- `skip` (int): Elementos a omitir (default: 0)
- `limit` (int): Elementos por página (default: 20, max: 100)

**Response (200):**
```json
{
  "eventos": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "nombre": "Concierto de Primavera 2024",
      "descripcion": "Concierto anual de primavera",
      "lugar": "Teatro Municipal",
      "fecha_presentacion": "2024-03-21T20:00:00Z",
      "tipo": {
        "id": 1,
        "codigo": "concierto",
        "nombre": "Concierto"
      },
      "estado": {
        "id": 1,
        "codigo": "planificacion",
        "nombre": "En Planificación"
      },
      "creado_por": "550e8400-e29b-41d4-a716-446655440000",
      "creado_en": "2024-01-15T10:30:00Z",
      "actualizado_en": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 1
}
```

---

### `GET /{evento_id}`
Obtener un evento específico por ID.

**Response (200):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "nombre": "Concierto de Primavera 2024",
  "descripcion": "Concierto anual de primavera",
  "lugar": "Teatro Municipal",
  "fecha_presentacion": "2024-03-21T20:00:00Z",
  "tipo": {
    "id": 1,
    "codigo": "concierto",
    "nombre": "Concierto"
  },
  "estado": {
    "id": 2,
    "codigo": "ensayando",
    "nombre": "Ensayando"
  },
  "creado_por": "550e8400-e29b-41d4-a716-446655440000",
  "creado_en": "2024-01-15T10:30:00Z",
  "actualizado_en": "2024-01-20T14:15:00Z"
}
```

---

### `PUT /{evento_id}`
Actualizar un evento existente.

**Request Body:**
```json
{
  "estado_codigo": "ensayando",
  "descripcion": "Concierto anual de primavera - Agregados más detalles"
}
```

**Response (200):** Mismo formato que GET /{evento_id}

---

### `DELETE /{evento_id}`
Eliminar un evento (soft delete).

**Response (200):**
```json
{
  "message": "Evento eliminado correctamente"
}
```

---

## 👥 Participantes

### `POST /{evento_id}/participantes`
Agregar un músico como participante del evento.

**Request Body:**
```json
{
  "musico_id": "456e7890-e89b-12d3-a456-426614174001",
  "estado_codigo": "invitado"
}
```

**Response (201):**
```json
{
  "id": "789e0123-e89b-12d3-a456-426614174002",
  "evento_id": "123e4567-e89b-12d3-a456-426614174000",
  "musico_id": "456e7890-e89b-12d3-a456-426614174001",
  "estado": {
    "id": 1,
    "codigo": "invitado",
    "nombre": "Invitado",
    "descripcion": "Músico invitado al evento"
  },
  "unido_en": "2024-01-16T09:00:00Z"
}
```

---

### `GET /{evento_id}/participantes`
Obtener todos los participantes de un evento.

**Response (200):**
```json
[
  {
    "id": "789e0123-e89b-12d3-a456-426614174002",
    "evento_id": "123e4567-e89b-12d3-a456-426614174000",
    "musico_id": "456e7890-e89b-12d3-a456-426614174001",
    "estado": {
      "id": 2,
      "codigo": "confirmado",
      "nombre": "Confirmado"
    },
    "unido_en": "2024-01-16T09:00:00Z"
  }
]
```

---

### `PUT /{evento_id}/participantes/{musico_id}`
Actualizar estado de participación de un músico.

**Request Body:**
```json
{
  "estado_codigo": "confirmado"
}
```

**Response (200):** Mismo formato que GET participantes

---

## 📚 Catálogos

### `GET /catalogs/tipos-evento`
Obtener catálogo de tipos de evento.

**Response (200):**
```json
[
  {
    "id": 1,
    "codigo": "concierto",
    "nombre": "Concierto",
    "descripcion": "Presentación musical en vivo",
    "activo": true,
    "orden": 1
  },
  {
    "id": 2,
    "codigo": "ensayo",
    "nombre": "Ensayo",
    "descripcion": "Práctica grupal",
    "activo": true,
    "orden": 2
  }
]
```

---

### `GET /catalogs/estados-evento`
Obtener catálogo de estados de evento.

**Response (200):**
```json
[
  {
    "id": 1,
    "codigo": "planificacion",
    "nombre": "En Planificación",
    "descripcion": "Evento en fase de planificación",
    "activo": true,
    "orden": 1
  },
  {
    "id": 2,
    "codigo": "ensayando",
    "nombre": "Ensayando",
    "descripcion": "Evento en fase de ensayos",
    "activo": true,
    "orden": 2
  }
]
```

---

## ❌ Códigos de Error

### Errores Comunes

| Código | Descripción | Ejemplo |
|--------|-------------|---------|
| 400 | Bad Request | Datos inválidos en el request |
| 404 | Not Found | Evento no encontrado |
| 422 | Validation Error | Error de validación Pydantic |
| 500 | Internal Server Error | Error interno del servidor |

### Formato de Error
```json
{
  "detail": "Descripción del error"
}
```

### Ejemplos Específicos

**Evento no encontrado (404):**
```json
{
  "detail": "Evento no encontrado"
}
```

**Tipo de evento inválido (400):**
```json
{
  "detail": "Tipo de evento no encontrado: tipo_invalido"
}
```

**Músico ya es participante (400):**
```json
{
  "detail": "El músico ya es participante del evento"
}
```

---

## 🔍 Casos de Uso

### 1. Crear un Evento Completo
```bash
# 1. Crear evento
curl -X POST "http://localhost:8001/api/v1/events/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Concierto de Rock",
    "lugar": "Auditorio Central",
    "fecha_presentacion": "2024-06-15T21:00:00Z",
    "tipo_codigo": "concierto",
    "creado_por": "550e8400-e29b-41d4-a716-446655440000"
  }'

# 2. Invitar músicos
curl -X POST "http://localhost:8001/api/v1/events/{evento_id}/participantes" \
  -H "Content-Type: application/json" \
  -d '{
    "musico_id": "456e7890-e89b-12d3-a456-426614174001",
    "estado_codigo": "invitado"
  }'

# 3. Confirmar participación
curl -X PUT "http://localhost:8001/api/v1/events/{evento_id}/participantes/{musico_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "estado_codigo": "confirmado"
  }'
```

### 2. Buscar Eventos Próximos
```bash
# Obtener eventos con paginación
curl "http://localhost:8001/api/v1/events/?skip=0&limit=10"
```

### 3. Cambiar Estado de Evento
```bash
# Mover evento a fase de ensayos
curl -X PUT "http://localhost:8001/api/v1/events/{evento_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "estado_codigo": "ensayando"
  }'
```

---

## 🔧 Configuración

### Variables de Entorno
```env
DATABASE_URL=postgresql://user:pass@host:port/database
DATABASE_SCHEMA=servicio_eventos
SECRET_KEY=your-secret-key
DEBUG=true
```

### Health Check
```bash
curl http://localhost:8001/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "events-service",
  "version": "1.0.0"
}
```

---

## 📖 Documentación Interactiva

Una vez que el servicio esté corriendo, puedes acceder a:

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **OpenAPI JSON**: http://localhost:8001/api/v1/openapi.json