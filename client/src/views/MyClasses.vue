<script lang="ts" setup>
import { reactive, defineProps, onBeforeMount, ref } from 'vue'
import { useAuthStore } from '@/stores/auth';
import axios from 'axios';
import { API_URL } from '@/utils/config';
import CourseCard from '@/components/Card/CoursesCard.vue'
let authStore = useAuthStore();
import router from "@/router"
const state = reactive({
    coursesSeach: ""
})
const props = defineProps<{}>()
const courses = ref([])

const watchCourse = (code) => {
    router.push({ path: `/home/dashboard/my-classes/${code}` })
}
onBeforeMount(async () => {
    let config = {
        headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
        },
    };
    try {
        const response = await axios.get(API_URL + "/course/my-courses", config)
        if (response.status === 200) {
            courses.value = response.data
            // console.log(courses.value)
        }
        else throw new Error("Can't fetch courses")
    } catch (error) {
        console.log(error)
    }
})


</script>

<style scoped></style>
<template>
    <h1>My classes</h1>
    <span class="p-input-icon-left">
        <i class="pi pi-search" />
        <InputText v-model="state.coursesSeach" placeholder="Search for courses" />
    </span>
    <div class="card p-3 mt-3" v-if="courses.length > 0">

        <CourseCard v-for="(course, index) in courses" :key="index" :name="course.name" :code="course.code"
            :credits="course.credits" :startDate="course.start_date" :endDate="course.end_date"
            :schedules="course.schedules" :details="true" @click="watchCourse(course.code)"></CourseCard>
    </div>
    <div v-else class="card mt-3">
        <i>You have no classes</i>
    </div>
</template>
