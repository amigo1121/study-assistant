<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>
<style lang="scss" scoped>
.app-topbar {
    background-color: #c6c5c5;
    height: 5rem;
    position: fixed;
    width: 100%;
    padding: 0 2rem;
    display: flex;
    align-items: center;
    justify-content: space-evenly;
}
</style>
<template>
    <div class="app-topbar">
        <router-link :to="{ name: 'dashboard' }">Dashboard</router-link>
        <router-link :to="{ name: 'todos' }">To-do List</router-link>
        <router-link :to="{ path: '/login' }">login</router-link>

    </div>
</template>