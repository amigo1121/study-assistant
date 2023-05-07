<script setup lang="ts">
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import listPlugin from "@fullcalendar/list";
import ModifyEventForm from "@/components/Form/ModifyEventForm.vue";
import CreateEventForm from "@/components/Form/CreateEventForm.vue";
import { getNewEvent } from "@/utils/event";
import { useEventStore } from "@/stores/events";
import { ref, onBeforeMount, reactive } from "vue";
import { useToast } from "primevue/usetoast";

const toast = useToast();
const eventStore = useEventStore();
const currentEvents = ref([]);
const openCreateDialog = ref<boolean>(false);
const openModifyDialog = ref<boolean>(false);
const createEventProps = reactive({ start: "", end: "", allDay: false });
const modifyEventProps = reactive({
  title: "",
  start: "",
  end: "",
  allDay: false,
});
const show = () => {
  toast.add({ severity: "info", summary: "Info", detail: "Message Content" });
};

const submitSuccess = () => {
  openCreateDialog.value = false;
  toast.add({
    severity: "success",
    summary: "Success",
    detail: "New event added",
    life: 2000,
  });
};

const modifySuccess = (message) => {
  toast.add({
    severity: "success",
    summary: "Success",
    detail: `${message} Success`,
    life: 2000,
  });
  openModifyDialog.value = false;
};

const handleDateSelect = async (selectInfo) => {
  // let title = prompt('Please enter a new title for your event')
  // let calendarApi = selectInfo.view.calendar

  // calendarApi.unselect() // clear date selection

  // if (title) {
  //   const inputEvent = {
  //     title: title,
  //     start: selectInfo.startStr,
  //     end: selectInfo.endStr,
  //   }

  //   await eventStore.createEvent(inputEvent);
  // }
  createEventProps.start = selectInfo.startStr;
  createEventProps.end = selectInfo.endStr;
  createEventProps.allDay = selectInfo.allDay;
  openCreateDialog.value = true;
};
const handleEventClick = async (clickInfo) => {
  // modify event of delete it
  // if (confirm(`Are you sure you want to delete the event '${clickInfo.event.title}'`)) {
  //   await eventStore.deleteEvent(clickInfo.event.id);
  // }

  modifyEventProps.title = clickInfo.event.title;
  modifyEventProps.start = clickInfo.event.startStr;
  modifyEventProps.end = clickInfo.event.endStr;
  modifyEventProps.allDay = clickInfo.event.allDay;
  modifyEventProps.id = Number(clickInfo.event.id);

  // console.log(modifyEventProps)
  openModifyDialog.value = true;
};
const handleEvents = (events) => {
  currentEvents.value = events;
};

const handleDrop = (dropInfor) => {
  const updateEvent = getNewEvent(dropInfor.event);
  eventStore.updateEvent(updateEvent);
};

const calendarOptions = ref({
  plugins: [
    listPlugin,
    dayGridPlugin,
    timeGridPlugin,
    interactionPlugin, // needed for dateClick
  ],
  headerToolbar: {
    left: "prev,next today",
    center: "title",
    right: "dayGridMonth,timeGridWeek,timeGridDay",
  },
  initialView: "dayGridMonth",
  events: eventStore.events, // alternatively, use the `events` setting to fetch from a feed
  editable: true,
  selectable: true,
  selectMirror: true,
  dayMaxEvents: true,
  weekends: true,
  navLinks: true,
  select: handleDateSelect,
  eventClick: handleEventClick,
  eventsSet: handleEvents,
  eventDrop: handleDrop,
  eventResize: handleDrop,
  /* you can update a remote database when these fire:
  eventAdd:
  eventChange:
  eventRemove:
  */
});

onBeforeMount(async () => {
  try {
    await eventStore.fetchEvents();
    calendarOptions.value.events = eventStore.events;
  } catch (error) {
    console.log(error);
  }
});
</script>

<template>
  <div class="demo-app">
    <div class="demo-app-main">
      <FullCalendar :options="calendarOptions">
        <template v-slot:eventContent="arg">
          <b>{{ arg.timeText }}</b>
          <i>{{ arg.event.title }}</i>
        </template>
      </FullCalendar>
    </div>
    <Dialog
      v-model:visible="openCreateDialog"
      modal
      :style="{ width: '40rem' }"
      header="Create event"
    >
      <CreateEventForm
        :start="createEventProps.start"
        :end="createEventProps.end"
        :allDay="createEventProps.allDay"
        @submit="submitSuccess"
      ></CreateEventForm>
    </Dialog>
    <Dialog
      v-model:visible="openModifyDialog"
      modal
      :style="{ width: '40rem' }"
      header="Modify event"
    >
      <ModifyEventForm
        :id="modifyEventProps.id"
        :title="modifyEventProps.title"
        :start="modifyEventProps.start"
        :end="modifyEventProps.end"
        :allDay="modifyEventProps.allDay"
        @submit="modifySuccess"
      ></ModifyEventForm>
    </Dialog>
  </div>
</template>

<style lang="scss" scoped>
b {
  margin-right: 3px;
}

.demo-app {
  min-height: 100%;
}
.demo-app-main {
  flex-grow: 1;
  padding: 3em;
}
.fc {
  /* the calendar root */
  max-width: 1100px;
  margin: 0 auto;
}
</style>
