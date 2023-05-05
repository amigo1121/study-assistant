<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
const authStore = useAuthStore()


</script>
<style lang="scss" scoped>

</style>
<template>
    <h1>Welcome {{ authStore.first_name }} {{ authStore.last_name }}</h1>
</template>
