<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useToast } from '../composables/useToast'
import { useAuthStore } from '../stores/auth'

const title = ref('')
const company = ref('')
const role_title = ref('')
const content = ref('')
const error = ref('')
const isSubmitting = ref(false)
const router = useRouter()
const { addToast } = useToast()
const authStore = useAuthStore()

const createExperience = async () => {
    isSubmitting.value = true
    error.value = ''
    try {
        if (!authStore.token) {
            addToast('You must be logged in to share.', 'warning')
            router.push('/login')
            return
        }

        await axios.post('/api/experiences', {
            title: title.value,
            company: company.value,
            role_title: role_title.value,
            content: content.value
        }, {
            headers: {
                'Authentication-Token': authStore.token,
                'Content-Type': 'application/json'
            }
        })
        
        addToast('Experience published successfully!', 'success')
        router.push('/')

    } catch (err) {
        console.error(err)
        const msg = 'Failed to create experience. Please try again.'
        error.value = msg
        addToast(msg, 'error')
    } finally {
        isSubmitting.value = false
    }
}
</script>


<template>
    <div class="auth-container">
        <div class="card">
            <h1>Share Interview Experience</h1>
            <form @submit.prevent="createExperience">
                <div class="form-group">
                    <label>Title</label>
                    <input v-model="title" type="text" required placeholder="e.g. SDE-1 Interview at Google" />
                </div>
                <div class="form-group two-col">
                    <div>
                        <label>Company</label>
                        <input v-model="company" type="text" required placeholder="e.g. Google" />
                    </div>
                    <div>
                        <label>Role</label>
                        <input v-model="role_title" type="text" required placeholder="e.g. Software Engineer" />
                    </div>
                </div>
                <div class="form-group">
                    <label>Experience Content</label>
                    <textarea v-model="content" rows="10" required placeholder="Describe your interview process..."></textarea>
                </div>
                <div v-if="error" class="error-msg">{{ error }}</div>
                <button type="submit" class="btn-primary" style="width: 100%" :disabled="isSubmitting">
                    {{ isSubmitting ? 'Publishing...' : 'Publish Experience' }}
                </button>
            </form>
        </div>
    </div>
</template>

<style scoped>
.auth-container {
    max-width: 800px;
    margin: 0 auto;
}

.form-group {
    margin-bottom: 1.25rem;
}

.two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.25rem;
}

.error-msg {
    color: var(--color-danger);
    background-color: #fef2f2;
    padding: 0.75rem;
    border-radius: var(--border-radius);
    margin-bottom: 1rem;
}
</style>
