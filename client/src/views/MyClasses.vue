<script lang="ts" setup>
import { reactive, defineProps, onBeforeMount, ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import axios from "axios";
import { API_URL } from "@/utils/config";
import CourseCard from "@/components/Card/CoursesCard.vue";
import CreateCourseForm from "@/components/Form/CreateCourseForm.vue";
import { useToast } from "primevue/usetoast";

const authStore = useAuthStore();
const toast = useToast();
import router from "@/router";

const props = defineProps<{}>();
const courses = ref([]);
const openAddCourseDialog = ref(false);
const watchCourse = (code) => {
  router.push({ path: `/home/dashboard/my-classes/${code}` });
};
onBeforeMount(async () => {
  let config = {
    headers: {
      Authorization: `Bearer ${authStore.accessToken}`,
    },
  };
  try {
    const response = await axios.get(API_URL + "/course/my-courses", config);
    if (response.status === 200) {
      courses.value = response.data;
      // console.log(courses.value)
    } else throw new Error("Can't fetch courses");
  } catch (error) {
    console.log(error);
    const message = error.message ? error.message : error.response.data.detail;
    toast.add({
      severity: "error",
      summary: "Failed",
      detail: message,
      life: 3000,
    });
  }
});
const toggleDialog = () => {
  openAddCourseDialog.value = !openAddCourseDialog.value;
};

const handleSubmit = (responseData) => {
  courses.value.push(responseData);
  toast.add({
    severity: "success",
    summary: "Sucsess",
    detail: "New course created successfully",
    life: 3000,
  });
  toggleDialog();
};
</script>

<style scoped></style>
<template>
  <Dialog
    v-model:visible="openAddCourseDialog"
    modal
    :style="{ width: '50rem' }"
    header="Create course"
  >
    <CreateCourseForm @submit="handleSubmit"></CreateCourseForm>
  </Dialog>
  <div class="flex justify-content-between">
    <h1>My classes</h1>
    <Button label="Add classes" class="mb-3" @click="toggleDialog"></Button>
  </div>
  <div class="card p-3" v-if="courses.length > 0">
    <CourseCard
      v-for="(course, index) in courses"
      :key="index"
      :name="course.name"
      :code="course.code"
      :credits="course.credits"
      :startDate="course.start_date"
      :endDate="course.end_date"
      :schedules="course.schedules"
      :details="true"
      @click="watchCourse(course.code)"
    ></CourseCard>
  </div>
  <div v-else class="card">
    <i>You have no classes</i>
  </div>
</template>
