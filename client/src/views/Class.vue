<script lang="ts" setup>
import { API_URL } from '@/utils/config';
import axios from 'axios'
import { useRoute } from 'vue-router'
import { onBeforeMount, reactive, ref } from 'vue'
import { useAuthStore } from '@/stores/auth';
import AssignmentPanel from '@/components/AssignmentPanel.vue';
import AssignmentForm from '@/components/Form/AssignmentForm.vue';
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
        const response = await axios(API_URL + `/course/code/${courseCode}`, config)
        courseData.value = response.data
        assignments.value = response.data.assignments
        console.log(courseData.value)
    }
    catch (error) {
        console.log(error)
    }

})
const isOpened = ref(false)

const toggleDialog = () => {
    isOpened.value = !isOpened.value
}
const menuItems = ref([
    {
        label: 'Options',
        items: [
            {
                label: 'Update',
                icon: 'pi pi-refresh',
                command: () => {
                    toast.add({ severity: 'success', summary: 'Updated', detail: 'Data Updated', life: 3000 });
                }
            },
            {
                label: 'Delete',
                icon: 'pi pi-times',
                command: () => {
                    toast.add({ severity: 'warn', summary: 'Delete', detail: 'Data Deleted', life: 3000 });
                }
            }
        ]
    }
])

const addAssignment = (data) => {
    data.course_code = courseData.value.code
    const config = {
        headers: {
            Authorization: `Bearer ${authStore.getAccessToken}`,
        },
    };
    axios.post(API_URL + "/assignments", data, config).then((response) => {
        router.go();
        console.log(response.data)
        toast.add({ severity: 'success', summary: "Success", detail: "Add assignment success", life: 3000 })
    }).catch((error) => {
        console.log(error)
        toast.add({ severity: 'error', summary: "Error", detail: "Add assignment failed", life: 3000 })
    })
}

const deleteAssignment = (id: number) => {

    const config = {
        headers: {
            Authorization: `Bearer ${authStore.getAccessToken}`,
        },
    };

    axios.delete(API_URL + "/assignments/" + id,config).then((response)=>{
        router.go()
        console.log(response.data)
        toast.add({ severity: 'success', summary: "Success", detail: "Delete assignment success", life: 3000 })
    }).catch((error) => {
        console.log(error)
        toast.add({ severity: 'error', summary: "Error", detail: "Delete assignment failed", life: 3000 })
    })

}
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
        <h1>{{ courseData.name }}</h1>
        <div class="flex gap-3">
            <h3>Schedule: </h3>
            <ul class="list-none mt-0 ">
                <li v-for="(schedule, index) in courseData.schedules" :key="index" class="mb-2">
                    {{ schedule.week_day }}: {{ moment(schedule.start_time, "HH:mm:ss").format("HH:mm") }} - {{
                        moment(schedule.end_time, "HH:mm:ss").format("HH:mm") }}
                </li>
            </ul>
        </div>
        <div class="flex justify-content-between">
            <h3>Assignments</h3>
            <Button label="Add assignment" @click="toggleDialog"></Button>
        </div>
        <div v-if="assignments.length > 0">
            <div class="card">
                <AssignmentPanel v-for="(assignment, index) in assignments" :key="index" :name="assignment.name"
                    :description="assignment.description" :deadline="assignment.due_date" :id="assignment.id"
                    @delete="deleteAssignment">
                </AssignmentPanel>
            </div>
        </div>
        <div v-else>
            <div class="card">
                <i>No assignments</i>
            </div>
        </div>
        <Dialog v-model:visible="isOpened" modal :style="{ width: '50rem' }" header="Add assignment">
            <AssignmentForm @close="toggleDialog" @addAssignment="addAssignment"></AssignmentForm>
        </Dialog>

    </div>
</template>
