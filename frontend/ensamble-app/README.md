# Band Management System - Frontend

## 🎵 Descripción

Frontend desarrollado en Angular 17 con standalone components para el Sistema de Gestión de Banda Musical. Utiliza PrimeNG como librería de componentes UI y está diseñado con una arquitectura moderna y escalable.

## 🚀 Características

### ✨ Tecnologías Principales
- **Angular 17** - Framework principal con standalone components
- **PrimeNG 17** - Librería de componentes UI moderna
- **TypeScript** - Tipado estático para mayor robustez
- **SCSS** - Estilos avanzados y variables CSS personalizadas
- **RxJS** - Management de estado reactivo

### 🎯 Funcionalidades Implementadas

#### 📊 Dashboard
- Vista general del sistema con métricas en tiempo real
- Estadísticas de eventos (total, en ensayo, completados, próximos)
- Lista de próximos eventos con navegación rápida
- Módulos del sistema con estados (activo/próximamente)
- Gráfico de actividad de eventos (últimos 6 meses)
- Diseño responsivo y accesible

#### 🎪 Gestión de Eventos
- **Lista de Eventos**: Tabla con paginación, filtros y búsqueda
- **Crear/Editar Eventos**: Formulario completo con validaciones
- **Detalle de Evento**: Vista completa con tabs organizados
- **Gestión de Participantes**: Invitar músicos y controlar estados
- **Catálogos**: Tipos y estados de eventos dinámicos

### 🏗️ Arquitectura

#### Estructura de Carpetas
```
src/
├── app/
│   ├── components/           # Componentes globales
│   │   └── dashboard/       # Dashboard principal
│   ├── modules/             # Módulos por dominio
│   │   └── eventos/         # Módulo de eventos
│   │       ├── components/  # Componentes específicos
│   │       ├── services/    # Servicios del dominio
│   │       └── eventos.routes.ts
│   ├── shared/              # Código compartido
│   │   └── interfaces/      # Interfaces TypeScript
│   ├── environments/        # Configuración de entornos
│   ├── app.component.ts     # Componente raíz
│   ├── app.config.ts        # Configuración de la app
│   └── app.routes.ts        # Rutas principales
├── assets/                  # Recursos estáticos
└── styles.scss             # Estilos globales
```

#### Patrones Implementados
- **Standalone Components**: Sin módulos NgModule tradicionales
- **Lazy Loading**: Carga diferida de módulos por rutas
- **Service Layer**: Separación clara de lógica de negocio
- **Reactive Forms**: Formularios tipados y validados
- **Dependency Injection**: Inyección de dependencias moderna

## 🛠️ Instalación y Configuración

### Prerrequisitos
- Node.js 18+
- npm 9+ o yarn
- Angular CLI 17+

### Instalación
```bash
# Clonar el repositorio
git clone <repository-url>
cd band-management-frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
cp src/environments/environment.ts src/environments/environment.local.ts
# Editar environment.local.ts con la URL de tu API

# Iniciar servidor de desarrollo
npm start
```

### Scripts Disponibles
```bash
npm start          # Servidor de desarrollo (http://localhost:4200)
npm run build      # Build para producción
npm run watch      # Build en modo watch
npm test           # Ejecutar tests unitarios
npm run lint       # Linter de código
```

## 🎨 Sistema de Design

### PrimeNG Theme
- **Tema Base**: Lara Light Blue
- **Personalización**: Variables CSS custom para consistencia
- **Componentes**: Más de 80 componentes UI listos para usar

### Colores y Estilos
```scss
:root {
  --primary-color: #3B82F6;      // Azul principal
  --success-color: #10B981;      // Verde para éxito
  --warning-color: #F59E0B;      // Amarillo para advertencias
  --danger-color: #EF4444;       // Rojo para errores
  --info-color: #06B6D4;         // Cyan para información
}
```

### Sistema de Espaciado
- **Padding/Margin**: Sistema basado en 0.25rem (4px)
- **Border Radius**: 8px para elementos normales, 12px para cards
- **Shadows**: Tres niveles (light, medium, large)
- **Transiciones**: 0.2s ease-in-out consistente

## 🔧 API Integration

### Configuración de Servicios
```typescript
// environment.ts
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8001'  // URL del backend
};
```

### EventosService
Servicio principal que consume la API REST del backend:

```typescript
// Métodos principales
- createEvento(evento: EventoCreate): Observable<Evento>
- getEventos(skip?: number, limit?: number): Observable<EventosListResponse>
- getEvento(eventoId: string): Observable<Evento>
- updateEvento(eventoId: string, evento: EventoUpdate): Observable<Evento>
- deleteEvento(eventoId: string): Observable<{message: string}>

// Gestión de participantes
- addParticipante(eventoId: string, participante: ParticipanteEventoCreate)
- getParticipantes(eventoId: string): Observable<ParticipanteEvento[]>
- updateParticipante(eventoId: string, musicoId: string, update: ParticipanteEventoUpdate)

// Catálogos
- getTiposEvento(): Observable<TipoEvento[]>
- getEstadosEvento(): Observable<EstadoEvento[]>
```

