<template>
  <div class="not-found">
    <h1>404</h1>
    <h2>Page Not Found</h2>
    <p>The page you are looking for does not exist.</p>
    <div class="actions">
        <RouterLink to="/" class="btn-primary">Go to Feed</RouterLink>
        <RouterLink to="/login" class="btn-link">Login</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.not-found {
    text-align: center;
    padding: 4rem 1rem;
}
h1 {
    font-size: 6rem;
    color: var(--primary-200);
    line-height: 1;
    margin-bottom: 1rem;
}
h2 {
    color: var(--slate-700);
    margin-bottom: 1rem;
}
.actions {
    margin-top: 2rem;
    display: flex;
    gap: 1rem;
    justify-content: center;
    align-items: center;
}
</style>
