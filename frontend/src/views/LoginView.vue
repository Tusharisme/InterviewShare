<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

const login = async () => {
    try {
        const response = await axios.post('/login?include_auth_token', {
            email: email.value,
            password: password.value
        })
        
        // Flask-Security returns the token in specific ways depending on config
        // Default with JSON: response.data.response.user.authentication_token or similar
        // Let's inspect the response in dev, but for now assume standard
        
        const token = response.data.response.user.authentication_token
        
        if (token) {
            localStorage.setItem('auth_token', token)
            localStorage.setItem('user_email', email.value)
            // Redirect to home or dashboard
            router.push('/')
            // Simple force reload to update nav state (can be improved with store)
            setTimeout(() => window.location.reload(), 100)
        } else {
            error.value = 'Login succeeded but no token received.'
        }

    } catch (err) {
        console.error(err)
        error.value = err.response?.data?.response?.errors?.[0] || 'Invalid credentials'
    }
}
</script>

<template>
    <div class="auth-container">
        <h1>Login</h1>
        <form @submit.prevent="login">
            <div class="form-group">
                <label>Email</label>
                <input v-model="email" type="email" required placeholder="Enter your email" />
            </div>
            <div class="form-group">
                <label>Password</label>
                <input v-model="password" type="password" required placeholder="Enter your password" />
            </div>
            <div v-if="error" class="error">{{ error }}</div>
            <button type="submit">Login</button>
        </form>
        <p>Don't have an account? <RouterLink to="/register">Register here</RouterLink></p>
    </div>
</template>

<style scoped>
.auth-container {
    max-width: 400px;
    margin: 2rem auto;
    padding: 2rem;
    border: 1px solid var(--color-border);
    border-radius: 8px;
}

.form-group {
    margin-bottom: 1rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
}

input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
}

button {
    width: 100%;
    padding: 0.75rem;
    background-color: hsla(160, 100%, 37%, 1);
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
}

button:hover {
    background-color: hsla(160, 100%, 30%, 1);
}

.error {
    color: red;
    margin-bottom: 1rem;
}
</style>
