<script lang="ts">
import TextEditor from '../TextEditor.vue';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import Calendar from 'primevue/calendar';
import Button from 'primevue/button';
import Editor from 'primevue/editor';
import moment from 'moment';
export default {
    components: { TextEditor, InputText, Dropdown, Calendar, Button },
    props: {
        id: {
            type: String,
            required: false,
            default: '',
        },
        title: {
            type: String,
            required: false,
            default: '',
        },
        priority: {
            type: String,
            required: false,
            default: '',
        },
        description: {
            type: String,
            required: false,
            default: '',
        },
        dueDate: {
            type: String,
            required: false,
            default: null,
        }
    },
    data() {
        const {id,...data} = this.$props;
        return {
            state:{
                title: data.title,
                priority: data.priority,
                description: data.description,
                dueDate: data.dueDate? data.dueDate:null,
            }
        }
    },
    methods: {
        handleCancel() {
            this.$emit('close');
        },
        handleSubmit() {
            const {dueDate,...restData} =this.state
            const dueDateFormated = moment(dueDate).format()
            this.$emit('addAssignment',{due_date:dueDateFormated,...restData});
            this.$emit('modifyAssignment',{id: this.id ,...this.state});
            this.$emit('close');
            this.reset();
        },
        reset(){
            this.state = {
                title: '',
                priority: '',
                description: '',
                dueDate: null,
            }
        }
    },
    emits : ['close','addAssignment','modifyAssignment']
}
</script>
<template>
    <h5>Assignment</h5>
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
            <Dropdown v-model="state.priority" :options="['High', 'Medium', 'Low']" />
        </div>
        <div class="field col-12 md:col-8">
            <label for="date">Due date</label>
            <Calendar v-model="state.dueDate" showButtonBar showTime hourFormat="24" />
        </div>
        <div class="col flex justify-content-end gap-3">
            <Button class="w-auto p-button-danger" label="Cancel" @click="handleCancel"></Button>
            <Button class="w-auto p-button-info" label="Submit" @click="handleSubmit"></Button>
        </div>
    </div>
</template>
