<script lang="ts" setup>
import { defineProps, withDefaults, ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import { API_URL } from "@/utils/config";
import axios from 'axios'
import { useToast } from 'primevue/usetoast';
import router from "@/router";
const toast = useToast();
const authStore = useAuthStore();
const openCreateNewAssignment = ref(false);
const openCourseActions = ref(false);
interface Props {
    name?: String
    code: String
    schedules: Array<Object>
    teacher?: String
    credits: Number
    details?: Boolean
    startDate: String
    endDate: String
}
const props = withDefaults(defineProps<Props>(), {
    name: "default",
    details: false
})

const createNewAssignment = () => {
    openCreateNewAssignment.value = true;
}
const registerOrLeaveCourse = () => {
    openCourseActions.value = true;
}
const handleRegister = async () => {

    if (confirm("Confirm course registration")) {
        try {

            let config = {
                headers: {
                    Authorization: `Bearer ${authStore.accessToken}`,
                },
            };
            const response = await axios.post(API_URL + "/course-action/register-course",{course_code: props.code}, config)

            if (response.status !== 200)
                throw new Error("Something wrong, cannot register for course")

            toast.add({ severity: 'success', summary: "Success", detail: 'Course register sucess', life: 2000 })
        }
        catch (error) {
            console.log(error)
            toast.add({ severity: 'error', summary: "Error", detail: 'Failed to register', life: 2000 })
        }
    }

}
const handleDrop = async () =>{
    if (confirm("Confirm course deregistration")) {
        try {

            let config = {
                headers: {
                    Authorization: `Bearer ${authStore.accessToken}`,
                },
            };
            const response = await axios.post(API_URL + "/course-action/drop-course",{course_code: props.code}, config)

            if (response.status !== 200)
                throw new Error("Something wrong, cannot deregister for course")

            toast.add({ severity: 'success', summary: "Success", detail: 'Course deregister sucess', life: 2000 })
            router.go()
        }
        catch (error) {
            console.log(error)
            toast.add({ severity: 'error', summary: "Error", detail: 'Failed to deregister', life: 2000 })
        }
    }
}
const handleClick = () => {
    if (authStore.type == 2)
        createNewAssignment()
    else
        registerOrLeaveCourse()
}
</script>
<style lang="scss" scoped></style>
<template>
    <div class="card border-round-3xl" @click="handleClick">
        <h3>Course name: {{ props.name }}</h3>
        <h4>Course code: {{ props.code }}</h4>
        <template v-if="details && props.schedules.length > 0">
            <h4>Schedue: </h4>
            <ul class="list-none">
                <li v-for="(value, key) in props.schedules" :key="key">
                    {{ value.day.toString().toUpperCase() }}: {{ value.start }} - {{ value.end }}
                </li>
            </ul>
            <h4>Start date: {{ props.startDate }}</h4>
            <h4>End date: {{ props.endDate }}</h4>
        </template>
        <h4 v-if="!!props.teacher">
            Teacher: {{ props.teacher }}
        </h4>
        <h4>
            Credit: {{ props.credits }}
        </h4>
        <div class="flex gap-3" v-if="authStore.type == 1">
            <Button label="Register" severity="info" @click="handleRegister" />
            <Button label="Drop" severity="danger"  @click="handleDrop"/>
        </div>
    </div>

    <Dialog v-model:visible="openCreateNewAssignment" modal :style="{ width: '40rem' }" header="Create new Assignment">

    </Dialog>
</template>
