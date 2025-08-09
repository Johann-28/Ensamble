// src/app/modules/musicos/components/musicos-list/musicos-list.component.ts

import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';

// PrimeNG Imports
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { TagModule } from 'primeng/tag';
import { PaginatorModule } from 'primeng/paginator';
import { CardModule } from 'primeng/card';
import { ToolbarModule } from 'primeng/toolbar';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { ToastModule } from 'primeng/toast';
import { RippleModule } from 'primeng/ripple';
import { BadgeModule } from 'primeng/badge';
import { TooltipModule } from 'primeng/tooltip';

import { ConfirmationService, MessageService } from 'primeng/api';

import { MusicosService } from '../../services/musicos.service';
import { Musico, EstadoMusico } from '../../../../shared/interfaces/musicos.interface';

@Component({
  selector: 'app-musicos-list',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    FormsModule,
    TableModule,
    ButtonModule,
    InputTextModule,
    TagModule,
    PaginatorModule,
    CardModule,
    ToolbarModule,
    ConfirmDialogModule,
    ToastModule,
    RippleModule,
    BadgeModule,
    TooltipModule
  ],
  providers: [ConfirmationService, MessageService],
  templateUrl: './musicos-list.component.html',
  styleUrls: ['./musicos-list.component.scss']
})
export class MusicosListComponent implements OnInit {
  private musicosService = inject(MusicosService);
  private confirmationService = inject(ConfirmationService);
  private messageService = inject(MessageService);

  // Datos
  musicos: Musico[] = [];
  estadosMusico: EstadoMusico[] = [];
  
  // Estado de carga
  loading = true;
  
  // Paginación
  totalRecords = 0;
  currentPage = 0;
  rows = 20;
  
  // Filtros
  searchTerm = '';
  selectedEstado: EstadoMusico | null = null;
  activosSolo = true;

  ngOnInit(): void {
    this.loadEstados();
    this.loadMusicos();
  }

  loadEstados(): void {
    this.musicosService.getEstadosMusico().subscribe({
      next: (estados) => {
        this.estadosMusico = estados;
      },
      error: (error) => {
        console.error('Error loading estados:', error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'No se pudieron cargar los estados'
        });
      }
    });
  }

  loadMusicos(): void {
    this.loading = true;
    const skip = this.currentPage * this.rows;
    
    this.musicosService.getMusicos(skip, this.rows, this.activosSolo).subscribe({
      next: (response) => {
        this.musicos = response.musicos;
        this.totalRecords = response.total;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading musicos:', error);
        this.loading = false;
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'No se pudieron cargar los músicos'
        });
      }
    });
  }

  onPageChange(event: any): void {
    this.currentPage = event.page;
    this.rows = event.rows;
    this.loadMusicos();
  }

  search(): void {
    if (this.searchTerm.trim()) {
      this.musicosService.searchMusicos(this.searchTerm, 0, 100).subscribe({
        next: (musicos) => {
          this.musicos = musicos;
          this.totalRecords = musicos.length;
          this.loading = false;
        },
        error: (error) => {
          console.error('Error searching musicos:', error);
          this.messageService.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Error en la búsqueda'
          });
        }
      });
    } else {
      this.currentPage = 0;
      this.loadMusicos();
    }
  }

  clearSearch(): void {
    this.searchTerm = '';
    this.selectedEstado = null;
    this.currentPage = 0;
    this.loadMusicos();
  }

  filterByEstado(): void {
    // Esta funcionalidad requeriría modificar el servicio backend
    // Por ahora solo recargamos los datos
    this.currentPage = 0;
    this.loadMusicos();
  }

  toggleActivos(): void {
    this.activosSolo = !this.activosSolo;
    this.currentPage = 0;
    this.loadMusicos();
  }

  deleteMusico(musico: Musico): void {
    this.confirmationService.confirm({
      message: `¿Estás seguro de que deseas eliminar al músico ${musico.nombre}?`,
      header: 'Confirmar Eliminación',
      icon: 'pi pi-exclamation-triangle',
      acceptLabel: 'Sí, eliminar',
      rejectLabel: 'Cancelar',
      accept: () => {
        this.musicosService.deleteMusico(musico.id).subscribe({
          next: () => {
            this.messageService.add({
              severity: 'success',
              summary: 'Éxito',
              detail: `Músico ${musico.nombre} eliminado correctamente`
            });
            this.loadMusicos();
          },
          error: (error) => {
            console.error('Error deleting musico:', error);
            this.messageService.add({
              severity: 'error',
              summary: 'Error',
              detail: 'No se pudo eliminar el músico'
            });
          }
        });
      }
    });
  }

  formatDate(dateString: string): string {
    return this.musicosService.formatDate(dateString);
  }

  getEstadoSeverity(estadoCodigo: string): 'success' | 'info' | 'warn' | 'danger' | 'secondary' {
    return this.musicosService.getEstadoSeverity(estadoCodigo);
  }

  getInstrumentosPrincipales(musico: Musico): string {
    const principales = musico.instrumentos
      .filter(i => i.es_principal)
      .map(i => i.instrumento?.nombre || 'N/A')
      .join(', ');
    
    return principales || 'Sin instrumentos principales';
  }

  getTotalInstrumentos(musico: Musico): number {
    return musico.instrumentos.length;
  }

  onImageError(event: any): void {
    event.target.src = 'https://i.pinimg.com/originals/c6/2d/f1/c62df1afc41249d5e315fb3d6b713d53.jpg';
  }
}
