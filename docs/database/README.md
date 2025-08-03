# Sistema de Gestión de Banda - Base de Datos PostgreSQL

## 📋 Descripción General

Este script SQL crea la estructura completa de base de datos para un Sistema de Gestión de Banda Musical. El sistema está diseñado con arquitectura de microservicios, donde cada servicio tiene su propio esquema en PostgreSQL.

## 🎯 Funcionalidades del Sistema

El sistema permite:
- Gestionar eventos musicales (conciertos, ensayos, grabaciones)
- Administrar el catálogo de canciones y sus requisitos instrumentales
- Coordinar votaciones para selección de canciones
- Registrar músicos y sus instrumentos
- Controlar disponibilidad y horarios de práctica
- Gestionar ensayos y marcar asistencia en tiempo real
- Recomendar canciones ejecutables según músicos presentes

## 🏗️ Arquitectura de Base de Datos

### Esquemas por Microservicio

1. **`servicio_eventos`** - Gestión de eventos musicales
2. **`servicio_canciones`** - Catálogo de canciones y requisitos
3. **`servicio_votacion`** - Sistema de recomendación y votación
4. **`servicio_musicos`** - Administración de músicos
5. **`servicio_disponibilidad`** - Control de disponibilidad
6. **`servicio_ensayos`** - Gestión de ensayos y asistencia

### Características Técnicas

- **UUID**: Identificadores únicos para soportar sistemas distribuidos
- **Catálogos Normalizados**: Todos los campos tipo enum tienen su tabla catálogo
- **Soft Deletes**: Campo `eliminado_en` para mantener historial
- **Auditoría**: Campos `creado_en` y `actualizado_en` con triggers automáticos
- **Arrays PostgreSQL**: Para listas de roles presentes/faltantes
- **Vistas**: Consultas prearmadas para casos de uso comunes
- **Índices**: Optimizados para consultas frecuentes

## 📦 Requisitos Previos

- PostgreSQL 12 o superior
- Extensión `uuid-ossp` (el script la instala automáticamente)
- Permisos para crear esquemas y tablas

## 🚀 Instalación

### 1. Instalación Completa

```bash
# Conectar a PostgreSQL
psql -U postgres -d mi_base_datos

# Ejecutar el script completo
\i /ruta/al/script/band_system_database.sql
```

### 2. Instalación por Microservicio

Si prefieres instalar cada servicio en bases de datos separadas:

```bash
# Extraer secciones específicas del script y ejecutar por separado
# Por ejemplo, para servicio_eventos:
psql -U postgres -d eventos_db -c "CREATE SCHEMA servicio_eventos;"
# Luego ejecutar solo la sección de servicio_eventos
```

### 3. Crear Datos de Ejemplo

```sql
-- Después de la instalación, puedes crear datos de prueba:
SELECT crear_datos_ejemplo();
```

## 📊 Estructura de Datos

### Tablas Principales por Servicio

#### servicio_eventos
- `eventos` - Eventos musicales principales
- `participantes_evento` - Músicos confirmados por evento
- Catálogos: tipos de evento, estados, estados de participante

#### servicio_canciones
- `canciones` - Catálogo de canciones
- `requisitos_cancion` - Instrumentos requeridos por canción
- `canciones_evento` - Canciones seleccionadas para cada evento
- Catálogos: niveles de dificultad, habilidad, instrumentos, estados

#### servicio_votacion
- `recomendaciones_cancion` - Sugerencias de canciones
- `votaciones` - Procesos de votación
- `votos` - Votos individuales
- Catálogos: estados de recomendación y votación

#### servicio_musicos
- `musicos` - Información de músicos
- `instrumentos_musico` - Instrumentos que toca cada músico
- Catálogos: estados de músico

#### servicio_disponibilidad
- `disponibilidad_evento` - Disponibilidad general por evento
- `disponibilidad_ensayo` - Confirmación para ensayos específicos
- `horarios_practica` - Horarios regulares de práctica
- Catálogos: tipos de disponibilidad

#### servicio_ensayos
- `ensayos` - Ensayos programados
- `asistencia_ensayo` - Registro de asistencia
- `recomendaciones_canciones_ensayo` - Canciones ejecutables según presentes
- Catálogos: estados de ensayo y asistencia

## 🔧 Configuración Post-Instalación

### 1. Crear Usuarios por Servicio

```sql
-- Crear usuarios específicos para cada microservicio
CREATE USER eventos_app WITH PASSWORD 'password_seguro';
CREATE USER canciones_app WITH PASSWORD 'password_seguro';
-- etc...

-- Asignar roles
GRANT servicio_eventos_user TO eventos_app;
GRANT servicio_canciones_user TO canciones_app;
-- etc...
```

