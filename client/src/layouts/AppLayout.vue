<script setup lang="ts">
import AppTopbar from './AppTopbar.vue';
import { RouterView } from 'vue-router';
</script>
<style lang="scss" scoped>
.app-layout{
    height: 100%;
    width: 100%;
    .app-main-display {
        padding: 7rem 2rem 2rem;
    }
}
</style>

<template>
    <div class="app-layout">
        <AppTopbar class="fixed z-5 min-w-full"></AppTopbar>
        <div class="app-main-display">
            <RouterView />
        </div>
    </div>
</template>
