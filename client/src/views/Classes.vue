<script lang="ts" setup>
import {useEventStore} from '@/stores/events'
import {onMounted, ref} from 'vue';
const eventStore = useEventStore()
const id = ref(0)
const title = ref("")

const test = () => {
    const mock = {
        title: title.value,
        start: "start",
        end: "end"
    }

    eventStore.createEvent(mock);
    console.log(eventStore.events)
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
        <Button @click="test">add events</Button>
        <input type="number" v-model="id">
        <Button @click="del">delete events</Button>

    </div>
</template>