### 2. Configurar Conexiones

Cada microservicio debe conectarse solo a su esquema:

```javascript
// Ejemplo en Node.js
const eventosDB = {
  host: 'localhost',
  database: 'band_system',
  user: 'eventos_app',
  password: 'password_seguro',
  searchPath: 'servicio_eventos'
};
```

### 3. Personalizar Catálogos

Los catálogos vienen con datos iniciales, pero puedes personalizarlos:

```sql
-- Agregar un nuevo tipo de evento
INSERT INTO servicio_eventos.cat_tipos_evento (codigo, nombre, descripcion, orden)
VALUES ('festival', 'Festival', 'Participación en festival', 5);

-- Agregar un nuevo instrumento
INSERT INTO servicio_canciones.cat_instrumentos (codigo, nombre, familia, orden)
VALUES ('ukulele', 'Ukulele', 'cuerda', 13);
```

## 📝 Ejemplos de Uso

### Crear un Evento

```sql
INSERT INTO servicio_eventos.eventos (
    nombre, 
    descripcion, 
    tipo_id, 
    lugar, 
    fecha_presentacion, 
    estado_id, 
    creado_por
) VALUES (
    'Concierto de Primavera 2024',
    'Concierto anual de primavera',
    (SELECT id FROM servicio_eventos.cat_tipos_evento WHERE codigo = 'concierto'),
    'Teatro Municipal',
    '2024-03-21 20:00:00',
    (SELECT id FROM servicio_eventos.cat_estados_evento WHERE codigo = 'planificacion'),
    'usuario-uuid-aqui'
);
```

### Registrar Asistencia a Ensayo

```sql
-- Marcar músico como presente
INSERT INTO servicio_ensayos.asistencia_ensayo (
    ensayo_id,
    musico_id,
    estado_id,
    marcado_por
) VALUES (
    'ensayo-uuid',
    'musico-uuid',
    (SELECT id FROM servicio_ensayos.cat_estados_asistencia WHERE codigo = 'presente'),
    'coordinador-uuid'
);
```

### Consultar Canciones Ejecutables

```sql
-- Ver canciones recomendadas para un ensayo
SELECT 
    c.titulo,
    c.artista,
    r.puntaje_ejecutabilidad,
    r.roles_faltantes,
    r.roles_presentes
FROM servicio_ensayos.recomendaciones_canciones_ensayo r
JOIN servicio_canciones.canciones c ON r.cancion_id = c.id
WHERE r.ensayo_id = 'ensayo-uuid'
ORDER BY r.ranking;
```

## 🔍 Vistas Útiles

El sistema incluye vistas predefinidas:

- `v_canciones_con_requisitos` - Canciones con todos sus requisitos
- `v_resumen_asistencia_ensayo` - Estadísticas de asistencia
- `v_participacion_eventos` - Resumen de confirmaciones por evento

## ⚠️ Consideraciones Importantes

### Referencias Entre Microservicios

Las foreign keys entre esquemas están comentadas como "Sin FK" porque:
- Permite que cada servicio tenga su propia base de datos
- Mantiene la independencia entre microservicios
- La consistencia se mantiene a nivel de aplicación

### Mantenimiento de Catálogos

- No eliminar registros de catálogos, usar `activo = false`
- Los códigos de catálogo no deben modificarse (son referencias en código)
- Agregar nuevos valores al final (campo `orden`)

### Respaldos

```bash
# Respaldar esquema específico
pg_dump -U postgres -d band_system -n servicio_eventos > eventos_backup.sql

# Respaldar todo
pg_dump -U postgres -d band_system > band_system_backup.sql
```

## 📈 Monitoreo y Optimización

### Consultas para Monitoreo

```sql
-- Ver tamaño de tablas
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE schemaname LIKE 'servicio_%'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Verificar uso de índices
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan
FROM pg_stat_user_indexes
WHERE schemaname LIKE 'servicio_%'
ORDER BY idx_scan;
```

## 🤝 Contribución

Para contribuir al proyecto:

1. Mantener la nomenclatura en español
2. Agregar índices para nuevas consultas frecuentes
3. Documentar cambios en catálogos
4. Incluir comentarios en tablas y columnas nuevas

## 🆘 Soporte

Para problemas o preguntas:
- Revisar logs de PostgreSQL
- Verificar permisos de usuario
- Confirmar versión de PostgreSQL compatible

---

**Versión**: 1.0.0  
**Última actualización**: 03-08-2025
**Autor**: Johann Velazquez