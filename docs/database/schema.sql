-- Sistema de Gestión de Banda - Diseño de Base de Datos PostgreSQL
-- Cada microservicio tiene su propio esquema con catálogos normalizados

-- =====================================================
-- CONFIGURACIÓN INICIAL
-- =====================================================
-- Habilitar extensión UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
SET search_path TO public, uuid_ossp;


-- Crear esquemas para cada microservicio
CREATE SCHEMA IF NOT EXISTS servicio_eventos;
CREATE SCHEMA IF NOT EXISTS servicio_canciones;
CREATE SCHEMA IF NOT EXISTS servicio_votacion;
CREATE SCHEMA IF NOT EXISTS servicio_musicos;
CREATE SCHEMA IF NOT EXISTS servicio_disponibilidad;
CREATE SCHEMA IF NOT EXISTS servicio_ensayos;

-- =====================================================
-- ESQUEMA: servicio_eventos
-- =====================================================

SET search_path TO servicio_eventos;

-- Catálogo de tipos de evento
CREATE TABLE cat_tipos_evento (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT true,
    orden INTEGER DEFAULT 1
);

-- Catálogo de estados de evento
CREATE TABLE cat_estados_evento (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT true,
    orden INTEGER DEFAULT 1
);

-- Catálogo de estados de participante
CREATE TABLE cat_estados_participante (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT true,
    orden INTEGER DEFAULT 1
);

-- Tabla de eventos
CREATE TABLE eventos (
	id UUID PRIMARY KEY DEFAULT public.uuid_generate_v4(),
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    tipo_id INTEGER NOT NULL,
    lugar VARCHAR(255),
    fecha_presentacion TIMESTAMPTZ NOT NULL,
    estado_id INTEGER NOT NULL,
    creado_por UUID NOT NULL,
    creado_en TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    eliminado_en TIMESTAMPTZ,
    CONSTRAINT fk_evento_tipo FOREIGN KEY (tipo_id) REFERENCES cat_tipos_evento(id),
    CONSTRAINT fk_evento_estado FOREIGN KEY (estado_id) REFERENCES cat_estados_evento(id)
);

-- Tabla de participantes del evento
CREATE TABLE participantes_evento (
    id UUID PRIMARY KEY DEFAULT public.uuid_generate_v4(),
    evento_id UUID NOT NULL,
    musico_id UUID NOT NULL,
    estado_id INTEGER NOT NULL,
    unido_en TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_participantes_evento FOREIGN KEY (evento_id) REFERENCES eventos(id) ON DELETE CASCADE,
    CONSTRAINT fk_participantes_estado FOREIGN KEY (estado_id) REFERENCES cat_estados_participante(id),
    CONSTRAINT uk_evento_musico UNIQUE(evento_id, musico_id)
);

-- Datos iniciales para catálogos
INSERT INTO cat_tipos_evento (codigo, nombre, descripcion, orden) VALUES
    ('concierto', 'Concierto', 'Presentación musical en vivo', 1),
    ('ensayo', 'Ensayo', 'Práctica grupal', 2),
    ('grabacion', 'Grabación', 'Sesión de grabación en estudio', 3),
    ('otro', 'Otro', 'Otro tipo de evento', 4);

INSERT INTO cat_estados_evento (codigo, nombre, descripcion, orden) VALUES
    ('planificacion', 'En Planificación', 'Evento en fase de planificación', 1),
    ('ensayando', 'Ensayando', 'Evento en fase de ensayos', 2),
    ('completado', 'Completado', 'Evento finalizado', 3),
    ('cancelado', 'Cancelado', 'Evento cancelado', 4);

INSERT INTO cat_estados_participante (codigo, nombre, descripcion, orden) VALUES
    ('invitado', 'Invitado', 'Músico invitado al evento', 1),
    ('confirmado', 'Confirmado', 'Participación confirmada', 2),
    ('rechazado', 'Rechazado', 'Invitación rechazada', 3);

