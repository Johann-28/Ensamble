// src/app/modules/eventos/components/evento-detail/evento-detail.component.ts
import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, ActivatedRoute, RouterModule } from '@angular/router';

// PrimeNG Components
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { TagModule } from 'primeng/tag';
import { TableModule } from 'primeng/table';
import { DialogModule } from 'primeng/dialog';
import { InputTextModule } from 'primeng/inputtext';
import { SelectModule } from 'primeng/select';
import { ToastModule } from 'primeng/toast';
import { SkeletonModule } from 'primeng/skeleton';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { TabsModule } from 'primeng/tabs';

// Services
import { MessageService, ConfirmationService } from 'primeng/api';
import { EventosService } from '../../services/eventos.service';

// Interfaces
import { 
  Evento, 
  ParticipanteEvento, 
  ParticipanteEventoCreate,
  ParticipanteEventoUpdate 
} from '../../../../shared/interfaces/eventos.interface';
import { FormsModule, NgModel } from '@angular/forms';

@Component({
  selector: 'app-evento-detail',
  standalone: true,
  imports: [
    CommonModule,
    CardModule,
    ButtonModule,
    TagModule,
    TableModule,
    DialogModule,
    InputTextModule,
    SelectModule,
    ToastModule,
    SkeletonModule,
    ConfirmDialogModule,
    TabsModule,
    RouterModule,
    FormsModule
    
  ],
  providers: [MessageService, ConfirmationService],
  templateUrl: './evento-detail.component.html',
  styleUrls: ['./evento-detail.component.scss']
})
export class EventoDetailComponent implements OnInit {
  private router = inject(Router);
  private route = inject(ActivatedRoute);
  private eventosService = inject(EventosService);
  private messageService = inject(MessageService);
  private confirmationService = inject(ConfirmationService);

  // Estado
  evento: Evento | null = null;
  participantes: ParticipanteEvento[] = [];
  loading = true;
  loadingParticipantes = false;

  // Diálogos
  showInviteDialog = false;
  showEditParticipanteDialog = false;
  submittingInvite = false;
  submittingUpdate = false;

  // Formularios
  newParticipante = {
    musico_id: '',
    estado_codigo: 'invitado'
  };

  editingParticipante = {
    participante: null as ParticipanteEvento | null,
    estado_codigo: ''
  };

  // Catálogos
  estadosParticipante = [
    { label: 'Invitado', value: 'invitado' },
    { label: 'Confirmado', value: 'confirmado' },
    { label: 'Rechazado', value: 'rechazado' }
  ];

  ngOnInit(): void {
    const eventoId = this.route.snapshot.paramMap.get('id');
    if (eventoId) {
      this.loadEvento(eventoId);
      this.loadParticipantes(eventoId);
    }
  }

