import { defineStore } from 'pinia'
import { join } from 'lodash';
import { Auth0VueClient, User } from '@auth0/auth0-vue';
import { api, ValidationError } from 'src/boot/axios';
import { handleError } from 'src/utils';
import { AxiosError } from 'axios';

export interface AppUser {
  userId: string;
  email: string;
  firstName: string;
  lastName: string;
  sub: string;
  picture: string | null;
  nickname: string | null;
}

export const userUserStore = defineStore('user', {
  state: () => {
    return {
      errors: null as Map<string, string[]> | null,
      loading: false,
      appUser: {} as AppUser,
    }
  },
  getters: {
    user(): AppUser {
      return this.appUser
    },
    userName(): string {
      if (this.appUser.firstName && this.appUser.lastName) {
        return this.appUser.firstName + ' ' + this.appUser.lastName
      }
      if (this.appUser.nickname) {
        return this.appUser.nickname
      }
      if (this.appUser.email) {
        return this.appUser.email
      }
      return ''
    },
  },
  actions: {
    reset() {
      this.errors = null
    },
    defaultUserArgs() {
      return {
        email: this.appUser.email,
        picture: this.appUser.picture,
        nickname: this.appUser.nickname,
        sub: this.appUser.sub,
      }
    },
    async syncUser(auth0User: User | undefined) {
      this.loading = true;
      try {
        const response = await api.post('/user/sync', {
          email: auth0User?.email,
          firstName: auth0User?.given_name || auth0User?.nickname,
          lastName: auth0User?.family_name || auth0User?.nickname,
          picture: auth0User?.picture,
          nickname: auth0User?.nickname,
          sub: auth0User?.sub,
        });
        this.appUser = response.data;
      } catch (err) {
        this.errors = handleError(err as AxiosError | ValidationError);
      } finally {
        this.loading = false;
      }
    },
    async getUser(userId: string) {
      this.loading = true;
      try {
        const response = await api.get('/user/' + userId);
        this.appUser = response.data;
      } catch (err) {
        this.errors = handleError(err as AxiosError | ValidationError);
      } finally {
        this.loading = false;
      }
    },
    async checkUpdate(firstName: string | number | null, lastName: string | number | null) {
      this.loading = true;
      try {
        await api.post('/user/updateValidate', {
          firstName: firstName,
          lastName: lastName,
          ...this.defaultUserArgs()
        });
        this.errors = null;
      } catch (err) {
        this.errors = handleError(err as AxiosError | ValidationError);
      } finally {
        this.loading = false;
      }
    },
    async updateUser(firstName: string | number | null, lastName: string | number | null) {
      this.loading = true;
      try {
        const response = await api.put('/user/' + this.appUser.userId, {
          first_name: firstName,
          last_name: lastName,
          ...this.defaultUserArgs()
        });
        await this.getUser(response.data.userId);
      } catch (err) {
        this.errors = handleError(err as AxiosError | ValidationError);
      } finally {
        this.loading = false;
      }
    },
    async deleteUser(auth0Client: Auth0VueClient) {
      if (!this.appUser.userId) {
        console.error('No userId found in appUser')
      }

      this.loading = true;
      try {
        await api.delete('/user/' + this.appUser.userId);
        auth0Client.logout();
      } catch (err) {
        this.errors = handleError(err as AxiosError | ValidationError);
      } finally {
        this.loading = false;
      }
    },
    async searchUser(email: string | null, choreId: string | null = null): Promise<AppUser[]> {
      this.loading = true;
      try {
        const response = await api.post('/user/search', { email, choreId });
        this.reset();
        return response.data as AppUser[];
      } catch (error) {
        console.error('Failed to search user:', error);
        this.errors = handleError(error as AxiosError | ValidationError);
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
