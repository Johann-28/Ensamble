export interface MenuItem {
  label: string;
  icon: string;
  routerLink?: string;
  command?: () => void;
  disabled?: boolean;
}

export interface ServiceStatus {
  name: string;
  status: 'active' | 'inactive' | 'maintenance';
  description: string;
}