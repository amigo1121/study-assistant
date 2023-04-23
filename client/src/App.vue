<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth';
import { useEventStore } from './stores/events';
import { BaseSocket } from '@/utils/sockets'
const authStore = useAuthStore();
const eventStore = useEventStore();

authStore.loadTokenFromLocalStorage('accessToken');
authStore.loadTokenFromLocalStorage('refreshToken');
const socket = BaseSocket.getInstance(authStore.getAccessToken);

eventStore.register(socket, "event/add", (event)=>{eventStore.addEvent(event)})
eventStore.register(socket, "event/remove", (event)=>{eventStore.removeEvent(event)})
eventStore.register(socket, "event/update", (event)=>{eventStore.modifyEvent(event)})
</script>

<template>
  <RouterView />
</template>
