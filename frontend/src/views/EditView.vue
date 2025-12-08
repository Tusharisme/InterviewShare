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
    <div class="create-container">
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
            <div v-if="error" class="error">{{ error }}</div>
            <button type="submit">Update Experience</button>
            <button type="button" class="cancel-btn" @click="router.push('/')">Cancel</button>
        </form>
    </div>
</template>

<style scoped>
.create-container {
    max-width: 800px;
    margin: 2rem auto;
    padding: 2rem;
    border: 1px solid var(--color-border);
    border-radius: 8px;
    background-color: var(--color-background-soft);
}

.form-group {
    margin-bottom: 1rem;
}

.two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: bold;
}

input, textarea {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-family: inherit;
}

button {
    width: 100%;
    padding: 1rem;
    background-color: hsla(160, 100%, 37%, 1);
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    margin-bottom: 0.5rem;
}

button:hover {
    background-color: hsla(160, 100%, 30%, 1);
}

.cancel-btn {
    background-color: #666;
}

.cancel-btn:hover {
    background-color: #555;
}

.error {
    color: red;
    margin-bottom: 1rem;
}
</style>
