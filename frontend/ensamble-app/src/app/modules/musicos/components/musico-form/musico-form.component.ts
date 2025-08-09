// src/app/modules/musicos/components/musico-form/musico-form.component.ts

import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule, FormsModule } from '@angular/forms';

// PrimeNG Imports
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { ToastModule } from 'primeng/toast';
import { ToolbarModule } from 'primeng/toolbar';
import { DividerModule } from 'primeng/divider';
import { FieldsetModule } from 'primeng/fieldset';
import { RippleModule } from 'primeng/ripple';
import { TableModule } from 'primeng/table';
import { CheckboxModule } from 'primeng/checkbox';
import { DialogModule } from 'primeng/dialog';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { TooltipModule } from 'primeng/tooltip';

import { MessageService, ConfirmationService } from 'primeng/api';

import { MusicosService } from '../../services/musicos.service';
import { 
  Musico, 
  MusicoCreate, 
  MusicoUpdate, 
  EstadoMusico,
  Instrumento,
  NivelHabilidad,
  InstrumentoMusico,
  InstrumentoMusicoCreate,
  InstrumentoMusicoUpdate
} from '../../../../shared/interfaces/musicos.interface';
import { SelectModule } from 'primeng/select';
import { DatePicker } from "primeng/datepicker";

@Component({
  selector: 'app-musico-form',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    ReactiveFormsModule,
    CardModule,
    ButtonModule,
    InputTextModule,
    ToastModule,
    ToolbarModule,
    DividerModule,
    FieldsetModule,
    RippleModule,
    TableModule,
    CheckboxModule,
    DialogModule,
    ConfirmDialogModule,
    TooltipModule,
    SelectModule,
    FormsModule,
    DatePicker
],
  providers: [MessageService, ConfirmationService],
  templateUrl: './musico-form.component.html',
  styleUrls: ['./musico-form.component.scss']
})
export class MusicoFormComponent implements OnInit {
  private fb = inject(FormBuilder);
  private router = inject(Router);
  private route = inject(ActivatedRoute);
  private musicosService = inject(MusicosService);
  private messageService = inject(MessageService);
  private confirmationService = inject(ConfirmationService);

  musicoForm!: FormGroup;
  isEditMode = false;
  musicoId: string | null = null;
  loading = false;
  estados: EstadoMusico[] = [];
  
  // Para gestión de instrumentos
  instrumentos: Instrumento[] = [];
  nivelesHabilidad: NivelHabilidad[] = [];
  currentMusico: Musico | null = null;
  
  // Dialog de instrumentos
  showInstrumentoDialog = false;
  isEditingInstrumento = false;
  currentInstrumento: InstrumentoMusico | null = null;
  instrumentoForm!: FormGroup;

  ngOnInit(): void {
    this.initForm();
    this.initInstrumentoForm();
    this.loadEstados();
    this.loadInstrumentos();
    this.loadNivelesHabilidad();
    
    // Verificar si estamos en modo edición
    this.musicoId = this.route.snapshot.paramMap.get('id');
    this.isEditMode = !!this.musicoId;

    if (this.isEditMode && this.musicoId) {
      this.loadMusico(this.musicoId);
    }
  }

  initForm(): void {
    this.musicoForm = this.fb.group({
      nombre: ['', [Validators.required, Validators.minLength(2), Validators.maxLength(255)]],
      email: ['', [Validators.required, Validators.email]],
      telefono: ['', [Validators.maxLength(50)]],
      estado_codigo: ['activo', [Validators.required]],
      url_foto_perfil: [''],
      fecha_ingreso: [new Date()]
    });
  }

  initInstrumentoForm(): void {
    this.instrumentoForm = this.fb.group({
      instrumento_id: ['', [Validators.required]],
      nivel_id: [0, [Validators.required]],
      es_principal: [false],
      fecha_inicio: [''],
      notas: ['']
    });
  }

