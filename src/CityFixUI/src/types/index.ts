export interface User {
    id: string;
    email: string;
    role: 'citizen' | 'operator' | 'admin';
    tenant_id?: string;
    created_at: string;
  }
  
  export interface Location {
    lat: number;
    lon: number;
    address?: string;
  }
  
  export interface Ticket {
    id: string;
    title: string;
    description: string;
    location: Location;
    status: 'pending' | 'in_progress' | 'completed' | 'rejected';
    category: string;
    reported_by: string;
    assigned_to?: string;
    images: string[];
    tenant_id: string;
    comments: Comment[];
    feedback?: Feedback;
    created_at: string;
    updated_at: string;
  }
  
  export interface Comment {
    user_id: string;
    message: string;
    created_at: string;
  }
  
  export interface Feedback {
    rating: number;
    comment?: string;
    created_at: string;
  }
  
  export interface Municipality {
    id: string;
    name: string;
    location: Location;
    admin_id: string;
    created_at: string;
  }
  
  export interface Notification {
    id: string;
    user_id: string;
    message: string;
    type: 'info' | 'warning' | 'success' | 'error';
    ticket_id?: string;
    read: boolean;
    created_at: string;
  }
  
  export interface Stats {
    total_tickets: number;
    pending_tickets: number;
    in_progress_tickets: number;
    completed_tickets: number;
    total_municipalities: number;
    total_users: number;
    tickets_by_category: Record<string, number>;
    tickets_by_municipality: Record<string, number>;
  }