<script lang="ts" setup>
import { defineProps, withDefaults, ref } from "vue";
import AssignmentFormVue from "../Form/AssignmentForm.vue";
import { useAuthStore } from "@/stores/auth";
import { API_URL } from "@/utils/config";
import moment from "moment";
import axios from "axios";
import { useToast } from "primevue/usetoast";
import router from "@/router";
const toast = useToast();
const authStore = useAuthStore();
const openCreateNewAssignment = ref(false);
const openCourseActions = ref(false);
interface Props {
  name?: String;
  code: String;
  schedules: Array<Object>;
  teacher?: String;
  credits: Number;
  details?: Boolean;
  startDate: String;
  endDate: String;
}
const props = withDefaults(defineProps<Props>(), {
  name: "default",
  details: false,
});

const createNewAssignment = () => {
  openCreateNewAssignment.value = true;
};
const registerOrLeaveCourse = () => {
  openCourseActions.value = true;
};
const handleRegister = async () => {
  if (confirm("Confirm course registration")) {
    try {
      let config = {
        headers: {
          Authorization: `Bearer ${authStore.accessToken}`,
        },
      };
      const response = await axios.post(
        API_URL + "/course-action/register-course",
        { course_code: props.code },
        config
      );

      if (response.status !== 200)
        throw new Error("Something wrong, cannot register for course");

      toast.add({
        severity: "success",
        summary: "Success",
        detail: "Course register sucess",
        life: 2000,
      });
    } catch (error) {
      console.log(error);
      toast.add({
        severity: "error",
        summary: "Error",
        detail: "Failed to register",
        life: 2000,
      });
    }
  }
};
const handleDrop = async () => {
  if (confirm("Confirm course deregistration")) {
    try {
      let config = {
        headers: {
          Authorization: `Bearer ${authStore.accessToken}`,
        },
      };
      const response = await axios.post(
        API_URL + "/course-action/drop-course",
        { course_code: props.code },
        config
      );

      if (response.status !== 200)
        throw new Error("Something wrong, cannot deregister for course");

      toast.add({
        severity: "success",
        summary: "Success",
        detail: "Course deregister sucess",
        life: 2000,
      });
      router.go();
    } catch (error) {
      console.log(error);
      toast.add({
        severity: "error",
        summary: "Error",
        detail: "Failed to deregister",
        life: 2000,
      });
    }
  }
};
const handleClick = () => {
  if (authStore.type == 2) createNewAssignment();
  else registerOrLeaveCourse();
};
const addAssignment = async (assignmentData) => {
  try {
    let config = {
      headers: {
        Authorization: `Bearer ${authStore.accessToken}`,
      },
    };
    try {
      assignmentData.course_code = props.code;
      const response = await axios.post(
        API_URL + "/assignments",
        assignmentData,
        config
      );
      if (response.status != 201) throw new Error("Cannot create new course");
      router.go();
    } catch (error) {
      console.log(error);
    }
  } catch (error) {}
};

const menu = ref(null);
const toggle = (event) => {
  menu.value.toggle(event);
};
</script>
<style lang="scss" scoped>
.card {
  &:hover {
    background-color: rgba($color: #000000, $alpha: 0.1);
  }
  position: relative;
}
.menu {
  position: absolute;
  top: 1rem;
  right: 1rem;
}
</style>
<template>
  <div class="card border-round-3xl">
    <h3>Course name: {{ props.name }}</h3>
    <h4>Course code: {{ props.code }}</h4>
    <template v-if="details && props.schedules.length > 0">
      <h4>Schedule:</h4>
      <ul class="list-none">
        <li
          v-for="(schedule, index) in props.schedules"
          :key="index"
          class="mb-2"
        >
          {{ schedule.week_day }}:
          {{ moment(schedule.start_time, "HH:mm:ss").format("HH:mm") }} -
          {{ moment(schedule.end_time, "HH:mm:ss").format("HH:mm") }}
        </li>
      </ul>
      <h4>Start date: {{ props.startDate }}</h4>
      <h4>End date: {{ props.endDate }}</h4>
    </template>
    <h4 v-if="!!props.teacher">Teacher: {{ props.teacher }}</h4>
    <h4>Credits: {{ props.credits }}</h4>
    <div class="menu">
      <slot name="menu" :course_code="props.code"> </slot>
    </div>
  </div>
</template>
