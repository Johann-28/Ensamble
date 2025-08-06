// src/app/modules/eventos/eventos.routes.ts
import { Routes } from '@angular/router';
import { EventoFormComponent } from './components/evento-form/evento-form.component';

export const eventosRoutes: Routes = [
  {
    path: '',
    loadComponent: () => import('./components/eventos-list/eventos-list.component').then(m => m.EventosListComponent)
  },
  {
    path: 'nuevo',
    loadComponent: () => import('./components/evento-form/evento-form.component').then(m => m.EventoFormComponent)
  },
  {
    path: ':id',
    loadComponent: () => import('./components/evento-detail/evento-detail.component').then(m => m.EventoDetailComponent)
  },
  {
    path: ':id/editar',
    loadComponent: () => import('./components/evento-form/evento-form.component').then(m => m.EventoFormComponent)
  }
];