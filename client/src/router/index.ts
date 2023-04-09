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
      meta: { requiresAuth: true },
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
      meta: { requiresAuth: false },
      component: () => import("@/views/Login.vue"),
    },
    {
      path: "/register",
      name: "register",
      meta: { requiresAuth: false },
      component: () => import("@/views/Register.vue"),
    },
    {
      path: "/",
      name: "welcome",
      meta: { requiresAuth: true },
      component: () => import("@/views/Welcome.vue"),
    },
  ],
});

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  // make authenticate request
  if (to.meta.requiresAuth) {
    try{
      await authStore.tryAuthenticate();
      next();
    }catch(error){
      next({name: "login"});
    }
  }else{
    if (to.name==="login"||to.name==="register")
    {
      try{
        await authStore.tryAuthenticate();
        next({name: "welcome"});
      }
      catch(error){
        next();
      }
    }
    else next();
  }
});

export default router;
