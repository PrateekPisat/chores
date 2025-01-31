
import { defineStore } from 'pinia'
import { api } from 'src/boot/axios';
import { z } from 'zod';
import { handleError } from 'src/utils';
import { join } from 'lodash';

export const LoginPayload = z.object({
  email: z.string().nullable(),
  password: z.string().nullable(),
});

export const LoginResponse = z.object({
  token: z.string(),
  user_id: z.string(),
});

export const userLoginStore = defineStore('login', {
  state: () => {
    return {
      loginPayload: {
        email: null,
        password: null,
      } as z.infer<typeof LoginPayload>,
      errors: null as Map<string, string[]> | null,
      loading: false,
    }
  },
  getters: {
  },
  actions: {
    reset() {
      this.loginPayload = {
        email: null,
        password: null,
      }
      this.errors = null
    },
    validateLoginPayload() {
      this.loading = true
      console.log('checking')
      api.post('/loginValidate', this.loginPayload)
        .then(() => { this.errors = null })
        .catch((err) => { this.errors = handleError(err) })
        .finally(() => { this.loading = false })
    },
    login(): Promise<z.infer<typeof LoginResponse>> {
      this.loading = true
      console.log('logging in')
      return api.post('/login', this.loginPayload)
        .then((response) => { return response.data })
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
