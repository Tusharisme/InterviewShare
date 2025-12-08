import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('auth_token') || null)
  const userEmail = ref(localStorage.getItem('user_email') || null)
  const userId = ref(localStorage.getItem('user_id') ? parseInt(localStorage.getItem('user_id')) : null)

  const isLoggedIn = computed(() => !!token.value)

  function setAuth(newToken, email, id) {
    token.value = newToken
    userEmail.value = email
    userId.value = id
    
    localStorage.setItem('auth_token', newToken)
    localStorage.setItem('user_email', email)
    localStorage.setItem('user_id', id)
  }

  function clearAuth() {
    token.value = null
    userEmail.value = null
    userId.value = null
    
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user_email')
    localStorage.removeItem('user_id')
  }

  async function login(email, password) {
    const response = await axios.post('/login?include_auth_token', {
      email,
      password
    })
    
    const responseData = response.data.response.user // Flask-Security standard structure
    const newToken = responseData.authentication_token
    const newId = responseData.id
    
    // Sometimes Flask-Security returns success but no token if already logged in differently
    // In strict API mode, we should just get the token.
    if (newToken) {
        setAuth(newToken, email, newId)
        return true
    } else {
         // Should not happen for API login, but if it does, consider it fail
        return false
    }
  }

  async function logout() {
    try {
        await axios.get('/logout')
    } catch (e) {
        // Ignore error if already logged out
    }
    clearAuth()
  }

  return { 
    token, 
    userEmail, 
    userId, 
    isLoggedIn, 
    login, 
    logout 
  }
})
