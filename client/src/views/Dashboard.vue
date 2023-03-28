<script lang="ts" setup>
import List from '@/components/List.vue';
import { useTasksStore } from '@/stores/tasks';
import { useAssignmentsStore } from '@/stores/assignments';
import TaskCard from '@/components/Card/TaskCard.vue';
import AssignmentCard from '@/components/Card/AssignmentCard.vue';
import TaskForm from '@/components/Form/TaskForm.vue';
import AssignmentForm from '@/components/Form/AssignmentForm.vue';
import { storeToRefs } from 'pinia';
const taskStore = useTasksStore();
const { tasks } = storeToRefs(taskStore);
const assignmentStore = useAssignmentsStore();
const { assignments } = storeToRefs(assignmentStore);

const addAssignment = (assignment) => {
    assignmentStore.addAssignment(assignment);
}

const addTask = (task) => {
    taskStore.addTask(task);
}


</script>
<style lang="scss" scoped>
.dashboard {
    width: 100%;
    height: 100%;
}

.task-list, .assignment-list {
    height: 50vh;
    overflow-y: auto;
}
</style>
<template>
    <div class="dashboard p-fluid formgrid grid">
        <div class="task-list card col-6">
            <ul>
                <li v-for="task in tasks" :key="task.id" class="mb-3">
                    <TaskCard v-bind="task">
                    </TaskCard>
                </li>
            </ul>
        </div>

        <div class="assignment-list card col-6">
            <ul>
                <li v-for="assignment in assignments" :key="assignment.id" class="mb-3">
                    <AssignmentCard v-bind="assignment">
                    </AssignmentCard>
                </li>
            </ul>
        </div>
        <div class="card field col-6 p-3">
            <TaskForm @add-task="addTask"></TaskForm>
        </div>
        <div class="card field col-6 p-3">
            <AssignmentForm @add-assignment="addAssignment"></AssignmentForm>
        </div>
    </div>
</template>