-- Índices para servicio de eventos
CREATE INDEX idx_eventos_fecha_presentacion ON eventos(fecha_presentacion);
CREATE INDEX idx_eventos_estado ON eventos(estado_id);
CREATE INDEX idx_eventos_tipo ON eventos(tipo_id);
CREATE INDEX idx_participantes_evento_evento ON participantes_evento(evento_id);
CREATE INDEX idx_participantes_evento_musico ON participantes_evento(musico_id);

-- =====================================================
-- ESQUEMA: servicio_canciones
-- =====================================================


SET search_path TO servicio_canciones;

-- Catálogo de niveles de dificultad
CREATE TABLE cat_niveles_dificultad (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT true,
    orden INTEGER DEFAULT 1
);

-- Catálogo de niveles de habilidad
CREATE TABLE cat_niveles_habilidad (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT true,
    orden INTEGER DEFAULT 1
);

-- Catálogo de estados de canción en evento
CREATE TABLE cat_estados_cancion_evento (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT true,
    orden INTEGER DEFAULT 1
);


-- Tabla catálogo de canciones
CREATE TABLE canciones (
    id UUID PRIMARY KEY DEFAULT public.uuid_generate_v4(),
    titulo VARCHAR(255) NOT NULL,
    artista VARCHAR(255),
    duracion INTEGER, -- en segundos
    genero VARCHAR(100),
    dificultad_id INTEGER,
    url_partitura TEXT,
    url_audio TEXT,
    creado_en TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    eliminado_en TIMESTAMPTZ,
    CONSTRAINT fk_cancion_dificultad FOREIGN KEY (dificultad_id) REFERENCES cat_niveles_dificultad(id)
);

-- Tabla de requisitos de canciones
CREATE TABLE requisitos_cancion (
    id UUID PRIMARY KEY DEFAULT public.uuid_generate_v4(),
    cancion_id UUID NOT NULL,
    instrumento_id INTEGER NOT NULL,
    es_requerido BOOLEAN DEFAULT true,
    nivel_minimo_id INTEGER,
    notas TEXT,
    CONSTRAINT fk_requisitos_cancion FOREIGN KEY (cancion_id) REFERENCES canciones(id) ON DELETE CASCADE,
    CONSTRAINT fk_requisitos_instrumento FOREIGN KEY (instrumento_id) REFERENCES cat_instrumentos(id),
    CONSTRAINT fk_requisitos_nivel FOREIGN KEY (nivel_minimo_id) REFERENCES cat_niveles_habilidad(id),
    CONSTRAINT uk_cancion_instrumento UNIQUE(cancion_id, instrumento_id)
);

-- Tabla de canciones por evento
CREATE TABLE canciones_evento (
    id UUID PRIMARY KEY DEFAULT public.uuid_generate_v4(),
    evento_id UUID NOT NULL, -- Referencias cruzadas sin FK (microservicios)
    cancion_id UUID NOT NULL,
    estado_id INTEGER NOT NULL,
    orden_en_repertorio INTEGER,
    agregado_en TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_canciones_evento_cancion FOREIGN KEY (cancion_id) REFERENCES canciones(id) ON DELETE CASCADE,
    CONSTRAINT fk_canciones_evento_estado FOREIGN KEY (estado_id) REFERENCES cat_estados_cancion_evento(id),
    CONSTRAINT uk_evento_cancion UNIQUE(evento_id, cancion_id)
);

-- Datos iniciales para catálogos
INSERT INTO cat_niveles_dificultad (codigo, nombre, descripcion, orden) VALUES
    ('facil', 'Fácil', 'Apto para principiantes', 1),
    ('medio', 'Medio', 'Requiere experiencia moderada', 2),
    ('dificil', 'Difícil', 'Para músicos experimentados', 3);

INSERT INTO cat_niveles_habilidad (codigo, nombre, descripcion, orden) VALUES
    ('principiante', 'Principiante', 'Menos de 1 año de experiencia', 1),
    ('intermedio', 'Intermedio', '1-3 años de experiencia', 2),
    ('avanzado', 'Avanzado', 'Más de 3 años de experiencia', 3);

