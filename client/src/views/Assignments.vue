<script lang="ts" setup>
import { reactive, defineProps, onBeforeMount, ref, nextTick } from 'vue'
import { useAuthStore } from '@/stores/auth';
import { API_URL } from '@/utils/config';
const authStore = useAuthStore()
import axios from 'axios'
// import AssignmentCard from '@/components/Card/AssignmentCard.vue';
import AssignmentPanel from '@/components/AssignmentPanel.vue';
import TaskPanel from '@/components/TaskPanel.vue';
const state = reactive({
    coursesSeach: ""
})
const props = defineProps<{}>()
const courses = ref([])
const assignments = ref([])

async function fetchData() {
    const config = {
        headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
        },
    };

    axios.get(API_URL + "/assignments/student", config).then(async (response) => {
        courses.value = response.data
        courses.value = courses.value.filter((enrollment)=>enrollment.course.assignments.length > 0)
    }).catch(error => {
        console.log(error)
    })

}

onBeforeMount(async () => {
    fetchData()
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

    <div class="card" v-for="(enrollment, index) in courses" :key="index">
        <h3>{{ enrollment.course.name }}</h3>
        <AssignmentPanel v-for="(assignment, index) in enrollment.course.assignments" :key="index" :name="assignment.name"
                :description="assignment.description" :deadline="assignment.due_date" :id="assignment.id" readOnly>
                <TabView>
                    <TabPanel header="Description">
                        <div v-html="assignment.description"></div>
                    </TabPanel>
                    <TabPanel header="Tasks">
                        <TaskPanel v-for="(task, index) in assignment.tasks" :key="index" :title="task.title" :id="task.id"
                            :assignment_id="assignment.id" :description="task.description" :est_hour="task.est_hours"
                            :readOnly="true" :status="task.status">
                            <div v-html="task.description"></div>
                        </TaskPanel>
                        <i v-if="assignment.tasks.length ===0">No task</i>
                    </TabPanel>
                </TabView>
            </AssignmentPanel>
    </div>

</template>
