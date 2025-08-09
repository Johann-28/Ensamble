// src/app/modules/musicos/components/musico-detail/musico-detail.component.ts

import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router, ActivatedRoute } from '@angular/router';

// PrimeNG Imports
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { TagModule } from 'primeng/tag';
import { BadgeModule } from 'primeng/badge';
import { ToolbarModule } from 'primeng/toolbar';
import { DividerModule } from 'primeng/divider';
import { FieldsetModule } from 'primeng/fieldset';
import { TableModule } from 'primeng/table';
import { ToastModule } from 'primeng/toast';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { RippleModule } from 'primeng/ripple';
import { SkeletonModule } from 'primeng/skeleton';

import { MessageService, ConfirmationService } from 'primeng/api';

import { MusicosService } from '../../services/musicos.service';
import { 
  Musico, 
  InstrumentoMusico 
} from '../../../../shared/interfaces/musicos.interface';

@Component({
  selector: 'app-musico-detail',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    CardModule,
    ButtonModule,
    TagModule,
    BadgeModule,
    ToolbarModule,
    DividerModule,
    FieldsetModule,
    TableModule,
    ToastModule,
    ConfirmDialogModule,
    RippleModule,
    SkeletonModule
  ],
  providers: [MessageService, ConfirmationService],
  templateUrl: './musico-detail.component.html',
  styleUrls: ['./musico-detail.component.scss']
})
export class MusicoDetailComponent implements OnInit {
  private router = inject(Router);
  private route = inject(ActivatedRoute);
  private musicosService = inject(MusicosService);
  private messageService = inject(MessageService);
  private confirmationService = inject(ConfirmationService);

  musico: Musico | null = null;
  loading = true;
  musicoId: string | null = null;

  ngOnInit(): void {
    this.musicoId = this.route.snapshot.paramMap.get('id');
    if (this.musicoId) {
      this.loadMusico(this.musicoId);
    } else {
      this.router.navigate(['/musicos']);
    }
  }

  loadMusico(id: string): void {
    this.loading = true;
    this.musicosService.getMusico(id).subscribe({
      next: (musico) => {
        console.log('Músico cargado:', musico);
        this.musico = musico;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading musico:', error);
        this.loading = false;
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'No se pudo cargar la información del músico'
        });
        this.router.navigate(['/musicos']);
      }
    });
  }

  editMusico(): void {
    if (this.musicoId) {
      this.router.navigate(['/musicos/editar', this.musicoId]);
    }
  }

  deleteMusico(): void {
    if (!this.musico) return;

    this.confirmationService.confirm({
      message: `¿Estás seguro de que deseas eliminar al músico ${this.musico.nombre}?`,
      header: 'Confirmar Eliminación',
      icon: 'pi pi-exclamation-triangle',
      acceptLabel: 'Sí, eliminar',
      rejectLabel: 'Cancelar',
      accept: () => {
        this.musicosService.deleteMusico(this.musico!.id).subscribe({
          next: () => {
            this.messageService.add({
              severity: 'success',
              summary: 'Éxito',
              detail: `Músico ${this.musico!.nombre} eliminado correctamente`
            });
            setTimeout(() => {
              this.router.navigate(['/musicos']);
            }, 1000);
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

  goBack(): void {
    this.router.navigate(['/musicos']);
  }

  formatDate(dateString: string): string {
    return this.musicosService.formatDate(dateString);
  }

  getEstadoSeverity(estadoCodigo: string): 'success' | 'info' | 'warn' | 'danger' | 'secondary' {
    return this.musicosService.getEstadoSeverity(estadoCodigo);
  }

  getInstrumentosPrincipales(): InstrumentoMusico[] {
    if (!this.musico) return [];
    return this.musico.instrumentos.filter(i => i.es_principal);
  }

  getInstrumentosSecundarios(): InstrumentoMusico[] {
    if (!this.musico) return [];
    return this.musico.instrumentos.filter(i => !i.es_principal);
  }

  getTiempoEnBanda(): string {
    if (!this.musico) return 'N/A';
    
    const fechaIngreso = new Date(this.musico.fecha_ingreso);
    const ahora = new Date();
    const diferencia = ahora.getTime() - fechaIngreso.getTime();
    
    const años = Math.floor(diferencia / (1000 * 60 * 60 * 24 * 365));
    const meses = Math.floor((diferencia % (1000 * 60 * 60 * 24 * 365)) / (1000 * 60 * 60 * 24 * 30));
    
    if (años > 0) {
      return meses > 0 ? `${años} años, ${meses} meses` : `${años} años`;
    } else if (meses > 0) {
      return `${meses} meses`;
    } else {
      const días = Math.floor(diferencia / (1000 * 60 * 60 * 24));
      return días > 0 ? `${días} días` : 'Menos de un día';
    }
  }

  addInstrumento(): void {
    // Esta funcionalidad se implementaría con un modal o navegación
    // Por ahora solo mostramos un mensaje
    this.messageService.add({
      severity: 'info',
      summary: 'Función no disponible',
      detail: 'La gestión de instrumentos estará disponible próximamente'
    });
  }

  onImageError(event: any): void {
    event.target.src = 'https://i.pinimg.com/originals/c6/2d/f1/c62df1afc41249d5e315fb3d6b713d53.jpg';
  }
}
