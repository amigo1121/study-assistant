<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
const authStore = useAuthStore()


</script>
<style lang="scss">

</style>
<template>
    <h1>Welcome</h1>
    <h2>Username: {{ authStore.username }}</h2>
    <h2>Email: {{ authStore.email }}</h2>
    <button @click="authStore.logout">Logout</button>
    <router-link to="/home/todos">Todos</router-link>
</template>
