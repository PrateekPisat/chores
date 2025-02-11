
import { defineStore } from 'pinia'
import { join } from 'lodash';
import { Auth0VueClient, useAuth0, User } from '@auth0/auth0-vue';
import { api } from 'src/boot/axios';
import { handleError } from 'src/utils';

export interface AppUser {
  user_id: string;
  email: string;
  first_name: string;
  last_name: string;
  sub: string;
  picture: string | null;
  nickname: string | null;
}

export const userUserStore = defineStore('user', {
  state: () => {
    return {
      errors: null as Map<string, string[]> | null,
      loading: false,
      auth0: useAuth0() as Auth0VueClient,
      appUser: {} as AppUser,
    }
  },
  getters: {
    isAuthenticated(): boolean {
      return this.auth0.isAuthenticated
    },
    auth0User(): User | undefined {
      return this.auth0.user
    },
    user(): AppUser {
      return this.appUser
    },
    isVerified(): boolean {
      return this.auth0User?.email_verified || false
    }
  },
  actions: {
    reset() {
      this.errors = null
    },
    syncUser() {
      this.loading = true
      api.post('/user/sync', {
        email: this.auth0User?.email,
        firstName: this.auth0User?.given_name || this.auth0User?.nickname,
        lastName: this.auth0User?.family_name || this.auth0User?.nickname,
        picture: this.auth0User?.picture,
        nickname: this.auth0User?.nickname,
        sub: this.auth0User?.sub,
      }).then((response) => { this.appUser = response.data })
        .catch((err) => { this.errors = handleError(err) })
        .finally(() => { this.loading = false })
    },
    getUser(userId: string) {
      this.loading = true
      api.get('/user/' + userId).then((response) => { this.appUser = response.data })
        .catch((err) => { this.errors = handleError(err) })
        .finally(() => { this.loading = false })
    },
    updateUser() {
      this.loading = true
      api.put('/user/' + this.appUser.user_id, this.appUser).then((response) => { this.appUser = response.data })
        .catch((err) => { this.errors = handleError(err) })
        .finally(() => { this.loading = false })
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
