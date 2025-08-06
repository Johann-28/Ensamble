// src/app/components/dashboard/dashboard.component.ts
import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { ChartModule } from 'primeng/chart';
import { TagModule } from 'primeng/tag';
import { SkeletonModule } from 'primeng/skeleton';
import { RippleModule } from 'primeng/ripple';
import { BadgeModule } from 'primeng/badge';
import { EventosService } from '../../modules/eventos/services/eventos.service';
import { Evento } from '../../shared/interfaces/eventos.interface';
import { ServiceStatus, MenuItem } from '../../shared/interfaces/common.interface';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    CardModule,
    ButtonModule,
    ChartModule,
    TagModule,
    SkeletonModule,
    RippleModule,
    BadgeModule
  ],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})
export class DashboardComponent implements OnInit {
  private eventosService = inject(EventosService);

  // Estado de carga
  loading = true;

  // Estadísticas
  totalEventos = 0;
  eventosEnEnsayo = 0;
  eventosCompletados = 0;
  proximosEventos = 0;

  // Lista de próximos eventos
  proximosEventosList: Evento[] = [];

  // Datos del gráfico
  chartData: any;
  chartOptions: any;

  // Módulos del sistema
  modules = [
    {
      name: 'Eventos',
      description: 'Gestión de conciertos y ensayos',
      icon: 'pi pi-calendar',
      color: '#3B82F6',
      status: 'active' as const,
      route: '/eventos'
    },
    {
      name: 'Canciones',
      description: 'Catálogo y repertorio musical',
      icon: 'pi pi-music',
      color: '#10B981',
      status: 'inactive' as const,
      route: null
    },
    {
      name: 'Votaciones',
      description: 'Selección democrática de canciones',
      icon: 'pi pi-chart-bar',
      color: '#F59E0B',
      status: 'inactive' as const,
      route: null
    },
    {
      name: 'Músicos',
      description: 'Perfiles e instrumentos',
      icon: 'pi pi-users',
      color: '#8B5CF6',
      status: 'inactive' as const,
      route: null
    },
    {
      name: 'Disponibilidad',
      description: 'Horarios y confirmaciones',
      icon: 'pi pi-clock',
      color: '#EF4444',
      status: 'inactive' as const,
      route: null
    },
    {
      name: 'Ensayos',
      description: 'Coordinación y asistencia',
      icon: 'pi pi-microphone',
      color: '#06B6D4',
      status: 'inactive' as const,
      route: null
    }
  ];

  ngOnInit(): void {
    this.loadDashboardData();
    this.initChart();
  }

  loadDashboardData(): void {
    this.eventosService.getEventos(0, 50).subscribe({
      next: (response) => {
        this.calculateStats(response.eventos);
        this.proximosEventosList = this.getProximosEventos(response.eventos);
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading dashboard data:', error);
        this.loading = false;
      }
    });
  }

  calculateStats(eventos: Evento[]): void {
    const now = new Date();
    const thirtyDaysFromNow = new Date(now.getTime() + (30 * 24 * 60 * 60 * 1000));

    this.totalEventos = eventos.filter(e => e.estado.codigo !== 'cancelado').length;
    this.eventosEnEnsayo = eventos.filter(e => e.estado.codigo === 'ensayando').length;
    this.eventosCompletados = eventos.filter(e => e.estado.codigo === 'completado').length;
    
    this.proximosEventos = eventos.filter(e => {
      const fechaEvento = new Date(e.fecha_presentacion);
      return fechaEvento >= now && fechaEvento <= thirtyDaysFromNow && e.estado.codigo !== 'cancelado';
    }).length;
  }

  getProximosEventos(eventos: Evento[]): Evento[] {
    const now = new Date();
    
    return eventos
      .filter(e => {
        const fechaEvento = new Date(e.fecha_presentacion);
        return fechaEvento >= now && e.estado.codigo !== 'cancelado';
      })
      .sort((a, b) => new Date(a.fecha_presentacion).getTime() - new Date(b.fecha_presentacion).getTime())
      .slice(0, 5);
  }

  initChart(): void {
    // Datos de ejemplo para el gráfico con mejor diseño
    this.chartData = {
      labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio'],
      datasets: [
        {
          label: 'Eventos Creados',
          data: [3, 5, 2, 8, 4, 6],
          borderColor: '#3B82F6',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          tension: 0.4,
          fill: true,
          pointBackgroundColor: '#3B82F6',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 6,
          pointHoverRadius: 8
        },
        {
          label: 'Eventos Completados',
          data: [2, 4, 1, 6, 3, 5],
          borderColor: '#10B981',
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          tension: 0.4,
          fill: true,
          pointBackgroundColor: '#10B981',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 6,
          pointHoverRadius: 8
        }
      ]
    };

    this.chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: false,
        mode: 'index'
      },
      plugins: {
        legend: {
          position: 'top',
          labels: {
            usePointStyle: true,
            padding: 20,
            font: {
              size: 12,
              family: 'Inter'
            }
          }
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: 'white',
          bodyColor: 'white',
          borderColor: 'rgba(255, 255, 255, 0.2)',
          borderWidth: 1,
          cornerRadius: 8,
          displayColors: false
        }
      },
      scales: {
        x: {
          grid: {
            display: false
          },
          ticks: {
            font: {
              family: 'Inter'
            }
          }
        },
        y: {
          beginAtZero: true,
          grid: {
            color: 'rgba(0, 0, 0, 0.1)',
            drawBorder: false
          },
          ticks: {
            stepSize: 1,
            font: {
              family: 'Inter'
            }
          }
        }
      }
    };
  }

  handleModuleClick(module: any): void {
    if (module.status === 'active' && module.route) {
      // Navegar al módulo
      window.location.href = module.route;
    } else {
      // Mostrar mensaje de "próximamente"
      alert(`El módulo de ${module.name} estará disponible próximamente. 🎵`);
    }
  }

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

  getStatusLabel(status: string): string {
    const labels: { [key: string]: string } = {
      'active': 'Activo',
      'inactive': 'Próximamente',
      'maintenance': 'Mantenimiento'
    };
    return labels[status] || status;
  }

  getStatusSeverity(status: string): 'success' | 'info' | 'warn' | 'danger' | 'secondary' | 'contrast' {
    const severities: { [key: string]: any } = {
      'active': 'success',
      'inactive': 'secondary',
      'maintenance': 'warn'
    };
    return severities[status] || 'secondary';
  }
}