<script lang="ts" setup>
import { defineProps, defineEmits, ref } from 'vue'
import { useConfirm } from 'primevue/useconfirm'
import { useToast } from 'primevue/usetoast'
import moment from 'moment'
import TaskForm from '@/components/Form/TaskForm.vue'
const menu=ref(null)
const confirm = useConfirm()
const toast = useToast()
const emit = defineEmits(['delete', 'update'])
const props = defineProps({
    title: {
        type: String,
        required: true
    },
    description: {
        type: String,
        required: false,
        default: ""
    },
    est_hour: {
        type: Number,
        required: true
    },
    assignment_id: {
        type: Number,
        required: true
    },
    id: {
        type: Number,
        required: true,
    },
    readOnly: {
        type: Boolean,
        default: false
    }

});

const confirmDelete = (event) => {
    confirm.require({
        target: event.currentTarget,
        message: 'Do you want to delete this task?',
        icon: 'pi pi-info-circle',
        acceptClass: 'p-button-danger',
        accept: () => {
            emit('delete', props.id, props.assignment_id)
        },
        reject: () => {
            toast.add({ severity: 'error', summary: 'Rejected', detail: 'You have rejected', life: 3000 });
        }
    });
};

const items = ref([
    {
        label: 'Options',
        items: [
            {
                label: 'Update',
                icon: 'pi pi-refresh',
                command: () => {
                    emit("update",props.id, props.assignment_id)
                }
            },
            {
                label: 'Delete',
                icon: 'pi pi-times',
                command: () => {
                    confirmDelete(event)
                }
            }
        ]
    }
]);

const toggle = () =>{
    menu.value.toggle(event);
}

</script>
<style lang="scss" scoped></style>
<template>
    <Panel :header="props.title" toggleable collapsed>
        <template #icons v-if="!props.readOnly">
            <button class="p-panel-header-icon p-link mr-2" @click="toggle">
                <span class="pi pi-cog"></span>
            </button>
            <Menu ref="menu" id="config_menu" :model="items" popup />
        </template>
        <slot></slot>
    </Panel>
</template>
