<script setup lang="ts">
import AppTopbar from "./AppTopbar.vue";
import { RouterView } from "vue-router";
import { useRoute } from "vue-router";
import { onMounted } from "vue";
import { useToast } from "primevue/usetoast";

const route = useRoute();
const toast = useToast();
onMounted(() => {
  if (route.query.message) {
    toast.add({
      severity: "info",
      summary: "Infor",
      detail: route.query.message,
      life: 3000,
    });
  }
  console.log("homepage mounted");
});
</script>
<style lang="scss" scoped>
.app-layout {
  height: 100%;
  width: 100%;
  .app-main-display {
    width: 100%;
    padding-top: 5rem;
    padding-bottom: 1rem;
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
