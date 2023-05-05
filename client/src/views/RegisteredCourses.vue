<script lang="ts" setup>
import { reactive, defineProps, onBeforeMount, ref } from 'vue'
import { useAuthStore } from '@/stores/auth';
import { API_URL } from '@/utils/config';
const authStore = useAuthStore()
import axios from 'axios'
import CourseCard from '@/components/Card/CoursesCard.vue'
import router from "@/router"
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
            courses.value = courses.value.map((course)=>course.course)
            console.log(courses.value)
        }
        else throw new Error("Can't fetch courses")
    } catch (error) {
        console.log(error)
    }
})

const watchCourse = (code) => {
    router.push({ path: `/dashboard/registered-courses/${code}` })
}
</script>
<style scoped></style>
<template>
    <h1>Courses</h1>
    <div class="card p-3 mt-3">
        <CourseCard  v-if="courses.length > 0" v-for="(course, index) in courses" :key="index" :name="course.name" :code="course.code"
            :credits="course.credits" :startDate="course.start_date" :endDate="course.end_date"
            :schedules="course.schedules" :details="false" @click="watchCourse(course.code)"></CourseCard>

        <p v-else> <i>You have no registered course</i></p>
    </div>
</template>
