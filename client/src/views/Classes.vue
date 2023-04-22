<script lang="ts" setup>
import {useEventStore} from '@/stores/events'
import {onMounted, ref} from 'vue';
const eventStore = useEventStore()
const id = ref(0)
const title = ref("")
const start = ref("")
const end = ref("")

const test = () => {
    const newEvent = {
        title: title.value,
        start: start.value,
        end: end.value
    };
    eventStore.createEvent(newEvent);
}

const del = () => {
    eventStore.deleteEvent(id.value);
}

onMounted(() => {
    eventStore.fetchEvents()
})

</script>
<template>
    <div>
        <h3>
            Classes
        </h3>

        <p v-for="(event, index) in eventStore.events" :key="index"> {{event.id}} - {{ event.title }}</p>

        <input type="text" v-model="title">
        <label for="start">
            Start Date
        </label>
        <input type="datetime-local" name="start" v-model="start"/>

        <label for="end">End date</label>
        <input type="datetime-local" name="end" v-model="end">
        <Button @click="test">add events</Button>
        <input type="number" v-model="id">
        <Button @click="del">delete events</Button>

    </div>
</template>