INSERT INTO cat_estados_cancion_evento (codigo, nombre, descripcion, orden) VALUES
    ('recomendada', 'Recomendada', 'Canción sugerida para el evento', 1),
    ('en_votacion', 'En Votación', 'En proceso de votación', 2),
    ('seleccionada', 'Seleccionada', 'Seleccionada para el repertorio', 3),
    ('rechazada', 'Rechazada', 'No seleccionada', 4);

INSERT INTO cat_instrumentos (codigo, nombre, familia, orden) VALUES
    ('voz_principal', 'Voz Principal', 'vocal', 1),
    ('voz_coro', 'Coros', 'vocal', 2),
    ('guitarra_principal', 'Guitarra Principal', 'cuerda', 3),
    ('guitarra_ritmica', 'Guitarra Rítmica', 'cuerda', 4),
    ('bajo', 'Bajo', 'cuerda', 5),
    ('bateria', 'Batería', 'percusion', 6),
    ('teclado', 'Teclado', 'teclas', 7),
    ('piano', 'Piano', 'teclas', 8),
    ('saxofon', 'Saxofón', 'viento', 9),
    ('trompeta', 'Trompeta', 'viento', 10),
    ('violin', 'Violín', 'cuerda', 11),
    ('percusion', 'Percusión', 'percusion', 12);

-- Índices para servicio de canciones
CREATE INDEX idx_canciones_titulo ON canciones(titulo);
CREATE INDEX idx_requisitos_cancion ON requisitos_cancion(cancion_id);
CREATE INDEX idx_canciones_evento_evento ON canciones_evento(evento_id);
CREATE INDEX idx_canciones_evento_estado ON canciones_evento(estado_id);

-- =====================================================
-- ESQUEMA: servicio_votacion
-- =====================================================

SET search_path TO servicio_votacion;

-- Catálogo de estados de recomendación
CREATE TABLE cat_estados_recomendacion (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT true,
    orden INTEGER DEFAULT 1
);

-- Catálogo de estados de votación
CREATE TABLE cat_estados_votacion (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT true,
    orden INTEGER DEFAULT 1
);

-- Tabla de recomendaciones de canciones
CREATE TABLE recomendaciones_cancion (
    id UUID PRIMARY KEY DEFAULT public.uuid_generate_v4(),
    evento_id UUID NOT NULL, -- Sin FK (referencia a servicio_eventos)
    cancion_id UUID NOT NULL, -- Sin FK (referencia a servicio_canciones)
    recomendado_por UUID NOT NULL, -- Sin FK (referencia a servicio_musicos)
    motivo TEXT,
    estado_id INTEGER NOT NULL,
    creado_en TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_recomendacion_estado FOREIGN KEY (estado_id) REFERENCES cat_estados_recomendacion(id)
);

-- Tabla de votaciones
CREATE TABLE votaciones (
    id UUID PRIMARY KEY DEFAULT public.uuid_generate_v4(),
    evento_id UUID NOT NULL, -- Sin FK (referencia a servicio_eventos)
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    estado_id INTEGER NOT NULL,
    fecha_inicio TIMESTAMPTZ NOT NULL,
    fecha_fin TIMESTAMPTZ NOT NULL,
    cantidad_ganadores INTEGER DEFAULT 5,
    creado_en TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_votacion_estado FOREIGN KEY (estado_id) REFERENCES cat_estados_votacion(id),
    CONSTRAINT chk_fechas_validas CHECK (fecha_fin > fecha_inicio)
);

-- Tabla de votos
CREATE TABLE votos (
    id UUID PRIMARY KEY DEFAULT public.uuid_generate_v4(),
    votacion_id UUID NOT NULL,
    recomendacion_cancion_id UUID NOT NULL,
    votante_id UUID NOT NULL, -- Sin FK (referencia a servicio_musicos)
    ranking INTEGER, -- para voto por ranking
    votado_en TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_votos_votacion FOREIGN KEY (votacion_id) REFERENCES votaciones(id) ON DELETE CASCADE,
    CONSTRAINT fk_votos_recomendacion FOREIGN KEY (recomendacion_cancion_id) REFERENCES recomendaciones_cancion(id) ON DELETE CASCADE,
    CONSTRAINT uk_votacion_votante_recomendacion UNIQUE(votacion_id, votante_id, recomendacion_cancion_id)
);

