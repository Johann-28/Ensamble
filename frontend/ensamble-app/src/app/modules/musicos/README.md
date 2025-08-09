# Módulo de Músicos - Frontend

## 📁 Estructura del Módulo

```
src/app/modules/musicos/
├── components/
│   ├── musicos-list/           # Lista de músicos con paginación y filtros
│   ├── musico-form/           # Formulario para crear/editar músicos
│   └── musico-detail/         # Vista detallada del músico
├── services/
│   └── musicos.service.ts     # Servicio para API de músicos
└── musicos.routes.ts          # Configuración de rutas del módulo
```

## 🚀 Funcionalidades Implementadas

### 📋 Lista de Músicos (`musicos-list`)
- ✅ Visualización en tabla responsiva con PrimeNG
- ✅ Paginación con configuración de elementos por página
- ✅ Búsqueda por nombre
- ✅ Filtro por estado activo/inactivo
- ✅ Acciones: Ver, Editar, Eliminar
- ✅ Vista previa de foto de perfil
- ✅ Badges para instrumentos y estado

### ✏️ Formulario de Músico (`musico-form`)
- ✅ Creación de nuevos músicos
- ✅ Edición de músicos existentes
- ✅ Validaciones reactivas con Angular Forms
- ✅ Campos: nombre, email, teléfono, estado, foto de perfil
- ✅ Vista previa de imagen
- ✅ Manejo de errores y mensajes de éxito

### 👤 Detalle de Músico (`musico-detail`)
- ✅ Vista completa de la información del músico
- ✅ Instrumentos principales y secundarios
- ✅ Estadísticas visuales (cards con iconos)
- ✅ Información de auditoría (fechas de creación/actualización)
- ✅ Acciones: Editar, Eliminar, Volver

## 🔌 Integración con Backend

### Endpoints Utilizados
```
GET    /api/v1/musicos                    # Lista de músicos
GET    /api/v1/musicos/{id}              # Músico específico
POST   /api/v1/musicos                   # Crear músico
PUT    /api/v1/musicos/{id}              # Actualizar músico
DELETE /api/v1/musicos/{id}              # Eliminar músico
GET    /api/v1/musicos/search            # Buscar músicos
GET    /api/v1/musicos/catalogs/estados-musico  # Estados de músico
```

### URL del Microservicio
- **Desarrollo**: `http://localhost:8002`
- Configurado en `environment.ts` → `microservices.musicos`

## 🎨 Componentes de PrimeNG Utilizados

- **Table** - Tabla de datos con paginación
- **Button** - Botones con iconos y efectos
- **InputText** - Campos de entrada de texto
- **Tag** - Etiquetas de estado
- **Badge** - Contadores y badges
- **Card** - Contenedores de contenido
- **Toolbar** - Barras de herramientas
- **Toast** - Mensajes de notificación
- **ConfirmDialog** - Diálogos de confirmación
- **Fieldset** - Agrupación de campos
- **Skeleton** - Estados de carga

## 🧭 Navegación

### Rutas Configuradas
```typescript
/musicos              → Redirige a /musicos/lista
/musicos/lista        → Lista de músicos
/musicos/nuevo        → Crear nuevo músico
/musicos/editar/:id   → Editar músico existente
/musicos/detalle/:id  → Ver detalles del músico
```

### Integración con Dashboard
- ✅ Módulo activo en el dashboard principal
- ✅ Navegación mediante Angular Router
- ✅ Card interactivo con estado "active"

## 📝 Uso del Módulo

### Desde el Dashboard
1. Click en el card "Músicos" en el dashboard
2. Automáticamente navega a `/musicos/lista`

### Navegación Directa
```typescript
// En cualquier componente
this.router.navigate(['/musicos']);          // → Lista
this.router.navigate(['/musicos/nuevo']);    // → Crear
this.router.navigate(['/musicos/detalle/uuid']); // → Ver
```

## 🔧 Configuración Requerida

### Backend Service
Asegúrate de que el servicio de músicos esté corriendo en el puerto 8002:
```bash
cd backend/services/musicos
uvicorn app.main:app --port 8002 --reload
```

### CORS
El backend debe permitir peticiones desde `http://localhost:4200`

## 🎯 Próximas Funcionalidades

- 🔲 Gestión de instrumentos del músico (modal)
- 🔲 Subida de imágenes para foto de perfil
- 🔲 Filtros avanzados (por instrumento, nivel)
- 🔲 Exportar lista de músicos
- 🔲 Historial de cambios
- 🔲 Integración con módulo de eventos

## ⚠️ Limitaciones Actuales

- Gestión de instrumentos del músico muestra mensaje informativo
- URLs de fotos deben ser externas (no hay subida de archivos)
- Algunos endpoints de catálogos pueden no estar implementados en el backend

## 🐛 Troubleshooting

### Error de CORS
Si aparecen errores de CORS, verifica que el backend tenga configurado:
```python
allow_origins=["http://localhost:4200"]
```

### Service No Disponible
Si el servicio no responde, verifica:
1. Puerto 8002 libre y servicio ejecutándose
2. Base de datos PostgreSQL activa
3. Variables de entorno configuradas
