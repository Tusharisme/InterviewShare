<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useToast } from '../composables/useToast'
import { useAuthStore } from '../stores/auth'

const experiences = ref([])
const loading = ref(true)
const error = ref(null)
const searchQuery = ref('')
const router = useRouter()
const { addToast } = useToast()
const authStore = useAuthStore()
let searchTimeout = null

onMounted(async () => {
    fetchExperiences()
})

const fetchExperiences = async () => {
  loading.value = true
  try {
    const params = {}
    if (searchQuery.value) {
        params.q = searchQuery.value
    }
    const response = await axios.get('/api/experiences', { params })
    experiences.value = response.data.map(exp => ({
        ...exp,
        isLiked: exp.liker_ids ? exp.liker_ids.includes(authStore.userId) : false
    }))
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load experiences.'
    addToast('Failed to load experiences', 'error')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
    if (searchTimeout) clearTimeout(searchTimeout)
    searchTimeout = setTimeout(() => {
        fetchExperiences()
    }, 300)
}

const toggleLike = async (experience) => {
    if (!authStore.isLoggedIn) {
        addToast('Please login to like posts', 'warning')
        return
    }

    const previousState = experience.isLiked
    const previousCount = experience.likes_count
    
    experience.isLiked = !experience.isLiked
    experience.likes_count += experience.isLiked ? 1 : -1

    try {
        await axios.post(`/api/experiences/${experience.id}/like`, {}, {
            headers: { 'Authentication-Token': authStore.token }
        })
    } catch (err) {
        experience.isLiked = previousState
        experience.likes_count = previousCount
        addToast('Failed to like post', 'error')
    }
}

const canDelete = (experience) => {
    return authStore.userEmail && experience.author === authStore.userEmail
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

<template>
  <div class="home">
    <div class="head-section">
        <h1>Latest Interview Experiences</h1>
        <div class="search-box">
            <input 
                v-model="searchQuery" 
                @input="handleSearch" 
                type="text" 
                placeholder="Search companies or roles..." 
                class="search-input"
            />
        </div>
    </div>
    
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
        
        <div class="preview-container">
            <p class="preview" :class="{ 'blur-content': !authStore.isLoggedIn }">{{ experience.content }}</p>
            <div v-if="!authStore.isLoggedIn" class="lock-overlay">
                <span class="lock-icon">🔒</span>
                <span class="lock-message">Login to view full experience</span>
                <RouterLink to="/login" class="btn-primary-sm" style="display: inline-block;">Login Now</RouterLink>
            </div>
        </div>
        
        <div class="footer-row">
            <div class="author-info">
                <div class="avatar-placeholder">{{ experience.author.charAt(0).toUpperCase() }}</div>
                <div class="author-details">
                    <span class="author-name">{{ experience.author }}</span>
                    <span class="author-label">Shared 1 min read</span>
                </div>
            </div>
            
            <button 
                @click="toggleLike(experience)" 
                class="like-btn" 
                :class="{ 'liked': experience.isLiked }"
            >
                <span class="heart-icon">{{ experience.isLiked ? '❤️' : '🤍' }}</span>
                <span class="like-count">{{ experience.likes_count }}</span>
            </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.preview-container {
    position: relative;
    margin-bottom: 1.5rem;
}

/* Blur effect when not logged in */
.blur-content {
    filter: blur(5px);
    user-select: none;
    pointer-events: none;
    max-height: 100px;
    overflow: hidden;
}

.lock-overlay {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: rgba(255, 255, 255, 0.9);
    padding: 1rem 1.5rem;
    border-radius: 50px;
    box-shadow: var(--shadow-md);
    text-align: center;
    width: 80%;
    border: 1px solid var(--slate-200);
    z-index: 10;
}

.lock-message {
    color: var(--slate-800);
    font-weight: 600;
    margin-bottom: 0.5rem;
    display: block;
}

.lock-icon {
    font-size: 1.5rem;
    display: block;
    margin-bottom: 0.25rem;
}
.head-section {
    margin-bottom: 2rem;
    text-align: center;
}

.search-box {
    max-width: 500px;
    margin: 1.5rem auto 0;
}

.search-input {
    width: 100%;
    padding: 1rem 1.5rem;
    font-size: 1rem;
    border: 1px solid var(--slate-200);
    border-radius: 50px;
    box-shadow: var(--shadow-sm);
    transition: all 0.2s;
}

.search-input:focus {
    border-color: var(--primary-500);
    box-shadow: 0 0 0 4px var(--primary-50);
    outline: none;
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

.footer-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 1rem;
    border-top: 1px solid var(--slate-100);
}

.author-info {
    display: flex;
    align-items: center;
    gap: 0.75rem;
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

.author-details {
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

.like-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: white;
    border: 1px solid var(--slate-200);
    padding: 0.4rem 0.8rem;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.2s;
}

.like-btn:hover {
    background-color: var(--slate-50);
}

.like-btn.liked {
    border-color: #fda4af;
    background-color: #fff1f2;
    color: #e11d48;
}

.heart-icon {
    font-size: 1.1rem;
}

.like-count {
    font-weight: 600;
    font-size: 0.9rem;
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
