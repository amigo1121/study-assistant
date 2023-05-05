<script lang="ts" setup>
import { defineEmits, defineProps, ref, inject, onMounted } from 'vue';
import MultiSelect from 'primevue/multiselect';
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import Dropdown from 'primevue/dropdown';
import Calendar from 'primevue/calendar';
import Button from 'primevue/button';
import TextEditor from '@/components/TextEditor.vue';
const emit = defineEmits(['create','cancle','change'])
const dialogRef = inject('dialogRef')
const options = ref([])
const statusOptions = ref([
    {label: "Not Started", value: "NOT_STARTED"},
    {label: "In Progress", value: "IN_PROGRESS"},
    {label: "Complete", value: "COMPLETE"}

])

const priorityOptions = ref([
    {label: "Low", value: "LOW"},
    {label: "Medium", value: "MEDIUM"},
    {label: "High", value: "HIGH"},
])
const props = defineProps({
    id: {
        type: String,
        required: false,
        default: null
    },
    title: {
        type: String,
        required: false,
        default: null
    },
    description: {
        type: String,
        required: false,
        default: ''
    },
    priority: {
        type: String,
        required: false,
        default: null
    },
    est_hours: {
        type: Number,
        required: false,
        default: null
    },
    dependencies: {
        type: Array,
        required: false,
        default: []
    },
    status: {
        type: String,
        required: false,
        default: "Not started"
    }
})

const state = ref({
    title: props.title,
    description: props.description,
    priority: props.priority,
    est_hours: props.est_hours,
    dependencies: props.dependencies,
});

const handleSubmit = () => {
    emit('create', state.value);
    reset();
};

const handleCancel = () => {
    emit('cancel');
};

const handleModify = () => {
    emit('change', state.value);
    reset();
};

const reset = () => {
    state.value = {
        title: null,
        description: '',
        priority: null,
        est_hours: null,
        dependencies: null,
    };
};

onMounted(()=>{
    options.value = dialogRef.value.data.options
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
        <div class="field col-12 md:col-6">
            <label for="age1">Priority</label>
            <Dropdown v-model="state.priority" :options="priorityOptions"  optionLabel="label" optionValue="value" />
        </div>
        <div class="field col-12 md:col-6">
            <label for="age1">Estimated Hours</label>
            <InputNumber v-model="state.est_hours" inputId="integeronly" :min="0" />
        </div>
        <div class="field col-12 md:col-6">
            <label for="age1">Dependencies</label>
            <MultiSelect v-model="state.dependencies" :options="options" optionLabel="title" optionValue="id"
                placeholder="Select dependencies" />
        </div>
        <div class="field col-12 md:col-6">
            <label>Status</label>
            <Dropdown v-model="state.status" :options="statusOptions" optionLabel="label" optionValue="value"/>
        </div>
        <div class="col-12 flex justify-content-end gap-3">
            <Button class="w-auto p-button-danger" label="Cancel" @click="handleCancel"></Button>
            <Button class="w-auto p-button-info" label="Submit" @click="handleSubmit"></Button>
        </div>
    </div>
</template>
