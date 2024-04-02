import type { User } from '@/types/user'
import axios from 'axios'

export const BASE_URL = 'http://127.0.0.1:3000'

export const uploadUrl = `${BASE_URL}/upload`

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 0
})

export const processImages = async () => {
  return api.get('/process_images')
}

export const register = async (user: User) => {
  return api.post('/register', user)
}

export const login = async (user: User) => {
  return api.post('/login', user)
}
