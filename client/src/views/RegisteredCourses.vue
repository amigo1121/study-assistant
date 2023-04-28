<script lang="ts" setup>
import { reactive, defineProps, onBeforeMount, ref } from 'vue'
import { useAuthStore } from '@/stores/auth';
import { API_URL } from '@/utils/config';
const authStore = useAuthStore()
import axios from 'axios'
import CourseCard from '@/components/Card/CoursesCard.vue'
const state = reactive({
    coursesSeach: ""
})
const props = defineProps<{}>()
const courses = ref([])

onBeforeMount(async () => {

    try {
        let config = {
                headers: {
                    Authorization: `Bearer ${authStore.accessToken}`,
                },
            };
        const response = await axios.get(API_URL + "/course/registered-courses",config)
        if (response.status === 200) {
            courses.value = response.data.registered_courses
            console.log(courses.value)
        }
        else throw new Error("Can't fetch courses")
    } catch (error) {
        console.log(error)
    }
})
</script>
<style scoped></style>
<template>
    <h1>Courses</h1>
    <div class="card max-h-full p-3 overflow-scroll mt-3">

        <CourseCard v-for="(course, index) in courses" :key="index" :name="course.name" :code="course.code"
            :credits="course.credits" :startDate="course.start_date" :endDate="course.end_date"
            :schedules="course.schedules" :details="true"></CourseCard>
    </div>
</template>
