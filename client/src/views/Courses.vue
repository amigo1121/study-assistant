<script lang="ts" setup>
import { reactive, defineProps, onBeforeMount, ref, nextTick } from "vue";
import { API_URL } from "@/utils/config";
import axios from "axios";
import CourseCard from "@/components/Card/CoursesCard.vue";
import { useAuthStore } from "@/stores/auth";
import { useToast } from "primevue/usetoast";
import { useConfirm } from "primevue/useconfirm";
import moment from "moment";
import type { Moment } from "moment";
const authStore = useAuthStore();
const state = reactive({
  coursesSeach: "",
});
const props = defineProps<{}>();
const courses = ref([]);
const toast = useToast();
const confirm = useConfirm();

async function fetchData() {
  try {
    let config = {
      headers: {
        Authorization: `Bearer ${authStore.accessToken}`,
      },
    };
    const response = await axios.get(
      API_URL + "/course/available-courses",
      config
    );
    if (response.status === 200) {
      courses.value = response.data;
    } else throw new Error("Can't fetch courses");
  } catch (error) {
    console.log(error);
    const message = error.message ? error.message : error.response.data.detail;
    toast.add({
      severity: "error",
      summary: "Failed",
      detail: message,
      life: 1000,
    });
  }
}
onBeforeMount(async () => {
  fetchData();
});

function getDaysOfWeek(startDate, endDate, dayOfWeek): Moment[] | string {
  let dates = [];
  let currentDate = moment(startDate).startOf("day");
  let end = moment(endDate).startOf("day");

  // Day of week dictionary
  let days = {
    SUNDAY: 0,
    MONDAY: 1,
    TUESDAY: 2,
    WEDNESDAY: 3,
    THURSDAY: 4,
    FRIDAY: 5,
    SATURDAY: 6,
  };

  if (days.hasOwnProperty(dayOfWeek.toUpperCase())) {
    dayOfWeek = days[dayOfWeek.toUpperCase()];
  } else {
    return "Invalid day of the week";
  }

  while (currentDate.day() !== dayOfWeek) {
    currentDate.add(1, "days");
  }

  while (!currentDate.isAfter(end, "day")) {
    dates.push(currentDate.clone());
    currentDate.add(1, "week");
  }

  return dates;
}

function addCourseSchedule(code) {
  const config = {
    headers: {
      Authorization: `Bearer ${authStore.accessToken}`,
    },
  };
  axios
    .get(API_URL + `/course/schedule/code/${code}`, config)
    .then((response) => {
      console.log("course schedule", response.data);
      const { name } = response.data;
      console.log("today", moment().days());
      console.log("start_date", moment(response.data.start_date).days());
      console.log("end_date", moment(response.data.end_date).days());
      let events = [];

      response.data.schedules.forEach((schedule) => {
        const { week_day, start_time, end_time } = schedule;
        let [start_hours, start_minutes, start_seconds] = start_time.split(":");
        let [end_hours, end_minutes, end_seconds] = end_time.split(":");
        const dayList = getDaysOfWeek(
          response.data.start_date,
          response.data.end_date,
          week_day
        );
        if (typeof dayList !== "string") {
          dayList.forEach((day) => {
            const start = day.clone();
            start.set("hour", start_hours);
            start.set("minute", start_minutes);
            start.set("second", start_seconds);

            const end = day.clone();
            end.set("hour", end_hours);
            end.set("minute", end_minutes);
            end.set("second", end_seconds);

            events.push({
              title: name,
              start: start.format(),
              end: end.format(),
            });
          });
        }
      });
      // console.log(events)
      axios
        .post(API_URL + "/events/multiple", { events: events }, config)
        .then((response) => {
          console.log(response);
          toast.add({
            severity: "success",
            summary: "Success",
            detail: response.data.message,
            life: 1000,
          });
        })
        .catch((error) => {
          console.log(error);
          const message = error.message ? error.message : null;
          toast.add({
            severity: "error",
            summary: "Error",
            detail: message,
            life: 1000,
          });
        });
    });
}

const registerCourse = (code) => {
  confirm.require({
    message: "Do you want to register for this course?",
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
        .post(API_URL + "/course-action/register-course", data, config)
        .then(async (response) => {
          toast.add({
            severity: "success",
            summary: "Sucess",
            detail: "Register course success",
            life: 1000,
          });
          nextTick();
          await fetchData();
          await addCourseSchedule(code);
        })
        .catch((error) => {
          toast.add({
            severity: "error",
            summary: "Error",
            detail: "Register course failed",
            life: 1000,
          });
        });
    },
    reject: () => {
      toast.add({
        severity: "error",
        summary: "Rejected",
        detail: "You have rejected",
        life: 1000,
      });
    },
  });
};
</script>
<style scoped></style>
<template>
  <h1>Courses</h1>
  <div class="card p-3 mt-3 bottom-0 h-full" v-if="courses.length > 0">
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
      @click="registerCourse(course.code)"
    ></CourseCard>
  </div>
  <div class="card" v-else>
    <p><i>You have no available course</i></p>
  </div>
  <ConfirmDialog></ConfirmDialog>
</template>
