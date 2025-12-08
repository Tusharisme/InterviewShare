<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

const register = async () => {
    try {
        // Flask-Security default register endpoint
        await axios.post('/register', {
            email: email.value,
            password: password.value
        })
        
        // After registration, redirect to login
        router.push('/login')

    } catch (err) {
        console.error(err)
        error.value = err.response?.data?.response?.errors?.[0] || 'Registration failed'
    }
}
</script>

<template>
    <div class="auth-container">
        <h1>Register</h1>
        <form @submit.prevent="register">
            <div class="form-group">
                <label>Email</label>
                <input v-model="email" type="email" required placeholder="Enter your email" />
            </div>
            <div class="form-group">
                <label>Password</label>
                <input v-model="password" type="password" required placeholder="Create a password" />
            </div>
            <div v-if="error" class="error">{{ error }}</div>
            <button type="submit">Register</button>
        </form>
        <p>Already have an account? <RouterLink to="/login">Login here</RouterLink></p>
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
