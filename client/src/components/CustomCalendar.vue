<script setup lang="ts">
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import { INITIAL_EVENTS, createEventId , createMockEvent, getNewEvent} from '@/utils/event'
import { useEventStore } from '@/stores/events'
import { ref, onMounted, onBeforeMount, computed} from 'vue';
const eventStore = useEventStore();

const currentEvents = ref([])
const handleDateSelect = async (selectInfo) => {
  let title = prompt('Please enter a new title for your event')
  let calendarApi = selectInfo.view.calendar

  calendarApi.unselect() // clear date selection

  if (title) {
    const inputEvent = {
      title: title,
      start: selectInfo.startStr,
      end: selectInfo.endStr,
    }

    await eventStore.createEvent(inputEvent);
  }
}
const handleEventClick = async (clickInfo) => {
  // modify event of delete it
  if (confirm(`Are you sure you want to delete the event '${clickInfo.event.title}'`)) {
    await eventStore.deleteEvent(clickInfo.event.id);
  }
}
const handleEvents = (events) => {
  currentEvents.value = events

}

const handleDrop = (dropInfor)=>{
  const updateEvent = getNewEvent(dropInfor.event)
  eventStore.updateEvent(updateEvent)
}


const calendarOptions = ref({
  plugins: [
    dayGridPlugin,
    timeGridPlugin,
    interactionPlugin // needed for dateClick
  ],
  headerToolbar: {
    left: 'prev,next today',
    center: 'title',
    right: 'dayGridMonth,timeGridWeek,timeGridDay'
  },
  initialView: 'dayGridMonth',
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
  eventResize: handleDrop
  /* you can update a remote database when these fire:
  eventAdd:
  eventChange:
  eventRemove:
  */
})

onBeforeMount(async()=>{
try {
  await eventStore.fetchEvents();
  calendarOptions.value.events = eventStore.events;
} catch (error) {
  console.log(error)
}
})




</script>

<template>
  <div class='demo-app'>
    <div class='demo-app-main'>
      <FullCalendar class='demo-app-calendar' :options='calendarOptions'>
        <template v-slot:eventContent='arg'>
          <b>{{ arg.timeText }}</b>
          <i>{{ arg.event.title }}</i>
        </template>
      </FullCalendar>
    </div>
  </div>
</template>

<style lang='css' scoped>
h2 {
  margin: 0;
  font-size: 16px;
}

ul {
  margin: 0;
  padding: 0 0 0 1.5em;
}

li {
  margin: 1.5em 0;
  padding: 0;
}

b {
  /* used for event dates/times */
  margin-right: 3px;
}

.demo-app {
  display: flex;
  min-height: 100%;
  font-family: Arial, Helvetica Neue, Helvetica, sans-serif;
  font-size: 14px;
}

.demo-app-sidebar {
  width: 300px;
  line-height: 1.5;
  background: #eaf9ff;
  border-right: 1px solid #d3e2e8;
}

.demo-app-sidebar-section {
  padding: 2em;
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
