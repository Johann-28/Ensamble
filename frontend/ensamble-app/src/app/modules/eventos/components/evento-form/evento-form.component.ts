// src/app/modules/eventos/components/evento-form/evento-form.component.ts
import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';

// PrimeNG Components
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { Select, SelectModule } from 'primeng/select';
import { DatePicker } from 'primeng/datepicker';
import { ToastModule } from 'primeng/toast';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { TextareaModule } from 'primeng/textarea';


// Services
import { MessageService } from 'primeng/api';
import { EventosService } from '../../services/eventos.service';

// Interfaces
import { EventoCreate, EventoUpdate, TipoEvento, Evento } from '../../../../shared/interfaces/eventos.interface';

@Component({
  selector: 'app-evento-form',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    CardModule,
    ButtonModule,
    InputTextModule,
    SelectModule,
    DatePicker,
    ToastModule,
    ProgressSpinnerModule,
    TextareaModule
  ],
  providers: [MessageService],
  templateUrl: './evento-form.component.html',
  styleUrls: ['./evento-form.component.scss'],
})
export class EventoFormComponent implements OnInit {
  private fb = inject(FormBuilder);
  private router = inject(Router);
  private route = inject(ActivatedRoute);
  private eventosService = inject(EventosService);
  private messageService = inject(MessageService);

  eventoForm: FormGroup;
  isEdit = false;
  eventoId: string | null = null;
  submitting = false;
  loadingEvento = false;

  // Catálogos
  tiposEvento: TipoEvento[] = [];
  estadosEvento: any[] = [];

  // Para vista previa
  selectedTipoEvento: TipoEvento | null = null;

  // Mock user ID - en producción vendría del servicio de autenticación
  private currentUserId = '550e8400-e29b-41d4-a716-446655440000';

  constructor() {
    this.eventoForm = this.fb.group({
      nombre: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(255)]],
      descripcion: [''],
      tipo_codigo: ['', Validators.required],
      estado_codigo: [''],
      lugar: ['', Validators.maxLength(255)],
      fecha_presentacion: [null, Validators.required]
    });

    // Observar cambios en tipo para vista previa
    this.eventoForm.get('tipo_codigo')?.valueChanges.subscribe(tipoCodigo => {
      this.selectedTipoEvento = this.tiposEvento.find(t => t.codigo === tipoCodigo) || null;
    });
  }

  ngOnInit(): void {
    this.checkEditMode();
    this.loadCatalogos();
  }

  checkEditMode(): void {
    this.eventoId = this.route.snapshot.paramMap.get('id');
    this.isEdit = !!this.eventoId && this.router.url.includes('editar');

    if (this.isEdit && this.eventoId) {
      this.loadEvento();
    }
  }

  loadCatalogos(): void {
    // Cargar tipos de evento
    this.eventosService.getTiposEvento().subscribe({
      next: (tipos) => {
        this.tiposEvento = tipos;
      },
      error: (error) => {
        console.error('Error loading tipos evento:', error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Error al cargar los tipos de evento'
        });
      }
    });

    // Cargar estados de evento (solo para edición)
    if (this.isEdit) {
      this.eventosService.getEstadosEvento().subscribe({
        next: (estados) => {
          this.estadosEvento = estados;
        },
        error: (error) => {
          console.error('Error loading estados evento:', error);
        }
      });
    }
  }

  loadEvento(): void {
    if (!this.eventoId) return;

    this.loadingEvento = true;
    this.eventosService.getEvento(this.eventoId).subscribe({
      next: (evento) => {
        this.populateForm(evento);
        this.loadingEvento = false;
      },
      error: (error) => {
        console.error('Error loading evento:', error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Error al cargar el evento'
        });
        this.loadingEvento = false;
        this.goBack();
      }
    });
  }

  populateForm(evento: Evento): void {
    this.eventoForm.patchValue({
      nombre: evento.nombre,
      descripcion: evento.descripcion,
      tipo_codigo: evento.tipo.codigo,
      estado_codigo: evento.estado.codigo,
      lugar: evento.lugar,
      fecha_presentacion: new Date(evento.fecha_presentacion)
    });
  }

  onSubmit(): void {
    if (this.eventoForm.invalid) {
      this.markAllFieldsAsTouched();
      return;
    }

    this.submitting = true;

    if (this.isEdit) {
      this.updateEvento();
    } else {
      this.createEvento();
    }
  }

  createEvento(): void {
    const formValue = this.eventoForm.value;
    const eventoData: EventoCreate = {
      nombre: formValue.nombre,
      descripcion: formValue.descripcion || undefined,
      tipo_codigo: formValue.tipo_codigo,
      lugar: formValue.lugar || undefined,
      fecha_presentacion: formValue.fecha_presentacion.toISOString(),
      creado_por: this.currentUserId
    };

    this.eventosService.createEvento(eventoData).subscribe({
      next: (evento) => {
        this.messageService.add({
          severity: 'success',
          summary: 'Éxito',
          detail: 'Evento creado correctamente'
        });
        this.submitting = false;
        this.router.navigate(['/eventos', evento.id]);
      },
      error: (error) => {
        console.error('Error creating evento:', error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Error al crear el evento'
        });
        this.submitting = false;
      }
    });
  }

  updateEvento(): void {
    if (!this.eventoId) return;

    const formValue = this.eventoForm.value;
    const eventoData: EventoUpdate = {
      nombre: formValue.nombre,
      descripcion: formValue.descripcion || undefined,
      tipo_codigo: formValue.tipo_codigo,
      estado_codigo: formValue.estado_codigo,
      lugar: formValue.lugar || undefined,
      fecha_presentacion: formValue.fecha_presentacion.toISOString()
    };

    this.eventosService.updateEvento(this.eventoId, eventoData).subscribe({
      next: (evento) => {
        this.messageService.add({
          severity: 'success',
          summary: 'Éxito',
          detail: 'Evento actualizado correctamente'
        });
        this.submitting = false;
        this.router.navigate(['/eventos', evento.id]);
      },
      error: (error) => {
        console.error('Error updating evento:', error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Error al actualizar el evento'
        });
        this.submitting = false;
      }
    });
  }

  goBack(): void {
    if (this.isEdit && this.eventoId) {
      this.router.navigate(['/eventos', this.eventoId]);
    } else {
      this.router.navigate(['/eventos']);
    }
  }

  isFieldInvalid(fieldName: string): boolean {
    const field = this.eventoForm.get(fieldName);
    return !!(field && field.invalid && (field.dirty || field.touched));
  }

  markAllFieldsAsTouched(): void {
    Object.keys(this.eventoForm.controls).forEach(key => {
      this.eventoForm.get(key)?.markAsTouched();
    });
  }

  formatPreviewDate(date: Date): string {
    if (!date) return '';
    return date.toLocaleDateString('es-ES', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }
}