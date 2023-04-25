<script setup lang="ts">
import moment from 'moment';
import { RouterView } from 'vue-router';
import { useToast } from 'primevue/usetoast';
import { useAuthStore } from './stores/auth';
import { useEventStore } from './stores/events';
import { BaseSocket } from '@/utils/sockets';
import { onMounted } from "vue";
import { sessionExpireRemind } from '@/utils/sessionExpireReminder'
const authStore = useAuthStore();
const eventStore = useEventStore();
const toast = useToast();

authStore.loadTokenFromLocalStorage('accessToken');
authStore.loadTokenFromLocalStorage('refreshToken');
const socket = BaseSocket.getInstance(authStore.getAccessToken);

eventStore.register(socket, "event/add", (event) => { eventStore.addEvent(event) })
eventStore.register(socket, "event/remove", (event) => { eventStore.removeEvent(event) })
eventStore.register(socket, "event/update", (event) => { eventStore.modifyEvent(event) })
// setTimeout(()=>{toast.add({severity: 'info', summary: "Info", detail: `Session expires in 1 minutes, you will be loged out.`});},(120-60)*1000)

onMounted(() => {
  sessionExpireRemind(() => { toast.add({ severity: 'info', summary: "Info", detail: `Session expires in 1 minutes, you will be logged out.` }); }, () => { authStore.logout(); })
})

</script>

<template>
  <Toast></Toast>
  <RouterView />
</template>