## 📱 Características UX/UI

### Responsive Design
- **Mobile First**: Diseño optimizado para móviles
- **Breakpoints**: sm (768px), md (992px), lg (1200px)
- **Navegación**: Menú adaptativo según dispositivo
- **Tablas**: Scroll horizontal en pantallas pequeñas

### Accesibilidad
- **WCAG 2.1**: Cumplimiento de estándares AA
- **Keyboard Navigation**: Navegación completa por teclado
- **Screen Readers**: Etiquetas ARIA y texto alternativo
- **Focus Management**: Estados de foco visibles y lógicos

### Estados de Carga
- **Skeletons**: Placeholders durante carga de datos
- **Spinners**: Indicadores para acciones async
- **Toasts**: Notificaciones de éxito/error
- **Confirmaciones**: Diálogos para acciones destructivas

## 🧪 Testing (Preparado para implementar)

### Estructura de Tests
```bash
src/
├── app/
│   ├── components/
│   │   └── dashboard/
│   │       ├── dashboard.component.spec.ts
│   │       └── dashboard.component.ts
│   └── modules/
│       └── eventos/
│           ├── services/
│           │   └── eventos.service.spec.ts
│           └── components/
│               ├── eventos-list/
│               │   └── eventos-list.component.spec.ts
│               ├── evento-form/
│               │   └── evento-form.component.spec.ts
│               └── evento-detail/
│                   └── evento-detail.component.spec.ts
```

### Tipos de Tests
- **Unit Tests**: Componentes y servicios
- **Integration Tests**: Interacciones entre componentes
- **E2E Tests**: Flujos completos de usuario

## 🚀 Deployment

### Build para Producción
```bash
# Build optimizado
npm run build

# Los archivos se generan en dist/
# Servir con cualquier servidor web estático
```

### Configuración de Entornos
```typescript
// environment.prod.ts
export const environment = {
  production: true,
  apiUrl: 'https://api.band-management.com'
};
```

## 🔮 Próximas Funcionalidades

### Módulos Preparados
Los siguientes módulos están preparados en la navegación y serán implementados en futuras iteraciones:

1. **🎵 Canciones**
   - Catálogo de canciones con metadatos
   - Requisitos instrumentales por canción
   - Gestión de dificultad y niveles

2. **🗳️ Votaciones**
   - Sistema de votación democrática
   - Recomendaciones de canciones
   - Resultados en tiempo real

3. **👥 Músicos**
   - Perfiles de músicos
   - Instrumentos y habilidades
   - Historial de participación

4. **📅 Disponibilidad**
   - Calendario de disponibilidad
   - Confirmación de asistencia
   - Horarios de práctica

5. **🎭 Ensayos**
   - Programación de ensayos
   - Registro de asistencia
   - Recomendaciones inteligentes

### Mejoras Técnicas Planeadas
- **PWA**: Aplicación web progresiva
- **Offline Mode**: Funcionalidad sin conexión
- **Push Notifications**: Notificaciones en tiempo real
- **Websockets**: Actualizaciones live
- **State Management**: NgRx para estado global
- **Internacionalización**: Soporte multi-idioma

## 🤝 Contribución

### Estándares de Código
- **ESLint**: Reglas de linting estrictas
- **Prettier**: Formateo automático de código
- **Conventional Commits**: Mensajes de commit estandarizados
- **TypeScript Strict**: Modo estricto habilitado

### Workflow de Desarrollo
1. Fork del repositorio
2. Crear branch feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commits siguiendo conventional commits
4. Tests para nueva funcionalidad
5. Pull request con descripción detallada

## 📖 Documentación Adicional

- [Guía de Componentes PrimeNG](https://primeng.org/)
- [Angular Style Guide](https://angular.io/guide/styleguide)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [SCSS Documentation](https://sass-lang.com/documentation)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 🎯 Estado Actual

### ✅ Completado
- [x] Configuración inicial del proyecto
- [x] Sistema de routing con lazy loading
- [x] Dashboard interactivo con métricas
- [x] Módulo completo de eventos (CRUD)
- [x] Integración con API backend
- [x] Sistema de estilos con PrimeNG
- [x] Componentes responsive
- [x] Manejo de errores y estados de carga

### 🔄 En Progreso
- [ ] Tests unitarios y de integración
- [ ] Documentación de componentes
- [ ] Optimización de performance

### 📋 Pendiente
- [ ] Implementación de módulos restantes
- [ ] PWA capabilities
- [ ] Internacionalización
- [ ] Accessibility audit completo
- [ ] Performance monitoring

---

**Desarrollado con ❤️ para la comunidad musical**