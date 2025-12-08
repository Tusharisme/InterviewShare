<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter, useRoute } from 'vue-router'

const title = ref('')
const company = ref('')
const role_title = ref('')
const content = ref('')
const error = ref('')
const loading = ref(true)

const router = useRouter()
const route = useRoute()
const experienceId = route.params.id

onMounted(async () => {
    try {
        const response = await axios.get(`/api/experiences/${experienceId}`)
        const data = response.data
        title.value = data.title
        company.value = data.company
        role_title.value = data.role_title
        content.value = data.content
    } catch (err) {
        console.error(err)
        error.value = 'Failed to load experience details.'
    } finally {
        loading.value = false
    }
})

const updateExperience = async () => {
    try {
        const token = localStorage.getItem('auth_token')
        if (!token) {
            router.push('/login')
            return
        }

        await axios.put(`/api/experiences/${experienceId}`, {
            title: title.value,
            company: company.value,
            role_title: role_title.value,
            content: content.value
        }, {
            headers: {
                'Authentication-Token': token,
                'Content-Type': 'application/json'
            }
        })
        
        router.push('/')

    } catch (err) {
        console.error(err)
        error.value = 'Failed to update experience. Please try again.'
    }
}
</script>

<template>
    <div class="auth-container">
        <div class="card">
            <h1>Edit Experience</h1>
            
            <div v-if="loading">Loading...</div>
            
            <form v-else @submit.prevent="updateExperience">
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
                
                <div class="actions">
                    <button type="submit">Update Experience</button>
                    <button type="button" class="btn-secondary" @click="router.push('/')">Cancel</button>
                </div>
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

.actions {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
}

button {
    flex: 1;
}

.error-msg {
    color: var(--color-danger);
    background-color: #fef2f2;
    padding: 0.75rem;
    border-radius: var(--border-radius);
    margin-bottom: 1rem;
}
</style>
