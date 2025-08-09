// src/app/app.component.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterModule } from '@angular/router';
import { MenubarModule } from 'primeng/menubar';
import { ButtonModule } from 'primeng/button';
import { MenuItem } from 'primeng/api';
import { PrimeNG } from 'primeng/config';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MenubarModule,
    ButtonModule
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {

 
  constructor(private primeng : PrimeNG) {}

  ngOnInit(): void {
    this.primeng.ripple.set(true);
  }
  menuItems: MenuItem[] = [
    {
      label: 'Dashboard',
      icon: 'pi pi-home',
      routerLink: '/dashboard'
    },
    {
      label: 'Eventos',
      icon: 'pi pi-calendar',
      routerLink: '/eventos'
    },
    {
      label: 'Canciones',
      icon: 'pi pi-music',
      command: () => this.showComingSoon('Canciones')
    },
    {
      label: 'Votaciones',
      icon: 'pi pi-chart-bar',
      command: () => this.showComingSoon('Votaciones')
    },
    {
      label: 'Músicos',
      icon: 'pi pi-users',
      routerLink: '/musicos'
    },
    {
      label: 'Disponibilidad',
      icon: 'pi pi-clock',
      command: () => this.showComingSoon('Disponibilidad')
    },
    {
      label: 'Ensayos',
      icon: 'pi pi-microphone',
      command: () => this.showComingSoon('Ensayos')
    }
  ];

  showComingSoon(module: string): void {
    // Por ahora solo un alert, más adelante se puede implementar un modal
    alert(`El módulo de ${module} estará disponible próximamente. 🎵`);
  }
}