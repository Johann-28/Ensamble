// src/app/modules/eventos/components/eventos-list/eventos-list.component.ts
import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';

// PrimeNG Components
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { TableModule } from 'primeng/table';
import { TagModule } from 'primeng/tag';
import { InputTextModule } from 'primeng/inputtext';
import { Select, SelectModule } from 'primeng/select';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { ToastModule } from 'primeng/toast';
import { SkeletonModule } from 'primeng/skeleton';
import { PaginatorModule } from 'primeng/paginator';

// Services
import { ConfirmationService, MessageService } from 'primeng/api';
import { EventosService } from '../../services/eventos.service';

// Interfaces
import { Evento, TipoEvento, EstadoEvento } from '../../../../shared/interfaces/eventos.interface';

@Component({
  selector: 'app-eventos-list',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    FormsModule,
    CardModule,
    ButtonModule,
    TableModule,
    TagModule,
    InputTextModule,
    SelectModule,
    ConfirmDialogModule,
    ToastModule,
    SkeletonModule,
    PaginatorModule
  ],
  providers: [
    ConfirmationService,
    MessageService
  ],
  templateUrl: './eventos-list.component.html',
  styleUrls : ['./eventos-list.component.scss']
})
export class EventosListComponent implements OnInit {
  private eventosService = inject(EventosService);
  private confirmationService = inject(ConfirmationService);
  private messageService = inject(MessageService);

  // Estado de la tabla
  eventos: Evento[] = [];
  loading = true;
  totalRecords = 0;
  pageSize = 20;
  first = 0;

  // Filtros
  searchTerm = '';
  selectedTipo: string | null = null;
  selectedEstado: string | null = null;

  // Catálogos
  tiposEvento: TipoEvento[] = [];
  estadosEvento: EstadoEvento[] = [];

  // Helper para skeleton loading
  loadingItems = Array.from({length: 10}, (_, i) => i);

  ngOnInit(): void {
    this.loadCatalogos();
  }

  loadCatalogos(): void {
    // Cargar tipos de evento
    this.eventosService.getTiposEvento().subscribe({
      next: (tipos) => {
        this.tiposEvento = tipos;
      },
      error: (error) => {
        console.error('Error loading tipos evento:', error);
      }
    });

    // Cargar estados de evento
    this.eventosService.getEstadosEvento().subscribe({
      next: (estados) => {
        this.estadosEvento = estados;
      },
      error: (error) => {
        console.error('Error loading estados evento:', error);
      }
    });
  }

  loadEventos(event: any): void {
    this.loading = true;
    this.first = event.first;
    this.pageSize = event.rows;

    // En una implementación real, aplicarías los filtros aquí
    this.eventosService.getEventos(this.first, this.pageSize).subscribe({
      next: (response) => {
        this.eventos = response.eventos;
        this.totalRecords = response.total;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading eventos:', error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Error al cargar los eventos'
        });
        this.loading = false;
      }
    });
  }

  onSearchChange(): void {
    // Implementar búsqueda con debounce
    this.refreshData();
  }

  onFilterChange(): void {
    // Implementar filtrado
    this.refreshData();
  }

  refreshData(): void {
    this.first = 0;
    this.loadEventos({ first: 0, rows: this.pageSize });
  }

  confirmDelete(evento: Evento): void {
    this.confirmationService.confirm({
      message: `¿Estás seguro de que deseas eliminar el evento "${evento.nombre}"?`,
      header: 'Confirmar Eliminación',
      icon: 'pi pi-exclamation-triangle',
      acceptButtonStyleClass: 'p-button-danger',
      accept: () => {
        this.deleteEvento(evento);
      }
    });
  }

  deleteEvento(evento: Evento): void {
    this.eventosService.deleteEvento(evento.id).subscribe({
      next: () => {
        this.messageService.add({
          severity: 'success',
          summary: 'Éxito',
          detail: 'Evento eliminado correctamente'
        });
        this.refreshData();
      },
      error: (error) => {
        console.error('Error deleting evento:', error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Error al eliminar el evento'
        });
      }
    });
  }

  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  }

  formatTime(dateString: string): string {
    return new Date(dateString).toLocaleTimeString('es-ES', {
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  getTipoSeverity(tipoCodigo: string): 'success' | 'info' | 'warn' | 'danger' | 'secondary' | 'contrast' {
    const severities: { [key: string]: any } = {
      'concierto': 'success',
      'ensayo': 'info',
      'grabacion': 'warn',
      'otro': 'secondary'
    };
    return severities[tipoCodigo] || 'secondary';
  }

  getEstadoSeverity(estadoCodigo: string): 'success' | 'info' | 'warn' | 'danger' | 'secondary' | 'contrast' {
    const severities: { [key: string]: any } = {
      'planificacion': 'info',
      'ensayando': 'warn',
      'completado': 'success',
      'cancelado': 'danger'
    };
    return severities[estadoCodigo] || 'secondary';
  }


  // Añadir estos métodos al EventosListComponent

// Método para verificar si hay filtros activos
hasActiveFilters(): boolean {
  return !!(this.searchTerm || this.selectedTipo || this.selectedEstado);
}

// Método para limpiar todos los filtros
clearAllFilters(): void {
  this.searchTerm = '';
  this.selectedTipo = null;
  this.selectedEstado = null;
  this.refreshData();
}

// Método para limpiar solo la búsqueda
clearSearch(): void {
  this.searchTerm = '';
  this.onSearchChange();
}

// Método para obtener el icono según el tipo de evento
getEventIcon(tipoCodigo: string): string {
  const icons: { [key: string]: string } = {
    'concierto': 'music',
    'ensayo': 'microphone',
    'grabacion': 'video',
    'otro': 'calendar'
  };
  return icons[tipoCodigo] || 'calendar';
}

// Método para obtener el icono según el estado
getStatusIcon(estadoCodigo: string): string {
  const icons: { [key: string]: string } = {
    'planificacion': 'clock',
    'ensayando': 'play',
    'completado': 'check',
    'cancelado': 'times'
  };
  return icons[estadoCodigo] || 'info-circle';
}

// También necesitas agregar estos imports al componente:

// Y en los imports del componente, cambiar:
// DropdownModule por SelectModule
}