<template>
  <div class="profile-container">
    <div class="head-section">
        <h1>My Experiences</h1>
        <p>Manage the interview experiences you have shared.</p>
    </div>
    
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error-msg">{{ error }}</div>
    
    <div v-else class="experiences-list">
      <div v-if="experiences.length === 0" class="empty-state">
        <div class="empty-icon">📂</div>
        <h3>No experiences yet</h3>
        <p>You haven't shared any interview experiences.</p>
        <button @click="router.push('/create')" class="btn-primary" style="margin-top: 1rem">Share One Now</button>
      </div>
      
      <div v-for="experience in experiences" :key="experience.id" class="card experience-card">
        <div class="card-header">
            <h2>{{ experience.title }}</h2>
            <div class="actions">
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
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useToast } from '../composables/useToast'
import { useAuthStore } from '../stores/auth'

const experiences = ref([])
const loading = ref(true)
const error = ref(null)
const router = useRouter()
const { addToast } = useToast()
const authStore = useAuthStore()

onMounted(async () => {
    fetchMyExperiences()
})

const fetchMyExperiences = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/experiences/me', {
         headers: { 'Authentication-Token': authStore.token }
    })
    experiences.value = response.data
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load your experiences.'
    addToast('Failed to load experiences', 'error')
  } finally {
    loading.value = false
  }
}

const deleteExperience = async (id) => {
    if (!confirm('Are you sure you want to delete this experience?')) return

    try {
        await axios.delete(`/api/experiences/${id}`, {
            headers: { 'Authentication-Token': authStore.token }
        })
        
        addToast('Experience deleted', 'success')
        experiences.value = experiences.value.filter(e => e.id !== id)
    } catch (err) {
        console.error(err)
        addToast('Failed to delete experience', 'error')
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

.error-msg {
    color: var(--color-danger);
    background-color: #fef2f2;
    padding: 0.75rem;
    border-radius: var(--border-radius);
    margin-bottom: 1rem;
}
</style>
