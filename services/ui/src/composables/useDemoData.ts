import { ref } from 'vue';
import type { Task, Chore } from 'src/stores/taskStore';
import type { AppUser } from 'src/stores/userStore';

export interface House {
  houseId: string;
  houseName: string;
  description: string;
  ownerId: string;
}

export function useDemoData() {
  // Demo user data
  const demoUser = ref<AppUser>({
    userId: 'usr_7k9m2n4p6q8r',
    email: 'sarah.johnson@email.com',
    firstName: 'Sarah',
    lastName: 'Johnson',
    sub: 'auth0|65f8a3b9c4e2d1a0f7e9b6c3',
    picture: 'https://ui-avatars.com/api/?name=Sarah+Johnson&background=6366f1&color=fff&bold=true',
    nickname: '',
  });

  // Demo chores
  const demoChores: Chore[] = [
    {
      id: 'chore-1',
      name: 'Vacuum Living Room',
      description: 'Vacuum the entire living room including under furniture',
      cadence: 'WEEKLY',
      startDate: '2026-01-01',
      endDate: '2026-12-31',
    },
    {
      id: 'chore-2',
      name: 'Clean Kitchen',
      description: 'Deep clean kitchen counters, sink, and appliances',
      cadence: 'WEEKLY',
      startDate: '2026-01-01',
      endDate: '2026-12-31',
    },
    {
      id: 'chore-3',
      name: 'Take Out Trash',
      description: 'Take out all trash and recycling bins',
      cadence: 'WEEKLY',
      startDate: '2026-01-01',
      endDate: '2026-12-31',
    },
    {
      id: 'chore-4',
      name: 'Mow Lawn',
      description: 'Mow the front and back lawn',
      cadence: 'BIWEEKLY',
      startDate: '2026-01-01',
      endDate: '2026-12-31',
    },
    {
      id: 'chore-5',
      name: 'Clean Bathrooms',
      description: 'Clean all bathrooms including toilet, shower, and sink',
      cadence: 'WEEKLY',
      startDate: '2026-01-01',
      endDate: '2026-12-31',
    },
    {
      id: 'chore-6',
      name: 'Water Plants',
      description: 'Water all indoor and outdoor plants',
      cadence: 'BIWEEKLY',
      startDate: '2026-01-01',
      endDate: '2026-12-31',
    },
    {
      id: 'chore-7',
      name: 'Change Air Filters',
      description: 'Replace HVAC air filters throughout the house',
      cadence: 'MONTHLY',
      startDate: '2026-01-01',
      endDate: '2026-12-31',
    },
    {
      id: 'chore-8',
      name: 'Clean Windows',
      description: 'Clean all windows inside and outside',
      cadence: 'MONTHLY',
      startDate: '2026-01-01',
      endDate: '2026-12-31',
    },
  ];

  // Demo tasks with various states (past due, this week, this month, completed)
  const demoTasks = ref<Task[]>([
    {
      id: 'task-1',
      chore: demoChores[0],
      user: demoUser.value,
      dueDate: '2026-01-17', // Past due (2 days ago)
      completedAt: null,
    },
    {
      id: 'task-2',
      chore: demoChores[1],
      user: demoUser.value,
      dueDate: '2026-01-16', // Past due (3 days ago)
      completedAt: null,
    },
    {
      id: 'task-3',
      chore: demoChores[2],
      user: demoUser.value,
      dueDate: '2026-01-19', // Today (current week)
      completedAt: null,
    },
    {
      id: 'task-4',
      chore: demoChores[3],
      user: demoUser.value,
      dueDate: '2026-01-22', // This week
      completedAt: null,
    },
    {
      id: 'task-5',
      chore: demoChores[4],
      user: demoUser.value,
      dueDate: '2026-01-24', // This week
      completedAt: null,
    },
    {
      id: 'task-6',
      chore: demoChores[5],
      user: demoUser.value,
      dueDate: '2026-01-28', // This month
      completedAt: null,
    },
    {
      id: 'task-7',
      chore: demoChores[6],
      user: demoUser.value,
      dueDate: '2026-02-01', // Next month
      completedAt: null,
    },
    {
      id: 'task-8',
      chore: demoChores[7],
      user: demoUser.value,
      dueDate: '2026-01-15', // Completed task
      completedAt: '2026-01-15T10:30:00Z',
    },
  ]);

  // Demo houses
  const demoHouses = ref<House[]>([
    {
      houseId: 'house-1',
      houseName: 'Main House',
      description: 'Primary family residence',
      ownerId: demoUser.value.userId,
    },
    {
      houseId: 'house-2',
      houseName: 'Vacation Home',
      description: 'Beach house for summer vacations',
      ownerId: demoUser.value.userId,
    },
  ]);

  // Mock API functions for demo mode
  const updateDemoTask = (taskId: string, completed: boolean, dueDate: string) => {
    const task = demoTasks.value.find((t) => t.id === taskId);
    if (task) {
      task.completedAt = completed ? new Date().toISOString() : null;
      task.dueDate = dueDate;
    }
  };

  const deleteDemoTask = (taskId: string) => {
    const index = demoTasks.value.findIndex((t) => t.id === taskId);
    if (index > -1) {
      demoTasks.value.splice(index, 1);
    }
  };

  const addDemoChore = (chore: Partial<Chore>) => {
    const newChore: Chore = {
      id: `chore-${Date.now()}`,
      name: chore.name || '',
      description: chore.description || '',
      cadence: chore.cadence || 'WEEKLY',
      startDate: chore.startDate || new Date().toISOString(),
      endDate: chore.endDate || new Date().toISOString(),
    };
    demoChores.push(newChore);
    return newChore;
  };

  const addDemoTask = (choreId: string, dueDate: string) => {
    const chore = demoChores.find((c) => c.id === choreId);
    if (chore) {
      const newTask: Task = {
        id: `task-${Date.now()}`,
        chore,
        user: demoUser.value,
        dueDate,
        completedAt: null,
      };
      demoTasks.value.push(newTask);
      return newTask;
    }
  };

  return {
    demoUser,
    demoTasks,
    demoHouses,
    demoChores,
    updateDemoTask,
    deleteDemoTask,
    addDemoChore,
    addDemoTask,
  };
}
