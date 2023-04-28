<script lang="ts" setup>
import { reactive, defineProps, onBeforeMount, ref } from 'vue'
import { useAuthStore } from '@/stores/auth';
import { API_URL } from '@/utils/config';
const authStore = useAuthStore()
import axios from 'axios'
import CourseCard from '@/components/Card/CoursesCard.vue'
import AssignmentCard from '@/components/Card/AssignmentCard.vue';
const state = reactive({
    coursesSeach: ""
})
const props = defineProps<{}>()
const courses = ref([])
const assignments = ref([])

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

            courses.value.forEach(course =>{
                assignments.value= assignments.value.concat(course.assignments)
            })

            console.log(courses.value)
            console.log(assignments.value)
        }
        else throw new Error("Can't fetch Assignments")
    } catch (error) {
        console.log(error)
    }
})
</script>
<style scoped></style>
<template>
    <h1>Assignments</h1>
    <div class="card max-h-full p-3 overflow-scroll mt-3">
        <AssignmentCard v-for="(assignment, index) in assignments" :key="index"
            :id="assignment.id"
            :title="assignment.title"
            :importance="assignment.importance"
            :description="assignment.description"
            :dueDate="assignment.due_date"
        ></AssignmentCard>
    </div>
</template>
