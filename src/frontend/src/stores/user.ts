import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { User, UserJWT } from '@/types/user'
import * as api from '@/api/api'
import router from '@/router'

export const useUserStore = defineStore('user', {
  state: () => {
    return {
      user: {} as UserJWT,
      isLoggedIn: false
    }
  },
  actions: {
    async register(user: User) {
      const res = await api.register(user)
      if (!res.data.success) {
        throw res.data.message
      }
      this.setUser({
        name: user.name,
        token: res.data.token
      })

      router.replace({ name: 'home' })
    },
    async login(user: User) {
      const res = await api.login(user)

      this.setUser({
        name: user.name,
        token: res.data.token
      })

      router.replace({ name: 'home' })
    },
    async autoLogin() {
      const user = {
        name: localStorage.getItem('username'),
        token: localStorage.getItem('token')
      } as UserJWT

      if (!user.token || !user.name) {
        return
      }

      this.setUser(user)
    },
    setUser(user: UserJWT) {
      this.user = user
      this.isLoggedIn = true

      localStorage.setItem('token', user.token)
      localStorage.setItem('username', user.name)
    },
    logout() {
      this.user = {} as UserJWT
      this.isLoggedIn = false

      localStorage.removeItem('token')
      localStorage.removeItem('username')
    }
  }
})
