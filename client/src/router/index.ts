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
          redirect: "/home/dashboard/overview" ,
          name: "dashboard",
          component: () => import("@/views/Dashboard.vue"),
          children: [
            {
              path: "overview",
              name: "overview",
              component : () => import("@/views/Overview.vue")
            },
            {
              path: "calendar",
              name: "calendar",
              component: () => import("@/views/Calendar.vue")
            },
            {
              path: "assignments",
              name: "assignments",
              component: () => import('@/views/Assignments.vue')
            },
            {
              path: "groups",
              name: "groups",
              component: () =>  import('@/views/Groups.vue')
            },
            {
              path: "my-day",
              name: "my-day",
              component: () => import('@/views/MyDay.vue')
            },
            {
              path: "classes",
              name: "classes",
              component: () => import('@/views/Classes.vue')
            },
            {
              path: "courses",
              name: "courses",
              component: () => import ('@/views/Courses.vue')
            },
            {
              path: "my-classes",
              name: "my-classes",
              component: () => import ('@/views/MyClasses.vue')
            }

          ]
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

router.beforeEach(async (to, from) => {
  const authStore = useAuthStore();
  // make authenticate request
  if (to.meta.requiresAuth) {
    try{
      await authStore.tryAuthenticate();
      return;
    }catch(error){
      if(authStore.accessToken)
      return ({name: "login",query: { sessionExpired: true }});
      else return ({name:"login"})
    }
  }else{
    if (to.name==="login"||to.name==="register")
    {
      try{
        await authStore.tryAuthenticate();
        return ({name: "welcome"});
      }
      catch(error){
        return;
      }
    }
    else return;
  }
});

export default router;
