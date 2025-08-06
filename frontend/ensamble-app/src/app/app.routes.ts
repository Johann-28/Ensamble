import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: '/dashboard',
    pathMatch: 'full'
  },
  {
    path: 'dashboard',
    loadComponent: () => import('./components/dashboard/dashboard.component').then(m => m.DashboardComponent)
  },
  {
    path: 'eventos',
    loadChildren: () => import('./modules/eventos/eventos.routes').then(m => m.eventosRoutes)
  },
  {
    path: '**',
    redirectTo: '/dashboard'
  }
];