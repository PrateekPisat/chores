import { defineStore } from 'pinia'


export interface User {
  firstName: string | null
  lastName: string | null
  email: string | null
}

export const useUserStore = defineStore('user', {
  state: () => {
    return {
      token: null as string | null,
      user: {
        firstName: null,
        lastName: null,
        email: null,
      } as User,
      errors: {} as Record<string, string>,
    }
  },
  getters: {
    getUser(): User {
      return this.user
    },
    getFullName(): string {
      return `${this.user.firstName} ${this.user.lastName}`
    },
    getEmail(): string | null {
      return this.user.email
    },
    isLoggedIn(): boolean {
      return !!this.token
    },
  },
  actions: {
    resetUser() {
      this.user = {
        firstName: null,
        lastName: null,
        email: null,
      }
    },
    validateRegisterPayload() {
      console.log('checking')
    },
    register() {
      // this.client.register(this.registerPayload).then((res) => {
      //   console.log(res)
      //   this.token = res.response.token
      // }).catch((err) => {
      //   console.log(err)
      // })
    },
  },
})
