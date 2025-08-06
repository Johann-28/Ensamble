export interface CatalogoBase {
  id: number;
  codigo: string;
  nombre: string;
  descripcion?: string;
  activo: boolean;
  orden: number;
}

export interface TipoEvento extends CatalogoBase {}
export interface EstadoEvento extends CatalogoBase {}
export interface EstadoParticipante extends CatalogoBase {}

export interface EventoBase {
  nombre: string;
  descripcion?: string;
  lugar?: string;
  fecha_presentacion: string;
}

export interface EventoCreate extends EventoBase {
  tipo_codigo: string;
  creado_por: string;
}

export interface EventoUpdate {
  nombre?: string;
  descripcion?: string;
  lugar?: string;
  fecha_presentacion?: string;
  tipo_codigo?: string;
  estado_codigo?: string;
}

export interface Evento extends EventoBase {
  id: string;
  tipo: TipoEvento;
  estado: EstadoEvento;
  creado_por: string;
  creado_en: string;
  actualizado_en: string;
  eliminado_en?: string;
}

export interface ParticipanteEventoCreate {
  musico_id: string;
  estado_codigo?: string;
}

export interface ParticipanteEventoUpdate {
  estado_codigo: string;
}

export interface ParticipanteEvento {
  id: string;
  evento_id: string;
  musico_id: string;
  estado: EstadoParticipante;
  unido_en: string;
}

export interface EventosListResponse {
  eventos: Evento[];
  total: number;
  page: number;
  size: number;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}