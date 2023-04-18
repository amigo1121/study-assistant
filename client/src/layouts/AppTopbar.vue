<script setup lang="ts">
import Menubar from 'primevue/menubar';
import { RouterLink } from 'vue-router'
import { ref } from 'vue'
const nestedMenuItem = ref([
    {
        label: 'Dashboard',
        to: 'dashboard'
    },
    {
        label: 'Chats',
        to: 'todos'
    },
    {
        label: 'Groups'
    }
])
</script>
<style lang="scss" scoped>
</style>
<template>
    <div class="layout-topbar">
      <Menubar :model="nestedMenuItem" class="h-5rem"></Menubar>
    </div>
</template>
