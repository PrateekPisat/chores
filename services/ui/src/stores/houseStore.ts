import { defineStore } from 'pinia';
import { api } from 'src/boot/axios';

export const houseStore = defineStore('house', {
  state: () => {
    return {
      errors: null as Map<string, string[]> | null,
      loading: false,
      tasks: [],
    }
  },
  getters: {
  },
  actions: {
    reset() {
      this.errors = null
    },
    async fetchTasks() {
      try {
        this.loading = true;
        const response = await api.get('/tasks');
        this.tasks = response.data;
      } catch (error) {
        console.error('Failed to fetch tasks:', error);
        this.errors = new Map([['fetchTasks', ['Failed to fetch tasks']]]);
      } finally {
        this.loading = false;
      }
    },
  },
})