-- Datos iniciales para catálogos
INSERT INTO cat_estados_recomendacion (codigo, nombre, descripcion, orden) VALUES
    ('pendiente', 'Pendiente', 'Esperando revisión', 1),
    ('aprobada', 'Aprobada', 'Aprobada para votación', 2),
    ('rechazada', 'Rechazada', 'No aprobada para votación', 3);

INSERT INTO cat_estados_votacion (codigo, nombre, descripcion, orden) VALUES
    ('borrador', 'Borrador', 'En preparación', 1),
    ('activa', 'Activa', 'Votación en curso', 2),
    ('cerrada', 'Cerrada', 'Votación finalizada', 3);

-- Índices para servicio de votación
CREATE INDEX idx_recomendaciones_evento ON recomendaciones_cancion(evento_id);
CREATE INDEX idx_recomendaciones_estado ON recomendaciones_cancion(estado_id);
CREATE INDEX idx_votaciones_evento ON votaciones(evento_id);
CREATE INDEX idx_votaciones_estado ON votaciones(estado_id);
CREATE INDEX idx_votos_votacion ON votos(votacion_id);

-- =====================================================
-- ESQUEMA: servicio_musicos
-- =====================================================

SET search_path TO servicio_musicos;

-- Catálogo de estados de músico
CREATE TABLE cat_estados_musico (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT true,
    orden INTEGER DEFAULT 1
);

-- Tabla de músicos
CREATE TABLE musicos (
    id UUID PRIMARY KEY DEFAULT public.uuid_generate_v4(),
    email VARCHAR(255) NOT NULL UNIQUE,
    nombre VARCHAR(255) NOT NULL,
    telefono VARCHAR(50),
    fecha_ingreso TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    estado_id INTEGER NOT NULL,
    url_foto_perfil TEXT,
    creado_en TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    eliminado_en TIMESTAMPTZ,
    CONSTRAINT fk_musico_estado FOREIGN KEY (estado_id) REFERENCES cat_estados_musico(id)
);

-- Tabla de instrumentos del músico
CREATE TABLE instrumentos_musico (
    id UUID PRIMARY KEY DEFAULT public.uuid_generate_v4(),
    musico_id UUID NOT NULL,
    instrumento_id INTEGER NOT NULL, -- Referencia al catálogo compartido
    nivel_id INTEGER NOT NULL, -- Referencia al catálogo compartido
    es_principal BOOLEAN DEFAULT false,
    fecha_inicio DATE,
    notas TEXT,
    CONSTRAINT fk_instrumentos_musico FOREIGN KEY (musico_id) REFERENCES musicos(id) ON DELETE CASCADE,
    CONSTRAINT uk_musico_instrumento UNIQUE(musico_id, instrumento_id)
);

-- Catálogo de instrumentos/roles
CREATE TABLE cat_instrumentos (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    familia VARCHAR(50), -- viento, cuerda, percusión, etc.
    descripcion TEXT,
    activo BOOLEAN DEFAULT true,
    orden INTEGER DEFAULT 1
);


-- Datos iniciales para catálogos
INSERT INTO cat_estados_musico (codigo, nombre, descripcion, orden) VALUES
    ('activo', 'Activo', 'Músico activo en la banda', 1),
    ('inactivo', 'Inactivo', 'Temporalmente inactivo', 2),
    ('retirado', 'Retirado', 'Ya no forma parte de la banda', 3);

-- Índices para servicio de músicos
CREATE INDEX idx_musicos_email ON musicos(email);
CREATE INDEX idx_musicos_estado ON musicos(estado_id);
CREATE INDEX idx_instrumentos_musico ON instrumentos_musico(musico_id);

-- =====================================================
-- ESQUEMA: servicio_disponibilidad
-- =====================================================

SET search_path TO servicio_disponibilidad;

