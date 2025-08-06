// src/app/modules/eventos/services/eventos.service.ts
import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { environment } from '../../../environments/environment';
import {
  Evento,
  EventoCreate,
  EventoUpdate,
  EventosListResponse,
  ParticipanteEvento,
  ParticipanteEventoCreate,
  ParticipanteEventoUpdate,
  TipoEvento,
  EstadoEvento
} from '../../../shared/interfaces/eventos.interface';

@Injectable({
  providedIn: 'root'
})
export class EventosService {
  private http = inject(HttpClient);
  private baseUrl = `${environment.microservices.eventos}/api/v1/eventos`;
  
  // Estado local para reactividad
  private eventosSubject = new BehaviorSubject<Evento[]>([]);
  public eventos$ = this.eventosSubject.asObservable();

  // ==================== EVENTOS ====================

  createEvento(evento: EventoCreate): Observable<Evento> {
    return this.http.post<Evento>(this.baseUrl, evento);
  }

  getEventos(skip: number = 0, limit: number = 20): Observable<EventosListResponse> {
    const params = new HttpParams()
      .set('skip', skip.toString())
      .set('limit', limit.toString());
    
    return this.http.get<EventosListResponse>(this.baseUrl, { params });
  }

  getEvento(eventoId: string): Observable<Evento> {
    return this.http.get<Evento>(`${this.baseUrl}/${eventoId}`);
  }

  updateEvento(eventoId: string, evento: EventoUpdate): Observable<Evento> {
    return this.http.put<Evento>(`${this.baseUrl}/${eventoId}`, evento);
  }

  deleteEvento(eventoId: string): Observable<{ message: string }> {
    return this.http.delete<{ message: string }>(`${this.baseUrl}/${eventoId}`);
  }

  // ==================== PARTICIPANTES ====================

  addParticipante(eventoId: string, participante: ParticipanteEventoCreate): Observable<ParticipanteEvento> {
    return this.http.post<ParticipanteEvento>(`${this.baseUrl}/${eventoId}/participantes`, participante);
  }

  getParticipantes(eventoId: string): Observable<ParticipanteEvento[]> {
    return this.http.get<ParticipanteEvento[]>(`${this.baseUrl}/${eventoId}/participantes`);
  }

  updateParticipante(
    eventoId: string, 
    musicoId: string, 
    participante: ParticipanteEventoUpdate
  ): Observable<ParticipanteEvento> {
    return this.http.put<ParticipanteEvento>(
      `${this.baseUrl}/${eventoId}/participantes/${musicoId}`, 
      participante
    );
  }

  // ==================== CATÁLOGOS ====================

  getTiposEvento(): Observable<TipoEvento[]> {
    return this.http.get<TipoEvento[]>(`${this.baseUrl}/catalogs/tipos-evento`);
  }

  getEstadosEvento(): Observable<EstadoEvento[]> {
    return this.http.get<EstadoEvento[]>(`${this.baseUrl}/catalogs/estados-evento`);
  }

  // ==================== MÉTODOS DE ESTADO ====================

  refreshEventos(): void {
    this.getEventos().subscribe(response => {
      this.eventosSubject.next(response.eventos);
    });
  }

  // Método helper para formatear fechas
  formatDate(date: string): string {
    return new Date(date).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  // Método helper para obtener color del estado
  getEstadoColor(estadoCodigo: string): string {
    const colores: { [key: string]: string } = {
      'planificacion': 'info',
      'ensayando': 'warning',
      'completado': 'success',
      'cancelado': 'danger'
    };
    return colores[estadoCodigo] || 'secondary';
  }

  // Método helper para obtener color del tipo
  getTipoColor(tipoCodigo: string): string {
    const colores: { [key: string]: string } = {
      'concierto': 'success',
      'ensayo': 'info',
      'grabacion': 'warning',
      'otro': 'secondary'
    };
    return colores[tipoCodigo] || 'secondary';
  }
}