  loadEvento(eventoId: string): void {
    this.loading = true;
    this.eventosService.getEvento(eventoId).subscribe({
      next: (evento) => {
        this.evento = evento;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading evento:', error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Error al cargar el evento'
        });
        this.loading = false;
      }
    });
  }

  loadParticipantes(eventoId: string): void {
    this.loadingParticipantes = true;
    this.eventosService.getParticipantes(eventoId).subscribe({
      next: (participantes) => {
        this.participantes = participantes;
        this.loadingParticipantes = false;
      },
      error: (error) => {
        console.error('Error loading participantes:', error);
        this.loadingParticipantes = false;
      }
    });
  }

  inviteMusico(): void {
    if (!this.evento || !this.newParticipante.musico_id) return;

    this.submittingInvite = true;
    const participanteData: ParticipanteEventoCreate = {
      musico_id: this.newParticipante.musico_id,
      estado_codigo: this.newParticipante.estado_codigo
    };

    this.eventosService.addParticipante(this.evento.id, participanteData).subscribe({
      next: (participante) => {
        this.participantes.push(participante);
        this.messageService.add({
          severity: 'success',
          summary: 'Éxito',
          detail: 'Músico invitado correctamente'
        });
        this.cancelInvite();
        this.submittingInvite = false;
      },
      error: (error) => {
        console.error('Error inviting musician:', error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Error al invitar al músico'
        });
        this.submittingInvite = false;
      }
    });
  }

  editParticipante(participante: ParticipanteEvento): void {
    this.editingParticipante = {
      participante: participante,
      estado_codigo: participante.estado.codigo
    };
    this.showEditParticipanteDialog = true;
  }

  updateParticipante(): void {
    if (!this.evento || !this.editingParticipante.participante) return;

    this.submittingUpdate = true;
    const updateData: ParticipanteEventoUpdate = {
      estado_codigo: this.editingParticipante.estado_codigo
    };

    this.eventosService.updateParticipante(
      this.evento.id,
      this.editingParticipante.participante.musico_id,
      updateData
    ).subscribe({
      next: (participanteActualizado) => {
        // Actualizar en la lista local
        const index = this.participantes.findIndex(p => 
          p.musico_id === participanteActualizado.musico_id
        );
        if (index !== -1) {
          this.participantes[index] = participanteActualizado;
        }

        this.messageService.add({
          severity: 'success',
          summary: 'Éxito',
          detail: 'Estado actualizado correctamente'
        });
        this.cancelEditParticipante();
        this.submittingUpdate = false;
      },
      error: (error) => {
        console.error('Error updating participant:', error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Error al actualizar el estado'
        });
        this.submittingUpdate = false;
      }
    });
  }

  confirmRemoveParticipante(participante: ParticipanteEvento): void {
    this.confirmationService.confirm({
      message: `¿Estás seguro de que deseas remover a este participante del evento?`,
      header: 'Confirmar Eliminación',
      icon: 'pi pi-exclamation-triangle',
      acceptButtonStyleClass: 'p-button-danger',
      accept: () => {
        this.removeParticipante(participante);
      }
    });
  }

  removeParticipante(participante: ParticipanteEvento): void {
    // Nota: Esta funcionalidad requeriría implementar un endpoint DELETE
    // Por ahora solo mostramos un mensaje
    this.messageService.add({
      severity: 'info',
      summary: 'Información',
      detail: 'La funcionalidad de remover participantes estará disponible próximamente'
    });
  }

  confirmDelete(): void {
    if (!this.evento) return;

    this.confirmationService.confirm({
      message: `¿Estás seguro de que deseas eliminar el evento "${this.evento.nombre}"?`,
      header: 'Confirmar Eliminación',
      icon: 'pi pi-exclamation-triangle',
      acceptButtonStyleClass: 'p-button-danger',
      accept: () => {
        this.deleteEvento();
      }
    });
  }

  deleteEvento(): void {
    if (!this.evento) return;

    this.eventosService.deleteEvento(this.evento.id).subscribe({
      next: () => {
        this.messageService.add({
          severity: 'success',
          summary: 'Éxito',
          detail: 'Evento eliminado correctamente'
        });
        this.goBack();
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

  cancelInvite(): void {
    this.showInviteDialog = false;
    this.newParticipante = {
      musico_id: '',
      estado_codigo: 'invitado'
    };
  }

  cancelEditParticipante(): void {
    this.showEditParticipanteDialog = false;
    this.editingParticipante = {
      participante: null,
      estado_codigo: ''
    };
  }

  goBack(): void {
    this.router.navigate(['/eventos']);
  }

  // Helpers
  formatDate(dateString: string): string {
    return this.eventosService.formatDate(dateString);
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

  getParticipanteSeverity(estadoCodigo: string): 'success' | 'info' | 'warn' | 'danger' | 'secondary' | 'contrast' {
    const severities: { [key: string]: any } = {
      'invitado': 'info',
      'confirmado': 'success',
      'rechazado': 'danger'
    };
    return severities[estadoCodigo] || 'secondary';
  }

  getConfirmados(): number {
    return this.participantes.filter(p => p.estado.codigo === 'confirmado').length;
  }

  getPendientes(): number {
    return this.participantes.filter(p => p.estado.codigo === 'invitado').length;
  }
}