-- Catálogo de tipos de disponibilidad general
CREATE TABLE cat_tipos_disponibilidad_general (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT true,
    orden INTEGER DEFAULT 1
);

-- Catálogo de tipos de disponibilidad ensayo
CREATE TABLE cat_tipos_disponibilidad_ensayo (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT true,
    orden INTEGER DEFAULT 1
);

-- Tabla de disponibilidad por evento
CREATE TABLE disponibilidad_evento (
    id UUID PRIMARY KEY DEFAULT public.uuid_generate_v4(),
    evento_id UUID NOT NULL, -- Sin FK (referencia a servicio_eventos)
    musico_id UUID NOT NULL, -- Sin FK (referencia a servicio_musicos)
    disponibilidad_general_id INTEGER NOT NULL,
    notas TEXT,
    actualizado_en TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_disponibilidad_tipo FOREIGN KEY (disponibilidad_general_id) REFERENCES cat_tipos_disponibilidad_general(id),
    CONSTRAINT uk_evento_musico_disp UNIQUE(evento_id, musico_id)
);

-- Tabla de disponibilidad por ensayo
CREATE TABLE disponibilidad_ensayo (
    id UUID PRIMARY KEY DEFAULT public.uuid_generate_v4(),
    ensayo_id UUID NOT NULL, -- Sin FK (referencia a servicio_ensayos)
    musico_id UUID NOT NULL, -- Sin FK (referencia a servicio_musicos)
    disponibilidad_id INTEGER NOT NULL,
    motivo TEXT,
    respondido_en TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_disponibilidad_ensayo_tipo FOREIGN KEY (disponibilidad_id) REFERENCES cat_tipos_disponibilidad_ensayo(id),
    CONSTRAINT uk_ensayo_musico_disp UNIQUE(ensayo_id, musico_id)
);

-- Tabla de horarios de práctica
CREATE TABLE horarios_practica (
    id UUID PRIMARY KEY DEFAULT public.uuid_generate_v4(),
    evento_id UUID NOT NULL, -- Sin FK (referencia a servicio_eventos)
    musico_id UUID NOT NULL, -- Sin FK (referencia a servicio_musicos)
    dia_semana INTEGER NOT NULL CHECK (dia_semana BETWEEN 1 AND 7),
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    vigente_desde DATE NOT NULL,
    vigente_hasta DATE,
    creado_en TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_fechas_horario CHECK (vigente_hasta IS NULL OR vigente_hasta > vigente_desde),
    CONSTRAINT chk_horas_horario CHECK (hora_fin > hora_inicio)
);

-- Datos iniciales para catálogos
INSERT INTO cat_tipos_disponibilidad_general (codigo, nombre, descripcion, orden) VALUES
    ('completa', 'Completa', 'Disponible para todo el evento', 1),
    ('parcial', 'Parcial', 'Disponible parcialmente', 2),
    ('ninguna', 'Ninguna', 'No disponible', 3);

INSERT INTO cat_tipos_disponibilidad_ensayo (codigo, nombre, descripcion, orden) VALUES
    ('disponible', 'Disponible', 'Confirmado para asistir', 1),
    ('no_disponible', 'No Disponible', 'No puede asistir', 2),
    ('tal_vez', 'Tal Vez', 'Pendiente de confirmar', 3);

-- Índices para servicio de disponibilidad
CREATE INDEX idx_disponibilidad_evento_evento ON disponibilidad_evento(evento_id);
CREATE INDEX idx_disponibilidad_ensayo_ensayo ON disponibilidad_ensayo(ensayo_id);
CREATE INDEX idx_horarios_evento ON horarios_practica(evento_id);
CREATE INDEX idx_horarios_musico ON horarios_practica(musico_id);

-- =====================================================
-- ESQUEMA: servicio_ensayos
-- =====================================================

SET search_path TO servicio_ensayos;

-- Catálogo de estados de ensayo
CREATE TABLE cat_estados_ensayo (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT true,
    orden INTEGER DEFAULT 1
);

