export interface Task {
  id: number;
  title: string;
  description: string | null;
  status: 'incomplete' | 'complete';
  user_id: string;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}

export interface TaskCreate {
  title: string;
  description?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
}