<script lang="ts" setup>
import { API_URL } from '@/utils/config';
import axios from 'axios'
import { useRoute } from 'vue-router'
import { onBeforeMount, reactive, ref } from 'vue'
import { useAuthStore } from '@/stores/auth';
import AssignmentPanel from '@/components/AssignmentPanel.vue';
import AssignmentForm from '@/components/Form/AssignmentForm.vue';
import TaskPanel from '@/components/TaskPanel.vue';
import moment from "moment";
import router from '@/router';
import { useToast } from 'primevue/usetoast';

// stores
const route = useRoute();
const authStore = useAuthStore();
const toast = useToast();
let courseData = ref({});
const assignments = ref([])
// hooks
onBeforeMount(async () => {
    const courseCode = route.params.coursecode
    const config = {
        headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
        },
    };
    try {
        const response = await axios(API_URL + `/course/registered-course/${courseCode}`, config)
        courseData.value = response.data
        assignments.value = response.data.assignments
        console.log(courseData.value)
    }
    catch (error) {
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
    <div class="m-auto">
        <h1>{{ courseData.name + ' - ' + courseData.code }}</h1>
        <h2>Professor: {{ courseData.teacher?.first_name }} {{ courseData.teacher?.last_name }}</h2>
        <div class="mb-3">
            <h3>Schedule: </h3>
            <ul class="list-none mb-0 pl-3">
                <li v-for="(schedule, index) in courseData.schedules" :key="index" class="mb-2">
                    {{ schedule.week_day }}: {{ moment(schedule.start_time, "HH:mm:ss").format("HH:mm") }} - {{
                        moment(schedule.end_time, "HH:mm:ss").format("HH:mm") }}
                </li>
            </ul>
        </div>
        <h3>Assignments</h3>
        <div v-if="assignments.length > 0">
            <div class="card">
                <AssignmentPanel v-for="(assignment, index) in assignments" :key="index" :name="assignment.name"
                    :description="assignment.description" :deadline="assignment.due_date" :id="assignment.id" readOnly>
                    <TabView>
                        <TabPanel header="Description">
                           <div v-html="assignment.description"></div>
                        </TabPanel>
                        <TabPanel header="Tasks">
                           <div class="flex justify-content-end">
                            <Button class="mb-3">Add task</Button>
                           </div>
                            <TaskPanel v-for="(task, index) in assignment.tasks" :key="index" :name="task.title" :assignment_id="assignment.id" :description="task.description" :est_hour="task.est_hours">
                            <div v-html="task.description"></div>
                            </TaskPanel>
                        </TabPanel>
                    </TabView>
                </AssignmentPanel>
            </div>
    </div>
    <div v-else>
        <div class="card">
            <i>No assignments</i>
        </div>
    </div>
</div></template>
