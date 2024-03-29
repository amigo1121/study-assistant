import {
  createRouter,
  createWebHistory,
  createWebHashHistory,
} from "vue-router";
import AppLayout from "@/layouts/AppLayout.vue";
import { useAuthStore } from "@/stores/auth";

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: "/",
      name: "root",
      component: AppLayout,
      redirect: { name: "dashboard" },
      meta: { requiresAuth: true },
      children: [
        {
          path: "/",
          name: "dashboard",
          redirect: { name: "welcome" },
          component: () => import("@/views/Dashboard.vue"),
          children: [
            {
              path: "",
              name: "welcome",
              component: () => import("@/views/Welcome.vue"),
            },
            {
              path: "overview",
              name: "overview",
              component: () => import("@/views/Overview.vue"),
            },
            {
              path: "calendar",
              name: "calendar",
              component: () => import("@/views/Calendar.vue"),
            },
            {
              path: "assignments",
              name: "assignments",
              component: () => import("@/views/Assignments.vue"),
            },
            {
              path: "my-day",
              name: "my-day",
              component: () => import("@/views/MyDay.vue"),
            },
            {
              path: "available-courses",
              name: "available-courses",
              component: () => import("@/views/Courses.vue"),
            },
            {
              path: "my-classes",
              name: "my-classes",
              component: () => import("@/views/MyClasses.vue"),
            },
            {
              path: "registered-courses",
              name: "registered-courses",
              component: () => import("@/views/RegisteredCourses.vue"),
            },
            {
              path: "/my-classes/:coursecode",
              name: "class",
              component: () => import("@/views/Class.vue"),
            },
            {
              path: "/registered-courses/:coursecode",
              name: "course-detail",
              component: () => import("@/views/CourseDetail.vue"),
            },
            {
              path: "timer",
              name: "timer",
              component: () => import("@/views/Timer.vue"),
            },
          ],
        },
        {
          path: "/profile",
          name: "profile",
          meta: { requiresAuth: true },
          component: () => import("@/views/Profile.vue"),
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
  ],
});

router.beforeEach(async (to, from) => {
  const authStore = useAuthStore();
  // make authenticate request
  if (to.meta.requiresAuth) {
    try {
      await authStore.tryAuthenticate();
      return;
    } catch (error) {
      if (authStore.accessToken) {
        authStore.clearToken();
        authStore.resetData();
        return { name: "login", query: { sessionExpired: true } };
      } else return { name: "login" };
    }
  } else {
    if (to.name === "login" || to.name === "register") {
      try {
        await authStore.tryAuthenticate();
        return {
          name: "root",
          query: {
            message: "You already logged in, please log out to continue",
          },
        };
      } catch (error) {
        return;
      }
    } else return;
  }
});

export default router;
