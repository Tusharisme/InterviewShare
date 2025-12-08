<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useToast } from '../composables/useToast'

const email = ref('')
const password = ref('')
const error = ref('')
const isSubmitting = ref(false)
const router = useRouter()
const { addToast } = useToast()

const register = async () => {
    isSubmitting.value = true
    error.value = ''
    try {
        await axios.post('/register', {
            email: email.value,
            password: password.value
        })
        
        addToast('Registration successful! Please login.', 'success')
        router.push('/login')

    } catch (err) {
        console.error(err)
        const responseErrors = err.response?.data?.response?.errors
        
        if (Array.isArray(responseErrors) && responseErrors.length > 0) {
            error.value = responseErrors[0]
        } else if (err.response?.data?.response?.field_errors) {
            // Handle field-specific errors often returned by Flask-Security
            const fieldErrors = err.response.data.response.field_errors
            const firstField = Object.keys(fieldErrors)[0]
            error.value = fieldErrors[firstField][0]
        } else {
             error.value = 'Registration failed. Please check your details.'
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
                <div v-if="error" class="error-msg">{{ error }}</div>
                <button type="submit" class="btn-primary" style="width: 100%" :disabled="isSubmitting">
                    {{ isSubmitting ? 'Creating Account...' : 'Register' }}
                </button>
            </form>
            <p class="auth-footer">Already have an account? <RouterLink to="/login">Login here</RouterLink></p>
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
