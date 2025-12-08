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
        <div class="empty-icon">📝</div>
        <h3>No experiences yet</h3>
        <p>Be the first to share your interview journey!</p>
      </div>
      
      <div v-for="experience in experiences" :key="experience.id" class="card experience-card">
        <div class="card-header">
            <h2>{{ experience.title }}</h2>
            <div v-if="canDelete(experience)" class="actions">
                <button @click="router.push(`/edit/${experience.id}`)" class="btn-sm btn-edit">Edit</button>
                <button @click="deleteExperience(experience.id)" class="btn-sm btn-delete">Delete</button>
            </div>
        </div>
        
        <div class="meta-row">
            <span class="badge badge-primary">{{ experience.company }}</span>
            <span class="badge badge-secondary">{{ experience.role_title }}</span>
            <span class="date">{{ new Date(experience.created_at).toLocaleDateString() }}</span>
        </div>
        
        <p class="preview">{{ experience.content }}</p>
        
        <div class="author-row">
            <div class="avatar-placeholder">{{ experience.author.charAt(0).toUpperCase() }}</div>
            <div class="author-info">
                <span class="author-name">{{ experience.author }}</span>
                <span class="author-label">Shared 1 min read</span>
            </div>
        </div>
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
        experiences.value = experiences.value.filter(e => e.id !== id)
    } catch (err) {
        console.error(err)
        alert('Failed to delete experience')
    }
}
</script>

<style scoped>
.head-section {
    margin-bottom: 2rem;
    text-align: center;
}

.empty-state {
    text-align: center;
    padding: 3rem;
    background: white;
    border-radius: var(--border-radius-lg);
    border: 1px dashed var(--slate-300);
}

.empty-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.experience-card {
    margin-bottom: 1.5rem;
    background: white;
}

.experience-card h2 {
    font-size: 1.25rem;
    color: var(--slate-900);
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
}

.meta-row {
    display: flex;
    gap: 0.5rem;
    align-items: center;
    margin-bottom: 1.25rem;
}

.badge {
    padding: 0.25rem 0.75rem;
    border-radius: 9999px; /* Pill shape */
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
}

.badge-primary {
    background-color: var(--primary-100);
    color: var(--primary-700);
}

.badge-secondary {
    background-color: var(--slate-100);
    color: var(--slate-600);
}

.date {
    margin-left: auto;
    font-size: 0.85rem;
    color: var(--slate-400);
}

.preview {
    color: var(--slate-600);
    margin-bottom: 1.5rem;
    white-space: pre-wrap;
}

.author-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding-top: 1rem;
    border-top: 1px solid var(--slate-100);
}

.avatar-placeholder {
    width: 32px;
    height: 32px;
    background-color: var(--primary-100);
    color: var(--primary-600);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.85rem;
}

.author-info {
    display: flex;
    flex-direction: column;
    line-height: 1.2;
}

.author-name {
    font-size: 0.9rem;
    font-weight: 600;
}

.author-label {
    font-size: 0.8rem;
    color: var(--slate-400);
}

.btn-sm {
    padding: 0.4rem 0.8rem;
    font-size: 0.85rem;
    border-radius: 6px;
    margin-left: 0.5rem;
    border: none;
    cursor: pointer;
    font-weight: 600;
}

.btn-edit {
    background-color: var(--slate-100);
    color: var(--slate-700);
}
.btn-edit:hover {
    background-color: var(--slate-200);
}

.btn-delete {
    background-color: #fee2e2;
    color: #ef4444;
}
.btn-delete:hover {
    background-color: #fecaca;
}
</style>
