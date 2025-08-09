// src/app/modules/musicos/services/musicos.service.ts

import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { 
  Musico, 
  MusicoCreate, 
  MusicoUpdate, 
  MusicosListResponse,
  EstadoMusico,
  Instrumento,
  NivelHabilidad,
  InstrumentoMusico,
  InstrumentoMusicoCreate,
  InstrumentoMusicoUpdate
} from '../../../shared/interfaces/musicos.interface';

@Injectable({
  providedIn: 'root'
})
export class MusicosService {
  private baseUrl = `${environment.microservices.musicos}/api/v1/musicos`;

  constructor(private http: HttpClient) {}

  // ==================== MÚSICOS ====================
  
  /**
   * Obtener lista de músicos con paginación
   */
  getMusicos(skip: number = 0, limit: number = 20, activosSolo: boolean = true): Observable<MusicosListResponse> {
    let params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString())
      .set('activos_solo', activosSolo.toString());

    return this.http.get<MusicosListResponse>(this.baseUrl, { params });
  }

  /**
   * Obtener un músico específico por ID
   */
  getMusico(id: string): Observable<Musico> {
    return this.http.get<Musico>(`${this.baseUrl}/${id}`);
  }

  /**
   * Buscar músicos por nombre
   */
  searchMusicos(nombre: string, skip: number = 0, limit: number = 20): Observable<Musico[]> {
    let params = new HttpParams()
      .set('nombre', nombre)
      .set('skip', skip.toString())
      .set('limit', limit.toString());

    return this.http.get<Musico[]>(`${this.baseUrl}/search`, { params });
  }

  /**
   * Crear un nuevo músico
   */
  createMusico(musicoData: MusicoCreate): Observable<Musico> {
    return this.http.post<Musico>(this.baseUrl, musicoData);
  }

  /**
   * Actualizar un músico existente
   */
  updateMusico(id: string, musicoData: MusicoUpdate): Observable<Musico> {
    return this.http.put<Musico>(`${this.baseUrl}/${id}`, musicoData);
  }

  /**
   * Eliminar un músico (soft delete)
   */
  deleteMusico(id: string): Observable<any> {
    return this.http.delete(`${this.baseUrl}/${id}`);
  }

  // ==================== CATÁLOGOS ====================
  
  /**
   * Obtener catálogo de estados de músico
   */
  getEstadosMusico(): Observable<EstadoMusico[]> {
    return this.http.get<EstadoMusico[]>(`${this.baseUrl}/catalogs/estados-musico`);
  }

  /**
   * Obtener catálogo de instrumentos
   */
  getInstrumentos(): Observable<Instrumento[]> {
    return this.http.get<Instrumento[]>(`${environment.microservices.musicos}/api/v1/musicos/catalogs/instrumentos`);
  }

  /**
   * Obtener catálogo de niveles de habilidad
   */
  getNivelesHabilidad(): Observable<NivelHabilidad[]> {
    // Nota: Este endpoint debería estar en un servicio de catálogos
    // Por ahora asumimos que está disponible
    return this.http.get<NivelHabilidad[]>(`${this.baseUrl}/niveles-habilidad`);
  }

  // ==================== INSTRUMENTOS DEL MÚSICO ====================
  
  /**
   * Agregar un instrumento a un músico
   */
  addInstrumentoToMusico(musicoId: string, instrumentoData: InstrumentoMusicoCreate): Observable<InstrumentoMusico> {
    return this.http.post<InstrumentoMusico>(`${environment.microservices.musicos}/api/v1/musicos/${musicoId}/instrumentos`, instrumentoData);
  }

  /**
   * Actualizar un instrumento del músico
   */
  updateInstrumentoMusico(musicoId: string, instrumentoId: string, instrumentoData: InstrumentoMusicoUpdate): Observable<InstrumentoMusico> {
    return this.http.put<InstrumentoMusico>(`${environment.microservices.musicos}/api/v1/musicos/instrumentos/${instrumentoId}`, instrumentoData);
  }

  /**
   * Eliminar un instrumento del músico
   */
  removeInstrumentoFromMusico(musicoId: string, instrumentoId: string): Observable<any> {
    return this.http.delete(`${environment.microservices.musicos}/api/v1/musicos/${musicoId}/instrumentos/${instrumentoId}`);
  }

  // ==================== MÉTODOS DE UTILIDAD ====================
  
  /**
   * Formatear fecha para mostrar
   */
  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  }

  /**
   * Obtener color para el estado del músico
   */
  getEstadoColor(estadoCodigo: string): string {
    const colors: { [key: string]: string } = {
      'activo': '#10B981',
      'inactivo': '#6B7280',
      'suspendido': '#EF4444',
      'retirado': '#F59E0B'
    };
    return colors[estadoCodigo] || '#6B7280';
  }

  /**
   * Obtener severidad para tags de PrimeNG
   */
  getEstadoSeverity(estadoCodigo: string): 'success' | 'info' | 'warn' | 'danger' | 'secondary' {
    const severities: { [key: string]: any } = {
      'activo': 'success',
      'inactivo': 'secondary',
      'suspendido': 'danger',
      'retirado': 'warn'
    };
    return severities[estadoCodigo] || 'secondary';
  }
}
