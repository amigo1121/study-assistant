<script lang="ts" setup>
import AppSidebar from "@/layouts/AppSidebar.vue";
import { ref, onBeforeMount, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";

const sidebar = ref();
const content = ref();

const sidebarItems = ref([
  {
    // Statistic of Assignments, Tasks, etc
    label: "Overview",
    name: "overview",
  },
  {
    // Calendar of events, classes
    label: "Calendar",
    name: "calendar",
  },
  {
    // Show a list of task that need to do today
    label: "My day",
    name: "my-day",
  },
  {
    // List of assignments, create new, etc
    label: "Assignments",
    name: "assignments",
  },
  {
    label: "Available Courses",
    name: "available-courses",
  },
  {
    label: "Registered courses",
    name: "registered-courses",
  },
  {
    label: "Pomodoro Timer",
    name: "timer",
  },
]);

onBeforeMount(() => {
  const authStore = useAuthStore();
  if (authStore.role === "TEACHER") {
    sidebarItems.value = [
      {
        label: "My classes",
        name: "my-classes",
      },
    ];
  }
});

onMounted(() => {
  const sidebarWidth = sidebar.value.offsetWidth;
  content.value.style["padding-left"] = `calc(${sidebarWidth}px + 1rem)`;
});
</script>
<style lang="scss" scoped>
.task-list,
.assignment-list {
  height: 50vh;
  overflow-y: auto;
}
.dashboard {
  .dashboard__sidebar {
    position: fixed;
    top: 5rem;
    bottom: 0px;
    min-width: 15rem;
    padding: 1rem;
    z-index: 4;
    overflow: auto;
  }

  .dashboard__content {
    width: 100%;
    padding-top: 1rem;
    padding-right: 1rem;
  }
}
</style>
<template>
  <div class="dashboard">
    <div class="dashboard__sidebar bg-primary" ref="sidebar">
      <AppSidebar :model="sidebarItems" />
    </div>
    <div class="dashboard__content" ref="content">
      <router-view></router-view>
    </div>
  </div>
</template>
