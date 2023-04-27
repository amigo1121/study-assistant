<script lang="ts" setup>
import { reactive, defineProps } from 'vue'
import CourseCard from '@/components/Card/CoursesCard.vue'
const state = reactive({
    coursesSeach: ""
})
const props = defineProps<{}>()
</script>
<style scoped></style>
<template>
    <h1>Courses</h1>
    <span class="p-input-icon-left">
        <i class="pi pi-search" />
        <InputText v-model="state.coursesSeach" placeholder="Search for courses" />
    </span>
    <div class="card max-h-30rem p-3 overflow-scroll mt-3">
        <CourseCard code="abcdef" teacher="Johndoe" :schedule="{
            monday: {
                start: '12:00',
                end: '14:00',
            },
            tuesday: {
                start: '10:00',
                end: '11:30'
            }
        }" :credits="4"
        startDate="2023-04-10"
        endDate="2023-04-10"
        ></CourseCard>
        <CourseCard code="abcdef" teacher="Johndoe" :schedule="{
            monday: {
                start: '12:00',
                end: '14:00',
            },
            tuesday: {
                start: '10:00',
                end: '11:30'
            }
        }" :credits="4"
        startDate="2023-04-10"
        endDate="2023-04-10"
        ></CourseCard>
    </div>

</template>