  loadEstados(): void {
    this.musicosService.getEstadosMusico().subscribe({
      next: (estados) => {
        this.estados = estados;
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

  loadInstrumentos(): void {
    this.musicosService.getInstrumentos().subscribe({
      next: (instrumentos) => {
        this.instrumentos = instrumentos;
      },
      error: (error) => {
        console.error('Error loading instrumentos:', error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'No se pudieron cargar los instrumentos'
        });
      }
    });
  }

  loadNivelesHabilidad(): void {
    // Por ahora creamos niveles fijos, después se puede hacer dinámico
    this.nivelesHabilidad = [
      { id: 0, codigo: 'principiante', nombre: 'Principiante', activo: true, orden: 1 },
      { id: 1, codigo: 'intermedio', nombre: 'Intermedio', activo: true, orden: 2 },
      { id: 2, codigo: 'avanzado', nombre: 'Avanzado', activo: true, orden: 3 },
      { id: 3, codigo: 'experto', nombre: 'Experto', activo: true, orden: 4 }
    ];
  }

  loadMusico(id: string): void {
    this.loading = true;
    this.musicosService.getMusico(id).subscribe({
      next: (musico) => {
        this.currentMusico = musico;
        this.populateForm(musico);
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

  populateForm(musico: Musico): void {
    this.musicoForm.patchValue({
      nombre: musico.nombre,
      email: musico.email,
      telefono: musico.telefono,
      estado_codigo: musico.estado.codigo,
      url_foto_perfil: musico.url_foto_perfil,
      fecha_ingreso: new Date(musico.fecha_ingreso)
    });
  }

  onSubmit(): void {
    if (this.musicoForm.valid) {
      this.loading = true;
      
      const formData = this.musicoForm.value;
      
      if (this.isEditMode && this.musicoId) {
        this.updateMusico(formData);
      } else {
        this.createMusico(formData);
      }
    } else {
      this.markFormGroupTouched();
      this.messageService.add({
        severity: 'warn',
        summary: 'Formulario inválido',
        detail: 'Por favor, corrige los errores en el formulario'
      });
    }
  }

  createMusico(formData: any): void {
    const musicoData: MusicoCreate = {
      nombre: formData.nombre,
      email: formData.email,
      telefono: formData.telefono || undefined,
      estado_codigo: formData.estado_codigo,
      url_foto_perfil: formData.url_foto_perfil || undefined,
      fecha_ingreso: formData.fecha_ingreso?.toISOString()
    };

    this.musicosService.createMusico(musicoData).subscribe({
      next: (musico) => {
        this.loading = false;
        this.messageService.add({
          severity: 'success',
          summary: 'Éxito',
          detail: `Músico ${musico.nombre} creado correctamente`
        });
        setTimeout(() => {
          this.router.navigate(['/musicos/detalle', musico.id]);
        }, 1000);
      },
      error: (error) => {
        this.loading = false;
        console.error('Error creating musico:', error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'No se pudo crear el músico'
        });
      }
    });
  }

  updateMusico(formData: any): void {
    const musicoData: MusicoUpdate = {
      nombre: formData.nombre,
      email: formData.email,
      telefono: formData.telefono || undefined,
      estado_codigo: formData.estado_codigo,
      url_foto_perfil: formData.url_foto_perfil || undefined
    };

    this.musicosService.updateMusico(this.musicoId!, musicoData).subscribe({
      next: (musico) => {
        this.loading = false;
        this.messageService.add({
          severity: 'success',
          summary: 'Éxito',
          detail: `Músico ${musico.nombre} actualizado correctamente`
        });
        setTimeout(() => {
          this.router.navigate(['/musicos/detalle', musico.id]);
        }, 1000);
      },
      error: (error) => {
        this.loading = false;
        console.error('Error updating musico:', error);
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'No se pudo actualizar el músico'
        });
      }
    });
  }

  onCancel(): void {
    if (this.isEditMode && this.musicoId) {
      this.router.navigate(['/musicos/detalle', this.musicoId]);
    } else {
      this.router.navigate(['/musicos']);
    }
  }

  private markFormGroupTouched(): void {
    Object.keys(this.musicoForm.controls).forEach(key => {
      const control = this.musicoForm.get(key);
      control?.markAsTouched();
    });
  }

  // ==================== GESTIÓN DE INSTRUMENTOS ====================

  openInstrumentoDialog(): void {
    this.isEditingInstrumento = false;
    this.currentInstrumento = null;
    this.instrumentoForm.reset({
      instrumento_id: '',
      nivel_id: 0,
      es_principal: false,
      fecha_inicio: '',
      notas: ''
    });
    this.showInstrumentoDialog = true;
  }

  editInstrumento(instrumento: InstrumentoMusico): void {
    this.isEditingInstrumento = true;
    this.currentInstrumento = instrumento;
    this.instrumentoForm.patchValue({
      instrumento_id: instrumento.instrumento_id,
      nivel_id: instrumento.nivel_id,
      es_principal: instrumento.es_principal,
      fecha_inicio: instrumento.fecha_inicio || '',
      notas: instrumento.notas || ''
    });
    this.showInstrumentoDialog = true;
  }

  saveInstrumento(): void {
    if (this.instrumentoForm.valid && this.musicoId) {
      const formData = this.instrumentoForm.value;
      
      // Validar que no se esté agregando un instrumento duplicado
      if (!this.isEditingInstrumento) {
        const instrumentoExistente = this.currentMusico?.instrumentos.find(
          inst => inst.instrumento_id === formData.instrumento_id
        );
        if (instrumentoExistente) {
          this.messageService.add({
            severity: 'warn',
            summary: 'Advertencia',
            detail: 'Este músico ya tiene registrado este instrumento'
          });
          return;
        }
      } else if (this.currentInstrumento) {
        // Al editar, verificar que no hay otro instrumento con el mismo instrumento_id
        const instrumentoExistente = this.currentMusico?.instrumentos.find(
          inst => inst.instrumento_id === formData.instrumento_id && inst.id !== this.currentInstrumento!.id
        );
        if (instrumentoExistente) {
          this.messageService.add({
            severity: 'warn',
            summary: 'Advertencia',
            detail: 'Este músico ya tiene registrado este instrumento'
          });
          return;
        }
      }
      
      const instrumentoData: InstrumentoMusicoCreate = {
        instrumento_id: formData.instrumento_id,
        nivel_id: formData.nivel_id,
        es_principal: formData.es_principal || false,
        fecha_inicio: formData.fecha_inicio || undefined,
        notas: formData.notas || undefined
      };

      if (this.isEditingInstrumento && this.currentInstrumento) {
        // Actualizar instrumento existente
        this.musicosService.updateInstrumentoMusico(
          this.musicoId,
          this.currentInstrumento.id,
          instrumentoData
        ).subscribe({
          next: () => {
            this.messageService.add({
              severity: 'success',
              summary: 'Éxito',
              detail: 'Instrumento actualizado correctamente'
            });
            this.loadMusico(this.musicoId!);
            this.showInstrumentoDialog = false;
          },
          error: (error) => {
            console.error('Error updating instrumento:', error);
            let errorMessage = 'No se pudo actualizar el instrumento';
            
            if (error.status === 409) {
              errorMessage = error.error?.detail || 'Este músico ya tiene este instrumento registrado';
            }
            
            this.messageService.add({
              severity: 'error',
              summary: 'Error',
              detail: errorMessage
            });
          }
        });
      } else {
        // Crear nuevo instrumento
        this.musicosService.addInstrumentoToMusico(this.musicoId, instrumentoData).subscribe({
          next: () => {
            this.messageService.add({
              severity: 'success',
              summary: 'Éxito',
              detail: 'Instrumento agregado correctamente'
            });
            this.loadMusico(this.musicoId!);
            this.showInstrumentoDialog = false;
          },
          error: (error) => {
            console.error('Error adding instrumento:', error);
            let errorMessage = 'No se pudo agregar el instrumento';
            
            if (error.status === 409) {
              errorMessage = error.error?.detail || 'Este músico ya tiene este instrumento registrado';
            }
            
            this.messageService.add({
              severity: 'error',
              summary: 'Error',
              detail: errorMessage
            });
          }
        });
      }
    }
  }

  deleteInstrumento(instrumento: InstrumentoMusico): void {
    this.confirmationService.confirm({
      message: `¿Estás seguro de eliminar este instrumento?`,
      header: 'Confirmar Eliminación',
      icon: 'pi pi-exclamation-triangle',
      accept: () => {
        if (this.musicoId) {
          this.musicosService.removeInstrumentoFromMusico(this.musicoId, instrumento.id).subscribe({
            next: () => {
              this.messageService.add({
                severity: 'success',
                summary: 'Éxito',
                detail: 'Instrumento eliminado correctamente'
              });
              this.loadMusico(this.musicoId!);
            },
            error: (error) => {
              console.error('Error deleting instrumento:', error);
              this.messageService.add({
                severity: 'error',
                summary: 'Error',
                detail: 'No se pudo eliminar el instrumento'
              });
            }
          });
        }
      }
    });
  }

  getInstrumentoNombre(instrumentoId: number): string {
    const instrumento = this.instrumentos.find(i => i.id === instrumentoId);
    return instrumento?.nombre || 'Desconocido';
  }

  getNivelNombre(nivelId: number): string {
    const nivel = this.nivelesHabilidad.find(n => n.id === nivelId);
    return nivel?.nombre || 'Desconocido';
  }

  getNivelSeverity(nivelId: number): string {
    const nivel = this.nivelesHabilidad.find(n => n.id === nivelId);
    if (!nivel) return 'info';
    
    // Asignar severidad basada en el nivel
    const levelName = nivel.nombre.toLowerCase();
    if (levelName.includes('principiante') || levelName.includes('básico')) {
      return 'info';
    } else if (levelName.includes('intermedio') || levelName.includes('medio')) {
      return 'warning';
    } else if (levelName.includes('avanzado') || levelName.includes('experto') || levelName.includes('profesional')) {
      return 'success';
    } else if (levelName.includes('maestro') || levelName.includes('virtuoso')) {
      return 'danger';
    }
    return 'info';
  }

   onImageError(event: any): void {
    event.target.src = 'https://i.pinimg.com/originals/c6/2d/f1/c62df1afc41249d5e315fb3d6b713d53.jpg';
  }

  getInstrumentosDisponibles(): Instrumento[] {
    if (!this.currentMusico || !this.instrumentos) {
      return this.instrumentos || [];
    }

    // Si estamos editando un instrumento existente, incluirlo en las opciones
    if (this.isEditingInstrumento && this.currentInstrumento) {
      // Filtrar instrumentos que el músico no tenga, EXCEPTO el que está editando
      return this.instrumentos.filter(instrumento => {
        const yaLoTiene = this.currentMusico!.instrumentos.some(
          inst => inst.instrumento_id === instrumento.id && inst.id !== this.currentInstrumento!.id
        );
        return !yaLoTiene;
      });
    } else {
      // Para nuevos instrumentos, filtrar todos los que ya tiene el músico
      return this.instrumentos.filter(instrumento => {
        const yaLoTiene = this.currentMusico!.instrumentos.some(
          inst => inst.instrumento_id === instrumento.id
        );
        return !yaLoTiene;
      });
    }
  }



  // Getters para validaciones
  get nombre() { return this.musicoForm.get('nombre'); }
  get email() { return this.musicoForm.get('email'); }
  get telefono() { return this.musicoForm.get('telefono'); }
  get estadoCodigo() { return this.musicoForm.get('estado_codigo'); }
}