-- Catálogo de estados de asistencia
CREATE TABLE cat_estados_asistencia (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT true,
    orden INTEGER DEFAULT 1
);

-- Tabla de ensayos
CREATE TABLE ensayos (
    id UUID PRIMARY KEY DEFAULT public.uuid_generate_v4(),
    evento_id UUID NOT NULL, -- Sin FK (referencia a servicio_eventos)
    titulo VARCHAR(255) NOT NULL,
    fecha_programada TIMESTAMPTZ NOT NULL,
    duracion INTEGER NOT NULL, -- en minutos
    ubicacion VARCHAR(255),
    estado_id INTEGER NOT NULL,
    notas TEXT,
    creado_por UUID NOT NULL, -- Sin FK (referencia a servicio_musicos)
    creado_en TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_ensayo_estado FOREIGN KEY (estado_id) REFERENCES cat_estados_ensayo(id)
);

-- Tabla de asistencia a ensayos
CREATE TABLE asistencia_ensayo (
    id UUID PRIMARY KEY DEFAULT public.uuid_generate_v4(),
    ensayo_id UUID NOT NULL,
    musico_id UUID NOT NULL, -- Sin FK (referencia a servicio_musicos)
    estado_id INTEGER NOT NULL,
    marcado_por UUID NOT NULL, -- Sin FK (referencia a servicio_musicos)
    marcado_en TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    notas TEXT,
    CONSTRAINT fk_asistencia_ensayo FOREIGN KEY (ensayo_id) REFERENCES ensayos(id) ON DELETE CASCADE,
    CONSTRAINT fk_asistencia_estado FOREIGN KEY (estado_id) REFERENCES cat_estados_asistencia(id),
    CONSTRAINT uk_ensayo_musico_asist UNIQUE(ensayo_id, musico_id)
);

-- Tabla de recomendaciones de canciones para ensayo
CREATE TABLE recomendaciones_canciones_ensayo (
    id UUID PRIMARY KEY DEFAULT public.uuid_generate_v4(),
    ensayo_id UUID NOT NULL,
    cancion_id UUID NOT NULL, -- Sin FK (referencia a servicio_canciones)
    puntaje_ejecutabilidad DECIMAL(3,2) NOT NULL CHECK (puntaje_ejecutabilidad >= 0 AND puntaje_ejecutabilidad <= 1),
    roles_faltantes TEXT[], -- Array PostgreSQL
    roles_presentes TEXT[], -- Array PostgreSQL
    ranking INTEGER NOT NULL,
    calculado_en TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_recomendaciones_ensayo FOREIGN KEY (ensayo_id) REFERENCES ensayos(id) ON DELETE CASCADE,
    CONSTRAINT uk_ensayo_cancion UNIQUE(ensayo_id, cancion_id)
);

-- Datos iniciales para catálogos
INSERT INTO cat_estados_ensayo (codigo, nombre, descripcion, orden) VALUES
    ('programado', 'Programado', 'Ensayo programado', 1),
    ('en_progreso', 'En Progreso', 'Ensayo en curso', 2),
    ('completado', 'Completado', 'Ensayo finalizado', 3),
    ('cancelado', 'Cancelado', 'Ensayo cancelado', 4);

INSERT INTO cat_estados_asistencia (codigo, nombre, descripcion, orden) VALUES
    ('presente', 'Presente', 'Asistió al ensayo', 1),
    ('ausente', 'Ausente', 'No asistió', 2),
    ('tarde', 'Tarde', 'Llegó tarde', 3),
    ('temprano', 'Salió Temprano', 'Se retiró antes', 4);

-- Índices para servicio de ensayos
CREATE INDEX idx_ensayos_evento ON ensayos(evento_id);
CREATE INDEX idx_ensayos_fecha ON ensayos(fecha_programada);
CREATE INDEX idx_ensayos_estado ON ensayos(estado_id);
CREATE INDEX idx_asistencia_ensayo ON asistencia_ensayo(ensayo_id);
CREATE INDEX idx_recomendaciones_ensayo ON recomendaciones_canciones_ensayo(ensayo_id);
CREATE INDEX idx_recomendaciones_ranking ON recomendaciones_canciones_ensayo(ensayo_id, ranking);

