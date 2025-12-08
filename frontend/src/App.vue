<template>
  <header>
    <div class="container navbar">
      <RouterLink to="/" class="brand">
        <span class="logo-icon">🎓</span> InterviewShare
      </RouterLink>
      <nav class="nav-links">
        <RouterLink to="/">Feed</RouterLink>
        
        <template v-if="authStore.isLoggedIn">
           <RouterLink to="/create" class="btn-link">Share Experience</RouterLink>
           <RouterLink to="/profile" class="nav-text">My Profile</RouterLink>
           <a href="#" @click.prevent="logout" class="nav-text">Logout</a>
        </template>

        
        <template v-else>
          <RouterLink to="/login" class="nav-text">Login</RouterLink>
          <RouterLink to="/register" class="btn-primary-sm">Get Started</RouterLink>
        </template>
      </nav>
    </div>
  </header>

  <main class="container">
    <RouterView />
  </main>
  
  <footer>
    <div class="container">
        InterviewShare &copy; 2024. Built for Students.
    </div>
  </footer>
  
  <ToastContainer />
</template>

<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { ref } from 'vue'
import ToastContainer from './components/ToastContainer.vue'
import { useToast } from './composables/useToast'
import { useAuthStore } from './stores/auth'

const router = useRouter()
const { addToast } = useToast()
const authStore = useAuthStore()

const logout = () => {
    authStore.logout()
    addToast('Logged out successfully', 'info')
    router.push('/login')
}
</script>


<style scoped>
header {
  background-color: white;
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: var(--shadow-sm);
}

.navbar {
  height: 70px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--primary-600);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.logo-icon {
  font-size: 1.5rem;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.nav-links a:not([class]) {
    color: var(--slate-500);
    font-weight: 600;
}
.nav-links a:not([class]):hover {
    color: var(--primary-600);
}

.nav-text {
    color: var(--slate-500);
    font-weight: 600;
}
.nav-text:hover {
    color: var(--slate-800);
}

.btn-primary-sm {
    background-color: var(--primary-600);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: var(--border-radius);
    font-weight: 600;
    transition: all 0.2s;
}
.btn-primary-sm:hover {
    background-color: var(--primary-700);
    text-decoration: none;
}

.btn-link {
    color: var(--primary-600);
    font-weight: 600;
}

main {
    flex: 1;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

footer {
    padding: 2rem 0;
    background-color: white;
    border-top: 1px solid var(--border-color);
    color: var(--text-muted);
    font-size: 0.9rem;
    text-align: center;
}
</style>
