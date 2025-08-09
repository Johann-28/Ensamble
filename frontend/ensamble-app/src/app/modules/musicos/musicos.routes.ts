// src/app/modules/musicos/musicos.routes.ts

import { Routes } from '@angular/router';

export const musicosRoutes: Routes = [
  {
    path: '',
    redirectTo: 'lista',
    pathMatch: 'full'
  },
  {
    path: 'lista',
    loadComponent: () => import('./components/musicos-list/musicos-list.component')
      .then(c => c.MusicosListComponent)
  },
  {
    path: 'nuevo',
    loadComponent: () => import('./components/musico-form/musico-form.component')
      .then(c => c.MusicoFormComponent)
  },
  {
    path: 'editar/:id',
    loadComponent: () => import('./components/musico-form/musico-form.component')
      .then(c => c.MusicoFormComponent)
  },
  {
    path: 'detalle/:id',
    loadComponent: () => import('./components/musico-detail/musico-detail.component')
      .then(c => c.MusicoDetailComponent)
  }
];
