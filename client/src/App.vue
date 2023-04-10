<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth';
const authStore = useAuthStore();
authStore.loadTokenFromLocalStorage('accessToken');
authStore.loadTokenFromLocalStorage('refreshToken');
authStore.startRefreshToken()
</script>

<template>
  <RouterView />
</template>
