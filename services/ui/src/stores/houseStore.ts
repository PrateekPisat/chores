import { useAuth0, Auth0VueClient } from '@auth0/auth0-vue';
import { join } from 'lodash';
import { defineStore } from 'pinia';
import { api } from 'src/boot/axios';
import { handleError } from 'src/utils';

export interface House {
  id: string;
  name: string;
}

export const userHouseStore = defineStore('house', {
  state: () => {
    return {
      errors: null as Map<string, string[]> | null,
      loading: false,
      createHouseForm: {
        name: null as string | null,
      },
      houses: [] as House[],
      auth0: useAuth0() as Auth0VueClient,
    }
  },
  getters: {
    config: () => {
      return {
        headers: {
          Authorization: `Bearer ${useAuth0().getAccessTokenSilently()}`,
        },
      }
    }
  },
  actions: {
    reset() {
      this.errors = null
      this.createHouseForm.name = null
    },
    listUserHouses(userId: string) {
      this.loading = true;
      api.get(`/user/${userId}/houses`, this.config)
        .then((response) => { this.houses = response.data; })
        .catch((error) => {
          console.error('Failed to fetch tasks:', error);
          this.errors = new Map([['fetchTasks', ['Failed to fetch tasks']]]);
        })
        .finally(() => { this.loading = false });
    },
    checkCreate() {
      this.loading = true;
      api.post('/houseValidate', this.createHouseForm, this.config).then(() => { this.errors = null })
        .catch((err) => { this.errors = handleError(err) })
        .finally(() => { this.loading = false })
    },
    async createHouse() {
      try {
        this.loading = true;
        await api.post('/house', this.createHouseForm, this.config);
      } catch (error) {
        console.error('Failed to create house:', error);
        this.errors = new Map([['createHouse', ['Failed to create house']]]);
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
    }
  },
})
