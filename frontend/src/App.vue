<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/" class="brand">InterviewShare</RouterLink>
        <div class="links">
            <RouterLink to="/">Home</RouterLink>
            <RouterLink v-if="isLoggedIn" to="/create">Share Experience</RouterLink>
            <RouterLink v-if="!isLoggedIn" to="/login">Login</RouterLink>
            <RouterLink v-if="!isLoggedIn" to="/register">Register</RouterLink>
            <a v-if="isLoggedIn" href="#" @click.prevent="logout">Logout</a>
        </div>
      </nav>
    </div>
  </header>

  <main>
    <RouterView />
  </main>
</template>

<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { ref } from 'vue'

const isLoggedIn = ref(!!localStorage.getItem('auth_token'))
const router = useRouter()

const logout = () => {
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user_email')
    isLoggedIn.value = false
    router.push('/login')
}
</script>

<style scoped>
header {
  line-height: 1.5;
  background-color: var(--color-background-soft);
  padding: 1rem 0;
  border-bottom: 1px solid var(--color-border);
}

.wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

nav {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--color-heading);
    text-decoration: none;
}

.links a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
  color: var(--color-text);
  text-decoration: none;
}

.links a:first-of-type {
  border: 0;
}

main {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 1rem;
}
</style>
