<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const experiences = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const response = await axios.get('/api/experiences')
    experiences.value = response.data
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load experiences.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="home">
    <h1>Latest Interview Experiences</h1>
    
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <div v-else class="experiences-list">
      <div v-if="experiences.length === 0" class="empty-state">
        No experiences shared yet. Be the first!
      </div>
      
      <div v-for="experience in experiences" :key="experience.id" class="experience-card">
        <div class="card-header">
            <h2>{{ experience.title }}</h2>
            <div v-if="canDelete(experience)" class="actions">
                <button @click="router.push(`/edit/${experience.id}`)" class="edit-btn">Edit</button>
                <button @click="deleteExperience(experience.id)" class="delete-btn">Delete</button>
            </div>
        </div>

        <div class="meta">
            <span class="company">@ {{ experience.company }}</span>
            <span class="role">For: {{ experience.role_title }}</span>
        </div>
        <p class="preview">{{ experience.content.substring(0, 150) }}...</p>
        <div class="author">By: {{ experience.author }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const experiences = ref([])
const loading = ref(true)
const error = ref(null)
const currentUserEmail = localStorage.getItem('user_email')
const router = useRouter()

onMounted(async () => {
    fetchExperiences()
})

const fetchExperiences = async () => {
  try {
    const response = await axios.get('/api/experiences')
    experiences.value = response.data
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load experiences.'
  } finally {
    loading.value = false
  }
}

const canDelete = (experience) => {
    return currentUserEmail && experience.author === currentUserEmail
}

const deleteExperience = async (id) => {
    if (!confirm('Are you sure you want to delete this experience?')) return

    try {
        const token = localStorage.getItem('auth_token')
        await axios.delete(`/api/experiences/${id}`, {
            headers: { 'Authentication-Token': token }
        })
        // Refresh list
        experiences.value = experiences.value.filter(e => e.id !== id)
    } catch (err) {
        console.error(err)
        alert('Failed to delete experience')
    }
}
</script>

<style scoped>
.home {
    padding: 1rem;
}

.experience-card {
    border: 1px solid var(--color-border);
    padding: 1.5rem;
    margin-bottom: 1rem;
    border-radius: 8px;
    background-color: var(--color-background-soft);
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.experience-card h2 {
    margin-top: 0;
    margin-bottom: 0;
}

.delete-btn {
    background-color: #ff4d4f;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
}

.edit-btn {
    background-color: #1890ff;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    margin-right: 0.5rem;
}

.actions {
    display: flex;
    align-items: center;
}


.meta {
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
    color: #666;
    font-size: 0.9rem;
}

.meta span {
    margin-right: 1rem;
    font-weight: bold;
}

.preview {
    color: var(--color-text);
}

.author {
    margin-top: 1rem;
    font-size: 0.8rem;
    font-style: italic;
    color: #888;
}
</style>
