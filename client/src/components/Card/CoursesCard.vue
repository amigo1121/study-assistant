<script lang="ts" setup>
import { defineProps, withDefaults } from "vue";
interface Props {
    name?: String
    code: String
    schedule: Object
    teacher: String
    credits: Number
    details?: Boolean
    startDate: String
    endDate: String
}
const props = withDefaults(defineProps<Props>(),{
    name: "default",
    details: false
})
</script>
<style lang="scss" scoped></style>
<template>
    <div class="card border-round-3xl">
        <h3>Course name: {{ props.name }}</h3>
        <h4>Course code: {{ props.code }}</h4>
        <template v-if="details">
            <h4>Schedue: </h4>
        <ul class="list-none">
            <li v-for="(value, key) in props.schedule" :key="key">
                {{ key.toString().toUpperCase() }}: {{ value.start }} - {{ value.end }}
            </li>
        </ul>
        <h4>Start date: {{ props.startDate }}</h4>
        <h4>End date: {{ props.endDate }}</h4>
        </template>
        <h4>
            Teacher: {{ props.teacher }}
        </h4>
        <h4>
            Credit: {{ props.credits }}
        </h4>
    </div>
</template>
