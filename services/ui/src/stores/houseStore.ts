import { join } from 'lodash';
import { defineStore } from 'pinia';
import { api } from 'src/boot/axios';
import { handleError } from 'src/utils';
import { AppUser } from './userStore';

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
    }
  },
  actions: {
    reset() {
      this.errors = null
      this.createHouseForm.name = null
    },
    async listUserHouses(userId: string) {
      this.loading = true;
      return api.get(`/user/${userId}/houses`)
        .then((response) => { this.houses = response.data; })
        .catch((error) => {
          console.error('Failed to fetch tasks:', error);
          this.errors = new Map([['fetchTasks', ['Failed to fetch tasks']]]);
        })
        .finally(() => { this.loading = false });
    },
    async checkCreate() {
      this.loading = true;
      return api.post('/house/houseValidate', this.createHouseForm).then(() => { this.errors = null })
        .catch((err) => { this.errors = handleError(err) })
        .finally(() => { this.loading = false })
    },
    async checkValidate(name: string) {
      this.loading = true;
      return api.post('/house/houseValidate', { name }).then(() => { this.errors = null })
        .catch((err) => { this.errors = handleError(err) })
        .finally(() => { this.loading = false })
    },
    async createHouse(): Promise<string> {
      this.loading = true;
      return api.post('/house', this.createHouseForm)
        .then(async (response) => {
          return response.data.id;
        })
        .catch((error) => {
          console.error('Failed to create house:', error);
          this.errors = new Map([['createHouse', ['Failed to create house']]]);
        }).
        finally(() => { this.loading = false });
    },
    async getHouse(houseId: string): Promise<House> {
      this.loading = true;
      return api.get(`/house/${houseId}`)
        .then((response) => {
          return response.data;
        })
        .catch((error) => {
          console.error('Failed to fetch house:', error);
          this.errors = new Map([['fetchHouse', ['Failed to fetch house']]]);
        })
        .finally(() => { this.loading = false });
    },
    async editHouse(houseId: string, name: string | null) {
      this.loading = true;
      return api.put(`/house/${houseId}`, { name })
        .then(() => { this.errors = null })
        .catch((error) => {
          console.error('Failed to edit house:', error);
          this.errors = new Map([['editHouse', ['Failed to edit house']]]);
        })
        .finally(() => { this.loading = false });
    },
    async deleteHouse(houseId: string) {
      this.loading = true;
      return api.delete(`/house/${houseId}`)
        .then(() => { this.errors = null })
        .catch((error) => {
          console.error('Failed to delete house:', error);
          this.errors = new Map([['deleteHouse', ['Failed to delete house']]]);
        })
        .finally(() => { this.loading = false });
    },
    async addMembers(houseId: string, members: string[]) {
      this.loading = true;
      return api.post('/house/member', { houseId, userIds: members })
        .then()
        .catch((error) => {
          console.error('Failed to add members:', error);
          this.errors = new Map([['addMembers', ['Failed to add members']]]);
        })
        .finally(() => { this.loading = false });
    },
    async deleteMember(houseId: string, userId: string) {
      this.loading = true;
      try {
        await api.delete(`/house/${houseId}/member/${userId}`);
        this.errors = null;
      }
      catch (error) {
        console.error('Failed to delete member:', error);
        this.errors = new Map([['deleteMember', ['Failed to delete member']]]);
      } finally {
        this.loading = false;
      }
    },
    async getMembers(houseId: string): Promise<AppUser[]> {
      this.loading = true;
      try {
        const response = await api.get(`/house/${houseId}/member`);
        return response.data?.users as AppUser[];
      } catch (error) {
        console.error('Failed to fetch members:', error);
        this.errors = new Map([['fetchMembers', ['Failed to fetch members']]]);
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
    }
  },
})
