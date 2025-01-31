
import { join } from 'lodash';
import { defineStore } from 'pinia'
import { api } from 'src/boot/axios';
import { handleError } from 'src/utils';
import { inject } from 'vue';
import { VueCookies } from 'vue-cookies';
import { z } from 'zod';

export const RegisterPayload = z.object({
  firstName: z.string().nullable(),
  lastName: z.string().nullable(),
  email: z.string().nullable(),
  password: z.string().nullable(),
  confirmPassword: z.string().nullable(),
});

export const RegisterResponse = z.object({
  token: z.string(),
  user_id: z.string(),
});

export const userRegisterStore = defineStore('register', {
  state: () => {
    return {
      registerPayload: {
        firstName: null,
        lastName: null,
        email: null,
        password: null,
        confirmPassword: null,
      } as z.infer<typeof RegisterPayload>,
      errors: null as Map<string, string[]> | null,
      loading: false,
    }
  },
  getters: {
    cookies(): VueCookies | undefined {
      return inject<VueCookies>('$cookies');
    }
  },
  actions: {
    reset() {
      this.registerPayload = {
        firstName: null,
        lastName: null,
        email: null,
        password: null,
        confirmPassword: null,
      }
    },
    validateRegisterPayload() {
      this.loading = true
      api.post('/userValidate', this.registerPayload)
        .then(() => { this.errors = null })
        .catch((err) => { this.errors = handleError(err) })
        .finally(() => { this.loading = false })
    },
    register(): Promise<z.infer<typeof RegisterResponse> | undefined> {
      this.loading = true
      return api.post('/user', this.registerPayload)
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