-- =====================================================
-- FUNCIONES Y TRIGGERS COMUNES
-- =====================================================

-- Función para actualizar timestamp
CREATE OR REPLACE FUNCTION actualizar_columna_actualizado_en()
RETURNS TRIGGER AS $$
BEGIN
    NEW.actualizado_en = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Aplicar trigger de actualización a todas las tablas con actualizado_en
CREATE TRIGGER actualizar_eventos_actualizado_en BEFORE UPDATE ON servicio_eventos.eventos FOR EACH ROW EXECUTE FUNCTION actualizar_columna_actualizado_en();
CREATE TRIGGER actualizar_canciones_actualizado_en BEFORE UPDATE ON servicio_canciones.canciones FOR EACH ROW EXECUTE FUNCTION actualizar_columna_actualizado_en();
CREATE TRIGGER actualizar_musicos_actualizado_en BEFORE UPDATE ON servicio_musicos.musicos FOR EACH ROW EXECUTE FUNCTION actualizar_columna_actualizado_en();
CREATE TRIGGER actualizar_ensayos_actualizado_en BEFORE UPDATE ON servicio_ensayos.ensayos FOR EACH ROW EXECUTE FUNCTION actualizar_columna_actualizado_en();
CREATE TRIGGER actualizar_votaciones_actualizado_en BEFORE UPDATE ON servicio_votacion.votaciones FOR EACH ROW EXECUTE FUNCTION actualizar_columna_actualizado_en();
CREATE TRIGGER actualizar_recomendaciones_actualizado_en BEFORE UPDATE ON servicio_votacion.recomendaciones_cancion FOR EACH ROW EXECUTE FUNCTION actualizar_columna_actualizado_en();


-- =====================================================
-- COMENTARIOS EN TABLAS Y COLUMNAS
-- =====================================================

-- Comentarios para catálogos
COMMENT ON TABLE servicio_eventos.cat_tipos_evento IS 'Catálogo de tipos de eventos musicales';
COMMENT ON TABLE servicio_eventos.cat_estados_evento IS 'Catálogo de estados posibles para un evento';
COMMENT ON TABLE servicio_eventos.cat_estados_participante IS 'Catálogo de estados de participación en eventos';

COMMENT ON TABLE servicio_canciones.cat_niveles_dificultad IS 'Catálogo de niveles de dificultad para canciones';
COMMENT ON TABLE servicio_canciones.cat_niveles_habilidad IS 'Catálogo de niveles de habilidad musical';
COMMENT ON TABLE servicio_canciones.cat_instrumentos IS 'Catálogo maestro de instrumentos y roles musicales';
COMMENT ON TABLE servicio_canciones.cat_estados_cancion_evento IS 'Catálogo de estados de una canción en un evento';

COMMENT ON TABLE servicio_votacion.cat_estados_recomendacion IS 'Catálogo de estados para recomendaciones de canciones';
COMMENT ON TABLE servicio_votacion.cat_estados_votacion IS 'Catálogo de estados del proceso de votación';

COMMENT ON TABLE servicio_musicos.cat_estados_musico IS 'Catálogo de estados para músicos';

COMMENT ON TABLE servicio_disponibilidad.cat_tipos_disponibilidad_general IS 'Catálogo de tipos de disponibilidad general para eventos';
COMMENT ON TABLE servicio_disponibilidad.cat_tipos_disponibilidad_ensayo IS 'Catálogo de tipos de disponibilidad para ensayos específicos';

COMMENT ON TABLE servicio_ensayos.cat_estados_ensayo IS 'Catálogo de estados posibles para un ensayo';
COMMENT ON TABLE servicio_ensayos.cat_estados_asistencia IS 'Catálogo de estados de asistencia a ensayos';

