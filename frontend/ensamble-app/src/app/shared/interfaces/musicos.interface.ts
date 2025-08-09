// src/app/shared/interfaces/musicos.interface.ts

export interface EstadoMusico {
  id: number;
  codigo: string;
  nombre: string;
  descripcion?: string;
  activo: boolean;
  orden: number;
}

export interface Instrumento {
  id: number;
  codigo: string;
  nombre: string;
  familia?: string;
  descripcion?: string;
  activo: boolean;
  orden: number;
}

export interface NivelHabilidad {
  id: number;
  codigo: string;
  nombre: string;
  descripcion?: string;
  activo: boolean;
  orden: number;
}

export interface InstrumentoMusico {
  id: string;
  musico_id: string;
  instrumento_id: number;
  nivel_id: number;
  es_principal: boolean;
  fecha_inicio?: string;
  notas?: string;
  instrumento?: Instrumento;
  nivel?: NivelHabilidad;
}

export interface Musico {
  id: string;
  email: string;
  nombre: string;
  telefono?: string;
  fecha_ingreso: string;
  url_foto_perfil?: string;
  estado: EstadoMusico;
  instrumentos: InstrumentoMusico[];
  creado_en: string;
  actualizado_en?: string;
  eliminado_en?: string;
}

export interface MusicoCreate {
  email: string;
  nombre: string;
  telefono?: string;
  estado_codigo?: string;
  fecha_ingreso?: string;
  url_foto_perfil?: string;
}

export interface MusicoUpdate {
  email?: string;
  nombre?: string;
  telefono?: string;
  estado_codigo?: string;
  url_foto_perfil?: string;
}

export interface MusicosListResponse {
  musicos: Musico[];
  total: number;
  page: number;
  size: number;
}

export interface InstrumentoMusicoCreate {
  instrumento_id: number;
  nivel_id: number;
  es_principal?: boolean;
  fecha_inicio?: string;
  notas?: string;
}

export interface InstrumentoMusicoUpdate {
  instrumento_id?: number;
  nivel_id?: number;
  es_principal?: boolean;
  fecha_inicio?: string;
  notas?: string;
}
