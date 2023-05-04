<script lang="ts" setup>
import { reactive, defineProps, onBeforeMount, ref } from 'vue'
import { API_URL } from '@/utils/config';
import axios from 'axios'
import CourseCard from '@/components/Card/CoursesCard.vue'
import { useAuthStore } from '@/stores/auth';
import { useToast } from 'primevue/usetoast';
const authStore = useAuthStore();
const state = reactive({
    coursesSeach: ""
})
const props = defineProps<{}>()
const courses = ref([])
const toast = useToast();
onBeforeMount(async () => {

    try {
        const response = await axios.get(API_URL + "/course")
        if (response.status === 200) {
            courses.value = response.data
            console.log(courses.value)
        }
        else throw new Error("Can't fetch courses")
    } catch (error) {
        console.log(error)
    }
})

const registerCourse = (code) => {
    const config = {
        headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
        },
    };
    const data = {
        course_code: code
    }
    axios.post(API_URL+"/course-action/register-course", data, config).then((response)=>{
        toast.add({ severity: 'success', summary: 'Sucess', detail: 'Register course success', life: 3000 });
    }).catch((error)=>{
        toast.add({ severity: 'error', summary: 'Error', detail: 'Register course failed', life: 3000 });

    })
}
</script>
<style scoped></style>
<template>
    <h1>Courses</h1>
    <div class="card p-3 mt-3 bottom-0 h-full">
        <CourseCard v-for="(course, index) in courses" :key="index" :name="course.name" :code="course.code"
            :credits="course.credits" :startDate="course.start_date" :endDate="course.end_date"
            :schedules="course.schedules" :details="true" @click="registerCourse(course.code)"></CourseCard>
    </div>
</template>
