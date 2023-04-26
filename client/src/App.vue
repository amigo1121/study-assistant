<script setup lang="ts">
import { RouterView } from 'vue-router';
import { useToast } from 'primevue/usetoast';
import { useAuthStore } from './stores/auth';
import { useEventStore } from './stores/events';
import { BaseSocket } from '@/utils/sockets';
import { onMounted, watchEffect } from "vue";
import { sessionExpireRemind } from '@/utils/sessionExpireReminder';
const authStore = useAuthStore();
const eventStore = useEventStore();
const toast = useToast();

authStore.loadTokenFromLocalStorage('accessToken');
authStore.loadTokenFromLocalStorage('refreshToken');

watchEffect(() => {
  if (authStore.accessToken && authStore.accessToken !== "") {
    const socket = BaseSocket.getInstance();

    socket.offAll();
    socket.disconnect();
    socket.set({ auth: { token: authStore.accessToken } });
    socket.connect();

    socket.on("event/add", (event) => { eventStore.addEvent(event) })
    socket.on("event/remove", (event) => { eventStore.removeEvent(event) })
    socket.on("event/update", (event) => { eventStore.modifyEvent(event) })

    // eventStore.register(socket, "event/add", (event) => { eventStore.addEvent(event) })
    // eventStore.register(socket, "event/remove", (event) => { eventStore.removeEvent(event) })
    // eventStore.register(socket, "event/update", (event) => { eventStore.modifyEvent(event) })
  }
})




// setTimeout(()=>{toast.add({severity: 'info', summary: "Info", detail: `Session expires in 1 minutes, you will be loged out.`});},(120-60)*1000)

onMounted(() => {
  sessionExpireRemind(() => { toast.add({ severity: 'info', summary: "Info", detail: `Session expires in 1 minutes, you will be logged out.` }); }, () => { authStore.logout(); })
})

</script>

<template>
  <Toast></Toast>
  <RouterView />
</template>
