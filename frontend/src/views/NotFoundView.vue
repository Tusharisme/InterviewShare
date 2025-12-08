<template>
    <div class="not-found-container">
        <h1>404</h1>
        <h2>Page Not Found</h2>
        <p>The page you are looking for does not exist or has been moved.</p>
        <button @click="router.push('/')" class="btn-primary">Go Home</button>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<style scoped>
.not-found-container {
    text-align: center;
    padding: 4rem 2rem;
}

h1 {
    font-size: 6rem;
    color: var(--primary-500);
    margin-bottom: 1rem;
    line-height: 1;
}

h2 {
    font-size: 2rem;
    margin-bottom: 1rem;
}

p {
    color: var(--slate-500);
    margin-bottom: 2rem;
}
</style>
