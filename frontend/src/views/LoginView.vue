<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from '../composables/useToast'
import { useAuthStore } from '../stores/auth'

const email = ref('')
const password = ref('')
const error = ref('')
const isSubmitting = ref(false)
const router = useRouter()
const { addToast } = useToast()
const authStore = useAuthStore()

const login = async () => {
    isSubmitting.value = true
    error.value = ''
    try {
        const success = await authStore.login(email.value, password.value)
        
        if (success) {
            addToast('Welcome back!', 'success')
            router.push('/')
        } else {
            error.value = 'Login succeeded but no token received.'
        }

    } catch (err) {
        console.error(err)
        // Extract error message properly from Flask-Security response
        const responseErrors = err.response?.data?.response?.errors
        if (Array.isArray(responseErrors) && responseErrors.length > 0) {
            error.value = responseErrors[0]
        } else if (err.response?.data?.meta?.code === 400) {
            error.value = 'Invalid email or password'
        } else {
            error.value = 'An unexpected error occurred. Please try again.'
        }
        addToast(error.value, 'error')
    } finally {
        isSubmitting.value = false
    }
}
</script>


<template>
    <div class="auth-container">
        <div class="card">
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
                <div v-if="error" class="error-msg">{{ error }}</div>
                <button type="submit" class="btn-primary" style="width: 100%" :disabled="isSubmitting">
                    {{ isSubmitting ? 'Logging in...' : 'Login' }}
                </button>
            </form>
            <p class="auth-footer">Don't have an account? <RouterLink to="/register">Register here</RouterLink></p>
        </div>
    </div>
</template>

<style scoped>
.auth-container {
    max-width: 450px;
    margin: 2rem auto;
}

.form-group {
    margin-bottom: 1.25rem;
}

.error-msg {
    color: var(--color-danger);
    background-color: #fef2f2;
    padding: 0.75rem;
    border-radius: var(--border-radius);
    margin-bottom: 1rem;
}

.auth-footer {
    margin-top: 1.5rem;
    text-align: center;
    color: var(--slate-500);
}
</style>
