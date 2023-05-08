<script lang="ts" setup>
import { reactive, defineProps, onBeforeMount, ref, nextTick } from "vue";
import { useAuthStore } from "@/stores/auth";
import { API_URL } from "@/utils/config";
import axios from "axios";
import CourseCard from "@/components/Card/CoursesCard.vue";
import CourseCardMenu from "./CourseCardMenu.vue";
import router from "@/router";
import { useToast } from "primevue/usetoast";
import { useConfirm } from "primevue/useconfirm";
const authStore = useAuthStore();
const courses = ref([]);
const toast = useToast();
const confirm = useConfirm();

function getMenuItem(course_code) {
  return [
    {
      label: "Options",
      items: [
        {
          label: "Update",
          icon: "pi pi-refresh",
          command: () => {
            toast.add({
              severity: "success",
              summary: "Updated",
              detail: `${course_code}`,
              life: 3000,
            });
          },
        },
        {
          label: "Delete",
          icon: "pi pi-times",
          command: () => {
            toast.add({
              severity: "warn",
              summary: "Delete",
              detail: `${course_code}`,
              life: 3000,
            });
          },
        },
      ],
    },
  ];
}

const dropCourse = (code) => {
  confirm.require({
    message: "Do you want to drop this course?",
    header: "Register Confirmation",
    icon: "pi pi-info-circle",
    accept: () => {
      const config = {
        headers: {
          Authorization: `Bearer ${authStore.accessToken}`,
        },
      };
      const data = {
        course_code: code,
      };
      axios
        .post(API_URL + "/course-action/drop-course", { course_code: code }, config)
        .then(async (response) => {
          toast.add({
            severity: "success",
            summary: "Sucess",
            detail: "Drop course success",
            life: 3000,
          });
          nextTick();
          fetchData();
        })
        .catch((error) => {
          toast.add({
            severity: "error",
            summary: "Error",
            detail: "Drop course failed",
            life: 3000,
          });
        });
    },
    reject: () => {
      toast.add({
        severity: "error",
        summary: "Rejected",
        detail: "You have rejected",
        life: 3000,
      });
    },
  });
};

function fetchData() {
  const config = {
    headers: {
      Authorization: `Bearer ${authStore.accessToken}`,
    },
  };
  axios
    .get(API_URL + "/course/registered-courses", config)
    .then((response) => {
      updateCourse(response.data.registered_courses);
    })
    .catch((error) => {
      console.log(error.response.data.detail);
    });
}
async function updateCourse(newCourseData) {
  courses.value = newCourseData.map((course) => course.course);
  await nextTick();
  console.log(courses.value);
}
onBeforeMount(async () => {
  try {
    let config = {
      headers: {
        Authorization: `Bearer ${authStore.accessToken}`,
      },
    };
    const response = await axios.get(
      API_URL + "/course/registered-courses",
      config
    );
    if (response.status === 200) {
      courses.value = response.data.registered_courses;
      courses.value = courses.value.map((course) => course.course);
    } else throw new Error("Can't fetch courses");
  } catch (error) {
    console.log(error);
  }
});

const watchCourse = (code) => {
  router.push({ path: `/dashboard/registered-courses/${code}` });
};
</script>
<style scoped></style>
<template>
  <h1>Courses</h1>
  <div class="card p-3 mt-3">
    <CourseCard
      v-if="courses.length > 0"
      v-for="(course, index) in courses"
      :key="index"
      :name="course.name"
      :code="course.code"
      :credits="course.credits"
      :startDate="course.start_date"
      :endDate="course.end_date"
      :schedules="course.schedules"
      :details="false"
    >
      <template #menu>
        <CourseCardMenu
          :coursecode="course.code"
          @detail="watchCourse"
          @drop="dropCourse"
        ></CourseCardMenu>
      </template>
    </CourseCard>

    <p v-else><i>You have no registered course</i></p>
  </div>
  <ConfirmDialog></ConfirmDialog>
</template>