-- Comentarios para tablas principales
COMMENT ON TABLE servicio_eventos.eventos IS 'Tabla principal de eventos musicales';
COMMENT ON TABLE servicio_canciones.canciones IS 'Catálogo de canciones disponibles';
COMMENT ON TABLE servicio_canciones.requisitos_cancion IS 'Instrumentos/roles requeridos para tocar cada canción';
COMMENT ON TABLE servicio_ensayos.ensayos IS 'Ensayos programados para cada evento';
COMMENT ON TABLE servicio_ensayos.recomendaciones_canciones_ensayo IS 'Canciones recomendadas basadas en músicos presentes';
COMMENT ON COLUMN servicio_ensayos.recomendaciones_canciones_ensayo.puntaje_ejecutabilidad IS 'Porcentaje de músicos requeridos que están presentes (0-1)';


-- =====================================================
-- VISTAS PARA CONSULTAS COMUNES
-- =====================================================

-- Vista: Canciones con todos sus requisitos
CREATE VIEW servicio_canciones.v_canciones_con_requisitos AS
SELECT 
    c.id,
    c.titulo,
    c.artista,
    nd.nombre as dificultad,
    json_agg(
        json_build_object(
            'instrumento', ci.nombre,
            'requerido', rc.es_requerido,
            'nivel_minimo', nh.nombre
        ) ORDER BY ci.orden
    ) as requisitos
FROM servicio_canciones.canciones c
LEFT JOIN servicio_canciones.cat_niveles_dificultad nd ON c.dificultad_id = nd.id
LEFT JOIN servicio_canciones.requisitos_cancion rc ON c.id = rc.cancion_id
LEFT JOIN servicio_canciones.cat_instrumentos ci ON rc.instrumento_id = ci.id
LEFT JOIN servicio_canciones.cat_niveles_habilidad nh ON rc.nivel_minimo_id = nh.id
WHERE c.eliminado_en IS NULL
GROUP BY c.id, c.titulo, c.artista, nd.nombre;

-- Vista: Resumen de asistencia a ensayos
CREATE VIEW servicio_ensayos.v_resumen_asistencia_ensayo AS
SELECT 
    e.id as ensayo_id,
    e.evento_id,
    e.fecha_programada,
    ee.nombre as estado_ensayo,
    COUNT(CASE WHEN ea.nombre = 'Presente' THEN 1 END) as cantidad_presentes,
    COUNT(CASE WHEN ea.nombre = 'Ausente' THEN 1 END) as cantidad_ausentes,
    COUNT(CASE WHEN ea.nombre = 'Tarde' THEN 1 END) as cantidad_tardes,
    COUNT(ae.id) as total_marcados
FROM servicio_ensayos.ensayos e
JOIN servicio_ensayos.cat_estados_ensayo ee ON e.estado_id = ee.id
LEFT JOIN servicio_ensayos.asistencia_ensayo ae ON e.id = ae.ensayo_id
LEFT JOIN servicio_ensayos.cat_estados_asistencia ea ON ae.estado_id = ea.id
GROUP BY e.id, e.evento_id, e.fecha_programada, ee.nombre;

-- Vista: Resumen de participación en eventos
CREATE VIEW servicio_eventos.v_participacion_eventos AS
SELECT 
    e.id as evento_id,
    e.nombre as nombre_evento,
    te.nombre as tipo_evento,
    ee.nombre as estado_evento,
    COUNT(CASE WHEN ep.codigo = 'confirmado' THEN 1 END) as cantidad_confirmados,
    COUNT(CASE WHEN ep.codigo = 'invitado' THEN 1 END) as cantidad_invitados,
    COUNT(CASE WHEN ep.codigo = 'rechazado' THEN 1 END) as cantidad_rechazados
FROM servicio_eventos.eventos e
JOIN servicio_eventos.cat_tipos_evento te ON e.tipo_id = te.id
JOIN servicio_eventos.cat_estados_evento ee ON e.estado_id = ee.id
LEFT JOIN servicio_eventos.participantes_evento pe ON e.id = pe.evento_id
LEFT JOIN servicio_eventos.cat_estados_participante ep ON pe.estado_id = ep.id
WHERE e.eliminado_en IS NULL
GROUP BY e.id, e.nombre, te.nombre, ee.nombre;
