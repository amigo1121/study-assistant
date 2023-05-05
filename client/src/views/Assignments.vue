<script lang="ts" setup>
import { reactive, defineProps, onBeforeMount, ref } from 'vue'
import { useAuthStore } from '@/stores/auth';
import { API_URL } from '@/utils/config';
const authStore = useAuthStore()
import axios from 'axios'
// import AssignmentCard from '@/components/Card/AssignmentCard.vue';
import AssignmentPanel from '@/components/AssignmentPanel.vue';

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
                assignments.value= assignments.value.concat(course.course.assignments)
            })

            console.log("course",courses.value)
            console.log("ass",assignments.value)
        }
        else throw new Error("Can't fetch Assignments")
    } catch (error) {
        console.log(error)
    }
})
</script>
<style scoped>
:deep(.p-panel .p-panel-header, .p-panel-content) {
    border-radius: 0px;
}

:deep(.p-panel .p-panel-content) {
    border-radius: 0px;
}
</style>
<template>
    <h1>Assignments</h1>
    <div v-if="assignments.length > 0">
            <div class="card">
                <AssignmentPanel v-for="(assignment, index) in assignments" :key="index" :name="assignment.name"
                    :description="assignment.description" :deadline="assignment.due_date" :id="assignment.id"
                    readOnly
                    >
                    <div v-html="assignment.description"></div>
                </AssignmentPanel>
            </div>
        </div>
        <div v-else>
            <div class="card">
                <i>No assignments</i>
            </div>
        </div>
</template>
