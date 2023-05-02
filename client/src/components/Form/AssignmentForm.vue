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
            type: Number,
            required: false,
            default: null,
        },
        name: {
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
                name: data.name,
                description: data.description,
                dueDate: data.dueDate? moment(data.dueDate).toDate():null,
            },
            errorMsg:[]
        }
    },
    methods: {
        handleCancel() {
            this.$emit('close');
        },
        handleSubmit() {
            const {dueDate,...restData} =this.state
            const dueDateFormated = moment(dueDate).format()
            this.validateInput()
            if(this.errorMsg.length > 0)
                return;
            this.$emit('addAssignment',{due_date:dueDateFormated,...restData});
            this.$emit('modifyAssignment',{id: this.id ,due_date:dueDateFormated,...restData});
            this.$emit('close');
            this.reset();
        },
        reset(){
            this.state = {
                name: '',
                description: '',
                dueDate: null,
            }
        },
        validateInput(){
            this.errorMsg=[]
            if(this.state.name==="")
                this.errorMsg.push("Assignment name is empty")
            if(this.state.description==="")
                this.errorMsg.push("Assignment description is empty")
            if(!moment(this.state.dueDate).isValid())
                this.errorMsg.push("Assignment due date is invalid")
        }
    },
    emits : ['close','addAssignment','modifyAssignment']
}
</script>
<template>
    <h5>Assignment</h5>
    <div class="p-fluid formgrid grid">
        <div class="field col-12">
            <label for="name1">Name</label>
            <InputText id="name1" type="text" v-model="state.name" />
        </div>
        <div class="field col-12 h-auto">
            <label for="description">Description</label>
            <TextEditor v-model="state.description" class="z-5"/>
        </div>
        <div class="field col-12">
            <label for="date">Due date</label>
            <Calendar v-model="state.dueDate" showButtonBar showTime hourFormat="24" />
        </div>
        <div class="field col-12" v-if="errorMsg.length > 0">
            <InlineMessage v-for="(msg, index) in errorMsg" :key="index" severity="error">{{msg}}</InlineMessage>
        </div>
        <div class="col flex justify-content-end gap-3">
            <Button class="w-auto p-button-danger" label="Cancel" @click="handleCancel"></Button>
            <Button class="w-auto p-button-info" label="Submit" @click="handleSubmit"></Button>
        </div>
    </div>
</template>
