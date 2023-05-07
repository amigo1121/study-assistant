<script setup lang="ts">
import { ref, defineProps, onBeforeMount } from "vue";
import { useEventStore } from "@/stores/events";
import Calendar from "primevue/calendar";
import InputSwitch from "primevue/inputswitch";
import moment from "moment";

const props = defineProps<{
  start: string;
  end: string;
  allDay: boolean;
}>();
const eventStore = useEventStore();
const startDate = ref();
const endDate = ref();
const startTime = ref();
const endTime = ref();
const title = ref<string>("");
const allDay = ref<boolean>(false);
const valid = ref<boolean>(true);
const emit = defineEmits(["submit"]);

const validate = () => {
  valid.value = true;
  valid.value = valid.value && title.value !== "";
  if (allDay.value) {
    valid.value =
      valid.value &&
      moment(startDate.value).isValid() &&
      moment(endDate.value).isValid() &&
      moment(startDate.value).diff(moment(endDate.value), "days") < 0;
  } else {
    valid.value =
      valid.value &&
      moment(startDate.value).isValid() &&
      moment(endDate.value).isValid() &&
      moment(startDate.value).diff(moment(endDate.value), "days") <= 0;
    if (moment(startDate.value).diff(moment(endDate.value), "days") === 0) {
      valid.value =
        valid.value &&
        moment(startTime.value).diff(moment(endTime.value), "seconds") < 0;
    }
  }
  return valid.value;
};
const submit = async () => {
  if (validate()) {
    const inputEvent = {
      title: title.value,
      start: "",
      end: "",
    };

    if (allDay.value) {
      inputEvent.start = moment(startDate.value).format("YYYY-MM-DD");
      inputEvent.end = moment(endDate.value).format("YYYY-MM-DD");
    } else {
      const startTimeHour = moment(startTime.value).get("hour");
      const startTimeMinute = moment(startTime.value).get("minute");
      const endTimeHour = moment(endTime.value).get("hour");
      const endTimeMinute = moment(endTime.value).get("minute");
      inputEvent.start = moment(startDate.value)
        .hour(startTimeHour)
        .minute(startTimeMinute)
        .format();
      inputEvent.end = moment(endDate.value)
        .hour(endTimeHour)
        .minute(endTimeMinute)
        .format();
    }
    try {
      await eventStore.createEvent(inputEvent);
      emit("submit");
    } catch (error) {
      console.log(error);
    }
  }
};

onBeforeMount(() => {
  startDate.value = moment(props.start).toDate();
  endDate.value = moment(props.end).toDate();
  allDay.value = props.allDay;
  if (!props.allDay) {
    startTime.value = moment(props.start).toDate();
    endTime.value = moment(props.end).toDate();
  }
});
</script>
<template>
  <div class="p-fluid formgrid grid">
    <div class="field col-12">
      <label for="title">Title</label>
      <InputText id="title" type="text" v-model="title" />
    </div>

    <div class="field col-12">
      <div class="mb-1">All day</div>
      <InputSwitch v-model="allDay" />
    </div>
    <div class="field col-6">
      <label for="startDate">From</label>
      <Calendar
        v-model="startDate"
        id="startDate"
        dateFormat="yy-mm-dd"
        showButtonBar
      />
    </div>
    <div class="field col-6" v-if="!allDay">
      <label for="startTime">At</label>
      <Calendar v-model="startTime" id="startTime" timeOnly />
    </div>
    <div class="field col-6">
      <label for="endDate">To</label>
      <Calendar
        v-model="endDate"
        id="endDate"
        dateFormat="yy-mm-dd"
        showButtonBar
      />
    </div>
    <div class="field col-6" v-if="!allDay">
      <label for="endTime">At</label>
      <Calendar v-model="endTime" id="endTime" timeOnly />
    </div>
    <div class="col-12 mb-3" v-if="!valid">
      <InlineMessage severity="error">Wrong input</InlineMessage>
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
<style lang="scss" scoped></style>
