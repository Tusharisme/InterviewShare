<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const title = ref('')
const company = ref('')
const role_title = ref('')
const content = ref('')
const error = ref('')
const router = useRouter()

const createExperience = async () => {
    try {
        const token = localStorage.getItem('auth_token')
        if (!token) {
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
                'Authentication-Token': token,
                'Content-Type': 'application/json'
            }
        })
        
        router.push('/')

    } catch (err) {
        console.error(err)
        error.value = 'Failed to create experience. Please try again.'
    }
}
</script>

<template>
    <div class="create-container">
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
            <div v-if="error" class="error">{{ error }}</div>
            <button type="submit">Publish Experience</button>
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
}

button:hover {
    background-color: hsla(160, 100%, 30%, 1);
}

.error {
    color: red;
    margin-bottom: 1rem;
}
</style>
