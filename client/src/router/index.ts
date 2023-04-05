import { createRouter, createWebHistory } from "vue-router";
import AppLayout from "@/layouts/AppLayout.vue";
import { useAuthStore } from "@/stores/auth";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/home",
      name: "home",
      component: AppLayout,
      children: [
        {
          path: "dashboard",
          name: "dashboard",
          component: () => import("@/views/Dashboard.vue"),
        },
        {
          path: "todos",
          name: "todos",
          component: () => import("@/views/Todos.vue"),
        },
      ],
    },
    {
      path: "/login",
      name: "login",
      component: () => import("@/views/Login.vue"),
    },
    {
      path: "/register",
      name: "register",
      component: () => import("@/views/Register.vue"),
    },
    {
      path: "/",
      name: "welcome",
      component: () => import("@/views/Welcome.vue"),
    },
  ],
});

router.beforeEach(async (to, from) => {
  let isAuthenticated = false;
  const authStore = useAuthStore()
  // make authenticate request
  try {
    const response =  await authStore.tryAuthenticate()
    const {username, email} = response.data
    authStore.setEmail(email);
    authStore.setUsername(username);
    console.log(response)
    isAuthenticated = response.status == 200
  } catch (error) {
    console.log(error)
  }
  if (!isAuthenticated) {
    if (to.name !== "login" && to.name !== "register") return { name: "login" };
  }
});

export default router;
