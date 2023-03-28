<script lang="ts">
import { defineComponent } from 'vue';
import MultiSelect from 'primevue/multiselect';
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import Dropdown from 'primevue/dropdown';
import Calendar from 'primevue/calendar';
import Button from 'primevue/button';
import TextEditor from '@/components/TextEditor.vue';
import { useTasksStore } from '@/stores/tasks';
export default defineComponent({
    components: { MultiSelect, InputText, InputNumber, Dropdown, Calendar, Button, TextEditor },

    props:{
        id:{
            type: String,
            required: false,
            default: null
        },
        title:{
            type: String,
            required: false,
            default: null
        },
        description:{
            type: String,
            required: false,
            default: ''
        },
        importance:{
            type: String,
            required: false,
            default: null
        },
        dueDate:{
            type: String,
            required: false,
            default: ''
        },
        dueTime:{
            type: String,
            required: false,
            default: ''
        },
        estHours:{
            type: Number,
            required: false,
            default: null
        },
        dependencies:{
            type: Array,
            required: false,
            default: []
        }
    },
    data(){
        return {
            taskStore: useTasksStore(),
            state: {
                title: this.title,
                description: this.description,
                importance: this.importance,
                dueDate: this.dueDate,
                dueTime: this.dueTime,
                estHours: this.estHours,
                dependencies: this.dependencies
            }

        }
    },
    methods: {
        handleSubmit(){
            this.$emit('add-task', this.state);
            this.reset();
        },
        handleCancel(){
            this.$emit('cancel');
        },
        reset(){
            this.state = {
                title: null,
                description: '',
                importance: null,
                dueDate: '',
                dueTime: '',
                estHours: null,
                dependencies: null
            }
        }
    },
    emits: ['add-task', 'cancel']
})
</script>
<style lang="scss" scoped></style>
<template>
    <h5>Task</h5>
    <div class="p-fluid formgrid grid">
        <div class="field col-12">
            <label for="name1">Title</label>
            <InputText id="name1" type="text" v-model="state.title" />
        </div>
        <div class="field col-12 h-auto">
            <label for="description">Description</label>
            <TextEditor v-model="state.description" />
        </div>
        <div class="field col-12 md:col-4">
            <label for="age1">Priority</label>
            <Dropdown v-model="state.importance" :options="['High', 'Medium', 'Low']" />
        </div>
        <div class="field col-12 md:col-4">
            <label for="date">Due date</label>
            <Calendar v-model="state.dueDate" dateFormat="yy-mm-dd" showButtonBar />
        </div>
        <div class="field col-12 md:col-4">
            <label for="date">Due Time</label>
            <Calendar v-model="state.dueTime" timeOnly />
        </div>
        <div class="field col-12 md:col-4">
            <label for="age1">Estimated Hours</label>
            <InputNumber v-model="state.estHours" />
        </div>
        <div class="field col-12 md:col-4">
            <label for="age1">Dependencies</label>
            <MultiSelect v-model="state.dependencies" :options="taskStore.tasks" optionLabel="title" optionValue="id" placeholder="Select dependencies"/>
        </div>
        <div class="col-12 flex justify-content-end gap-3">
            <Button class="w-auto p-button-danger" label="Cancel" @click="handleCancel"></Button>
            <Button class="w-auto p-button-info" label="Submit" @click="handleSubmit"></Button>
        </div>
    </div>
</template>