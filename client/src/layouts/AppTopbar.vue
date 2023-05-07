<script setup lang="ts">
import Menubar from "primevue/menubar";
import { RouterLink } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { ref, onMounted } from "vue";
import CreateCourseForm from "@/components/Form/CreateCourseForm.vue";
const authStore = useAuthStore();
const nestedMenuItem = ref([
  {
    // label: 'Dashboard',
    icon: "pi pi-home",
    to: "/dashboard",
  },
  // {
  //     label: 'Chats',
  //     to: '/home/todos'
  // },
  // {
  //     label: 'Groups'
  // }
]);
const userMenu = ref();
const userMenuItems = ref([
  { separator: true },
  { label: "Profile", icon: "pi pi-fw pi-user", to: "/profile" },
  { separator: true },
]);
const toggleUserMenu = (event) => {
  userMenu.value.toggle(event);
};
const openAddCourseDialog = ref(false);

const handleSubmit = () => {
  openAddCourseDialog.value = false;
};
</script>
<style scoped>
.p-menubar {
  border-radius: 0px;
}
:deep(.p-menuitem-text) {
  font-weight: 500;
  font-size: large;
}
:deep(.p-menuitem-icon) {
  font-size: large;
  margin: 0px !important;
}
</style>
<template>
  <div class="layout-topbar">
    <Menubar :model="nestedMenuItem" class="h-5rem text-lg">
      <template #end>
        <Button
          icon="pi pi-user"
          severity="info"
          text
          rounded
          aria-label="User"
          @click="toggleUserMenu"
        />
        <Menu :model="userMenuItems" popup ref="userMenu">
          <template #start>
            <button
              @click=""
              class="w-full p-link flex align-items-center p-2 pl-3 text-color hover:surface-200 border-noround"
            >
              <div class="flex flex-column align">
                <span class="font-bold">{{
                  authStore.first_name + " " + authStore.last_name
                }}</span>
                <span class="text-sm">{{ authStore.email }}</span>
              </div>
            </button>
          </template>
          <template #end>
            <button
              @click="authStore.logout()"
              class="w-full p-link flex align-items-center p-2 pl-4 text-color hover:surface-200 border-noround"
            >
              <i class="pi pi-sign-out" />
              <span class="ml-2">Log Out</span>
            </button>
          </template>
        </Menu>
      </template>
    </Menubar>
  </div>
</template>
