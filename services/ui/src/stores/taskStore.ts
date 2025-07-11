import { defineStore } from 'pinia';
import { api } from 'src/boot/axios';
import { AppUser } from './userStore'
import { join } from 'lodash';
import { handleError } from 'src/utils';


export interface Chore {
  id: string;
  name: string;
  description: string;
  cadence: string;
  startDate: string;
  endDate: string;
}
export interface Task {
  id: string
  chore: Chore;
  user: AppUser;
  dueDate: string;
  completedAt: string | null;
}

export const taskStore = defineStore('task', {
  state: () => {
    return {
      errors: null as Map<string, string[]> | null,
      loading: false,
      tasks: [] as Task[],
      chores: [] as Chore[],
      newChore: {
        name: '',
        description: '',
        cadence: '',
        startDate: '',
        endDate: '',
        houseId: ''
      }
    }
  },
  getters: {
    config: () => {
      return {
        headers: {
          Authorization: 'Bearer FakeToken',
        },
      }
    }
  },
  actions: {
    resetForm() {
      this.newChore = {
        name: '',
        description: '',
        cadence: '',
        startDate: '',
        endDate: '',
        houseId: ''
      }
    },
    reset() {
      this.resetForm();
      this.errors = null
    },
    async fetchTasks(userId: string) {
      try {
        this.loading = true;
        const response = await api.get(`/user/${userId}/tasks`, this.config);
        this.tasks = response.data;
      } catch (error) {
        console.error('Failed to fetch tasks:', error);
        this.errors = new Map([['fetchTasks', ['Failed to fetch tasks']]]);
      } finally {
        this.loading = false;
      }
    },
    async deleteTask(taskId: string) {
      this.loading = true;
      try {
        await api.delete(`/task/${taskId}`, this.config);
      } catch (error) {
        console.error('Failed to delete task:', error);
        this.errors = new Map([['deleteTask', ['Failed to delete task']]]);
      } finally {
        this.loading = false;
      }
    },
    async updateTask(taskId: string, completed: boolean, dueDate: string) {
      this.loading = true;
      try {
        await api.put(
          `/task/${taskId}`,
          { completedAt: completed ? new Date() : null, dueDate: dueDate },
          this.config
        );
      } catch (error) {
        console.error('Failed to update task:', error);
        this.errors = new Map([['updateTask', ['Failed to update task']]]);
      } finally {
        this.loading = false;
      }
    },
    async checkCreateChore() {
      this.loading = true;
      return api.post('/chore/choreValidate', this.newChore, this.config)
        .then(() => { this.errors = null })
        .catch((err) => { this.errors = handleError(err) })
        .finally(() => { this.loading = false })
    },
    async checkCreateDistribution(userIds: string[], choreId: string) {
      this.loading = true;
      return api.post('/chore/distributionValidate', { userIds, choreId }, this.config)
        .then(() => { this.errors = null })
        .catch((err) => { this.errors = handleError(err) })
        .finally(() => { this.loading = false })
    },
    async getDistribution(choreId: string) {
      this.loading = true;
      try {
        const response = await api.get(`/chore/${choreId}/distribution`, this.config);
        return response.data;
      } catch (error) {
        console.error('Failed to get distribution:', error);
        this.errors = new Map([['getDistribution', ['Failed to get distribution']]]);
        return [];
      } finally {
        this.loading = false;
      }
    },
    async createDistribution(userIds: string[], choreId: string) {
      this.loading = true;
      try {
        await api.post('/chore/distribution', { userIds, choreId }, this.config);
      } catch (error) {
        this.errors = new Map([['createDistribution', ['Failed to create distribution']]]);
      } finally {
        this.loading = false;
      }
    },
    async updateDistribution(userIds: string[], choreId: string) {
      this.loading = true;
      try {
        await api.put(`/chore/${choreId}/distribution`, { userIds, choreId }, this.config);
      } catch (error) {
        this.errors = new Map([['updateDistribution', ['Failed to update distribution']]]);
      } finally {
        this.loading = false;
      }
    },
    async createChore() {
      this.loading = true;
      try {
        await api.post('/chore', this.newChore, this.config);
        this.resetForm();
      }
      catch (error) {
        this.errors = new Map([['createChore', ['Failed to create chore']]]);
      } finally {
        this.loading = false;
      }
    },
    async listChores(userId: string) {
      this.loading = true;
      try {
        const response = await api.get(`/user/${userId}/chores`, this.config);
        this.chores = response.data;
      } catch (error) {
        this.errors = new Map([['listChores', ['Failed to list chores']]]);
        return [];
      } finally {
        this.loading = false;
      }
    },
    getErrors(key: string): string {
      if (this.errors) {
        return join(this.errors.get(key) || []);
      } else {
        return '';
      }
    },
  },
})
