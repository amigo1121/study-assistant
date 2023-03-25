<script setup lang="ts">
import Formbase from './Formbase.vue';
import { ref } from 'vue';

type State = {
    title: string;
    description: string;
    dueDate: Date;
    dueTime: string;
    importance: string;
};
const state = ref<State>({
    title: '',
    description: '',
    dueDate: '',
    dueTime: '',
    importance: '',
});
const addAssigment = () => {
    console.log(state.value);
    resetForm();
}
const resetForm = () => {
    state.value.title = '';
    state.value.description = '';
    state.value.dueDate = '';
    state.value.dueTime = '';
    state.value.importance = '';
}
</script>
<style lang="scss" scoped>
.form-group {
    margin-bottom: 1rem;
}

.column {
    display: flex;
    flex-direction: column;
}
</style>
<template>
    <Formbase>
        <form @submit.prevent="addAssigment">
            <div class="form-group">
                <label for="title">Title</label>
                <input type="text" id="title" v-model="state.title" />
            </div>
            <div class="form-group column">
                <label for="description">Description</label>
                <textarea id="description" v-model="state.description"></textarea>
            </div>
            <div class="form-group">
                <label for="dueDate">Due Date</label>
                <input type="date" id="dueDate" v-model="state.dueDate" />
                <input type="time" id="dueTime" v-model="state.dueTime" />
            </div>
            <div class="form-group">
                <label for="importance">Importance</label>
                <select id="importance" v-model="state.importance">
                    <option value="" disabled>Choose importance</option>
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                </select>
            </div>
            <div class="form-group">
                <button type="submit">Add Assignment</button>
            </div>
        </form>
    </Formbase>
</template>