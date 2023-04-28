<script setup lang="ts">
import Menubar from 'primevue/menubar';
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth';
import { ref, onMounted } from 'vue'
import CreateCourseForm from '@/components/Form/CreateCourseForm.vue';
const authStore = useAuthStore()
const nestedMenuItem = ref([
    {
        label: 'Dashboard',
        to: '/home/dashboard'
    },
    {
        label: 'Chats',
        to: '/home/todos'
    },
    {
        label: 'Groups'
    }
])
const userMenu = ref()
const userMenuItems = ref([
    { separator: true },
    { label: 'Profile', icon: 'pi pi-fw pi-user' },
    { label: 'Settings', icon: 'pi pi-fw pi-cog' },
    { separator: true }
])
const toggleUserMenu = (event) => {
    userMenu.value.toggle(event);
}
const openAddCourseDialog = ref(false)

const handleSubmit = ()=>{
    openAddCourseDialog.value=false
}
onMounted(() => {
    if (authStore.type == 2) {
        nestedMenuItem.value.push({
            label: 'Add course',
            command: () => { openAddCourseDialog.value = true }
        })
    }
})
</script>
<style lang="scss" scoped>
.p-menubar {
    border-radius: 0px;
}
</style>
<template>
    <div class="layout-topbar">
        <Menubar :model="nestedMenuItem" class="h-5rem text-lg">
            <template #end>
                <Button icon="pi pi-user" severity="info" text rounded aria-label="User" @click="toggleUserMenu" />
                <Menu :model="userMenuItems" popup ref="userMenu">
                    <template #start>
                        <button @click=""
                            class="w-full p-link flex align-items-center p-2 pl-3 text-color hover:surface-200 border-noround">
                            <div class="flex flex-column align">
                                <span class="font-bold">{{ authStore.username }}</span>
                                <span class="text-sm">{{ authStore.email }}</span>
                            </div>
                        </button>
                    </template>
                    <template #end>
                        <button @click="authStore.logout()"
                            class="w-full p-link flex align-items-center p-2 pl-4 text-color hover:surface-200 border-noround">
                            <i class="pi pi-sign-out" />
                            <span class="ml-2">Log Out</span>
                        </button>
                    </template>
                </Menu>
            </template>
        </Menubar>
        <Dialog v-model:visible="openAddCourseDialog" modal :style="{ width: '40rem' }" header="Create course">
            <CreateCourseForm @submit="handleSubmit"></CreateCourseForm>
        </Dialog>
    </div>
</template>
