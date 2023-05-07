<script lang="ts" setup>
import {
  capitalize,
  timeValidation,
  getMinutesDifference,
} from "@/utils/datetime";
import { useToast } from "primevue/usetoast";
import Calendar from "primevue/calendar";
import moment from "moment";
import axios from "axios";
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import { API_URL } from "@/utils/config";
import router from "@/router";
const toast = useToast();
const authStore = useAuthStore();
const name = ref("");
const code = ref("");
const credits = ref(1);
const start = ref(null);
const end = ref(null);
const errorMsg = ref([]);
const schedule = ref({
  monday: {
    apply: false,
    from: null,
    to: null,
  },
  tuesday: {
    apply: false,
    from: null,
    to: null,
  },
  wednesday: {
    apply: false,
    from: null,
    to: null,
  },
  thursday: {
    apply: false,
    from: null,
    to: null,
  },
  friday: {
    apply: false,
    from: null,
    to: null,
  },
});
const emit = defineEmits(["submit"]);

const extractHour = (d: Date) => {
  return moment(d).format("HH:mm");
};

const validateInput = (input) => {
  errorMsg.value = [];
  let { start_date, end_date, schedules } = input;
  start_date = moment(start_date);
  end_date = moment(end_date);
  if (!input.name) errorMsg.value.push("Course name is empty");
  if (!input.code) errorMsg.value.push("Course code is empty");
  if (!start_date.isValid())
    errorMsg.value.push("Course's start date is empty or invalid");
  if (!end_date.isValid())
    errorMsg.value.push("Course's end date is empty or invalid");
  if (
    start_date.isValid() &&
    end_date.isValid() &&
    end_date.diff(start_date, "days") < 1
  )
    errorMsg.value.push("Course's start date must be before course's end date");
  if (schedules.length === 0)
    errorMsg.value.push("Course's schedule details missed");
  schedules.forEach((schedule) => {
    let { start_time, end_time, week_day } = schedule;
    if (!timeValidation(start_time))
      errorMsg.value.push(
        `Course's start time on ${capitalize(week_day)} is empty`
      );
    if (!timeValidation(end_time))
      errorMsg.value.push(
        `Course's end time on ${capitalize(week_day)} is empty`
      );
    if (
      timeValidation(start_time) &&
      timeValidation(end_time) &&
      getMinutesDifference(start_time, end_time) < 0
    )
      errorMsg.value.push(
        `Course's start time on ${capitalize(
          week_day
        )} must be before the end time`
      );
  });
  return errorMsg.value.length === 0;
};

const submit = async () => {
  const inputForm = {
    name: name.value,
    credits: credits.value,
    code: code.value,
    start_date: moment(start.value).format("YYYY-MM-DD"),
    end_date: moment(end.value).format("YYYY-MM-DD"),
    schedules: Object.entries(schedule.value)
      .filter(([key, value]) => value.apply)
      .map(([key, value]) => {
        return {
          week_day: key.toUpperCase(),
          start_time: extractHour(value.from),
          end_time: extractHour(value.to),
        };
      }),
  };
  // console.log(inputForm)

  if (validateInput(inputForm)) {
    let config = {
      headers: {
        Authorization: `Bearer ${authStore.accessToken}`,
      },
    };
    try {
      const response = await axios.post(API_URL + "/course", inputForm, config);
      if (response.status != 200) throw new Error("Cannot create new course");
      emit("submit", response.data);
    } catch (error) {
      console.log(error.response.data);
      toast.add({
        severity: "error",
        summary: "Error",
        detail: error.response.data.detail,
        life: 3000,
      });
    }
  } else {
    errorMsg.value.forEach((error, index) => {
      toast.add({
        severity: "error",
        summary: "Error",
        detail: error,
        life: 3000 + index * 10,
      });
    });
  }
};

const upper = (str) => {
  return str.charAt(0).toUpperCase() + str.slice(1);
};
</script>
<style lang="scss" scoped></style>
<template>
  <div class="p-fluid formgrid grid">
    <div class="field col-12">
      <label for="courseName">Course name</label>
      <InputText id="courseName" type="text" v-model="name" />
    </div>
    <div class="field col-6">
      <label for="courseCode">Course code</label>
      <InputText id="courseCode" type="text" v-model="code" />
    </div>

    <div class="field col-6">
      <label for="courseCredits">Credits</label>
      <InputNumber
        id="courseCredits"
        v-model="credits"
        inputId="minmax"
        :min="1"
        :max="5"
      />
    </div>

    <div class="field col-6">
      <label for="startDate">Start date</label>
      <Calendar
        v-model="start"
        id="startDate"
        dateFormat="yy-mm-dd"
        showButtonBar
      />
    </div>
    <div class="field col-6">
      <label for="endDate">End date</label>
      <Calendar
        v-model="end"
        id="endDate"
        dateFormat="yy-mm-dd"
        showButtonBar
      />
    </div>

    <div class="field col-12">
      <label for="schedule">Schedule</label>
      <div id="schedule">
        <div class="grid" v-for="(value, key) in schedule" :key="key">
          <div class="mb-1 col-12">
            <Checkbox v-model="value.apply" :binary="true" /> {{ upper(key) }}
          </div>
          <div class="field col-6" :class="{ 'p-disabled': !value.apply }">
            <label for="startTime">From</label>
            <Calendar v-model="value.from" id="startTime" timeOnly />
          </div>
          <div class="field col-6" :class="{ 'p-disabled': !value.apply }">
            <label for="endTime">To</label>
            <Calendar v-model="value.to" id="endTime" timeOnly />
          </div>
        </div>
      </div>
    </div>
    <div class="flex col-12 gap-4 flex-nowrap justify-content-end">
      <Button
        class="flex max-w-min"
        severity="info"
        label="Save"
        @click="submit"
      />
    </div>
  </div>
</template>
