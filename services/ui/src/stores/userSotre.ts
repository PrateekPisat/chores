// stores/counter.js
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
      } as User
    }
  },
  actions: {
    resetUser() {
      this.user = {
        firstName: null,
        lastName: null,
        email: null,
      }
    },
    login(email: string, _password: string) {
      // fetch user and set it
      console.log(_password)
      this.token = 'mytoken'
      this.user = {
        firstName: 'Eduardo',
        lastName: 'Sanchez',
        email: email,
      }
    },
    logout() {
      this.token = null
      this.resetUser()
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
    }
  }
})
