<script lang="ts" setup>
import Formbase from './Formbase.vue';
import { ref } from 'vue';

type Task = {
    taskName: string;
    taskDescription: string;
    taskDeadline: string;
    taskDependedsOn: string;
    taskDependencies: string[];
    taskEstimatedTime: number;
};
const state = ref({
    taskName: '',
    taskDescription: '',
    taskDeadline: '',
    taskDependedsOn: '',
    taskDependencies: [],
    taskEstimatedTime: null,
});

const addTaskDependencies = () => {
    state.value.taskDependencies.push(state.value.taskDependedsOn);
    state.value.taskDependedsOn = '';
};

const addTask = () => {
    console.log(state.value);
    resetForm();
};

const resetForm = () => {
    state.value.taskName = '';
    state.value.taskDescription = '';
    state.value.taskDeadline = '';
    state.value.taskDependedsOn = '';
    state.value.taskDependencies = [];
    state.value.taskAssignments = '';
    state.value.taskEstimatedTime = null;
}

</script>
<style lang="scss" scoped>
.form-task {
    display: block;
    background-color: #fff;
    border-radius: 0.5rem;
    box-shadow: 0 0 0.5rem rgba(0, 0, 0, 0.2);
}

.form-group {
    margin-bottom: 1rem;
}
</style>
<template>
    <Formbase>
        <form @submit.prevent="addTask">
            <div class="form-group">
                <label for="taskName">Task Name</label>
                <input type="text" id="taskName" v-model="state.taskName" @keydown.enter.prevent />
            </div>

            <div class="form-group">
                <label for="taskDescription">Task Description</label>
                <textarea id="taskDescription" v-model="state.taskDescription"></textarea>
            </div>

            <div class="form-group">
                <label for="taskEstimatedTime">Task Estimated Time</label>
                <input type="number" id="taskEstimatedTime" v-model="state.taskEstimatedTime" @keydown.enter.prevent min="0" />
            </div>
            <div class="form-group">
                <label for="taskDeadline">Task Deadline</label>
                <input type="datetime-local" id="taskDeadline" v-model="state.taskDeadline" @keydown.enter.prevent/>
            </div>

            <div class="form-group">
                <label for="taskAssignments">Task Assignments</label>
                <input type="text" id="taskAssignments" v-model="state.taskAssignments" @keydown.enter.prevent/>
            </div>

            <div class="form-group">
                <label for="taskDependsOn">Task Depends On</label>
                <input type="text" id="taskDependsOn" v-model="state.taskDependedsOn" @keydown.enter.prevent />
                <button type="button" @click="addTaskDependencies">Add Task Dependency</button>
                <div v-if="state.taskDependencies.length > 0">
                    <h3>Depens on:</h3>
                    <ul>
                        <li v-for="task in state.taskDependencies" :key="task.id">
                            {{ task }}
                        </li>
                    </ul>
                </div>
            </div>

            <button type="submit">Add Task</button>
            <button type="button" @click="resetForm">Reset Form</button>
        </form>
    </Formbase>
</template>