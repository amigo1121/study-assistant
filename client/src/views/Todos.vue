<script setup lang="ts">
import FormTask from '@/components/Form/FormTask.vue';
import BaseCard from '@/components/Card/BaseCard.vue';
import AssigmentCard from '@/components/Card/AssignmentCard.vue';
import TaskCard from '@/components/Card/TaskCard.vue'
import BaseDialog from '@/components/Dialog/BaseDialog.vue';
import TextEditor from '@/components/TextEditor.vue';
import AssignmentForm from '@/components/Form/AssignmentForm.vue';
import TaskForm from '@/components/Form/TaskForm.vue';
import { useAssignmentsStore } from '@/stores/assignments';
import { useTasksStore } from '@/stores/tasks';
import { storeToRefs } from 'pinia';
import {ref} from 'vue';


const store = useAssignmentsStore();
const assignments  = store.assignments;
const taskStore = useTasksStore();
const {tasks} = storeToRefs(taskStore);

const handleSubmit = (assignment) => {
    store.addAssignment(assignment);
}

const addTask = (task) => {
    taskStore.addTask(task);
}

</script>
<style lang="scss" scoped>
    li {
        list-style: none;
        margin-bottom: 1rem;
    }
</style>
<template>
    <div class="todos">
        <!-- <FormTask></FormTask> -->
        <ul>
            <li v-for="task in tasks" :key="task.id">
                <TaskCard v-bind="task">
                </TaskCard>
            </li>
        </ul>
    </div>
</template>