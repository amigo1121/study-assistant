<script lang="ts" setup>
import { reactive, defineProps, onBeforeMount, ref, nextTick } from 'vue'
import { API_URL } from '@/utils/config';
import axios from 'axios'
import CourseCard from '@/components/Card/CoursesCard.vue'
import { useAuthStore } from '@/stores/auth';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from "primevue/useconfirm";
const authStore = useAuthStore();
const state = reactive({
    coursesSeach: ""
})
const props = defineProps<{}>()
const courses = ref([])
const toast = useToast();
const confirm = useConfirm();

async function fetchData() {
    try {
        let config = {
            headers: {
                Authorization: `Bearer ${authStore.accessToken}`,
            },
        };
        const response = await axios.get(API_URL + "/course/available-courses", config)
        if (response.status === 200) {
            courses.value = response.data
            console.log(courses.value)
        }
        else throw new Error("Can't fetch courses")
    } catch (error) {
        console.log(error)
        const message = error.message ? error.message : error.response.data.detail;
        toast.add({ severity: 'error', summary: 'Failed', detail: message, life: 3000 })
    }
}
onBeforeMount(async () => {
    fetchData();
})

const registerCourse = (code) => {
    confirm.require({
        message: 'Do you want to register for this course?',
        header: 'Register Confirmation',
        icon: 'pi pi-info-circle',
        accept: () => {
            const config = {
                headers: {
                    Authorization: `Bearer ${authStore.accessToken}`,
                },
            };
            const data = {
                course_code: code
            }
            axios.post(API_URL + "/course-action/register-course", data, config).then(async (response) => {
                toast.add({ severity: 'success', summary: 'Sucess', detail: 'Register course success', life: 3000 });
                nextTick();
                fetchData();
            }).catch((error) => {
                toast.add({ severity: 'error', summary: 'Error', detail: 'Register course failed', life: 3000 });

            })
        },
        reject: () => {
            toast.add({ severity: 'error', summary: 'Rejected', detail: 'You have rejected', life: 3000 });
        }
    });

}
</script>
<style scoped></style>
<template>
    <h1>Courses</h1>
    <div class="card p-3 mt-3 bottom-0 h-full" v-if="courses.length > 0">
        <CourseCard v-for="(course, index) in courses" :key="index" :name="course.name" :code="course.code"
            :credits="course.credits" :startDate="course.start_date" :endDate="course.end_date"
            :schedules="course.schedules" :details="true" @click="registerCourse(course.code)"></CourseCard>
    </div>
    <div class="card" v-else>
        <p><i>You have no available course</i></p>
    </div>
    <ConfirmDialog></ConfirmDialog>
</template>
