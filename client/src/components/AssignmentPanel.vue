<script lang="ts" setup>
import axios from 'axios'
import router from '@/router';
import moment from 'moment'
import { ref } from 'vue'
import { useToast } from "primevue/usetoast";
import { useConfirm } from "primevue/useconfirm";
import AssignmentForm from '@/components/Form/AssignmentForm.vue';
import { API_URL } from '@/utils/config';
import { useAuthStore } from '@/stores/auth';
const props = defineProps(['name', 'description', 'deadline', 'id'])
const emit = defineEmits(['delete', 'update'])
const menu = ref(null);
const toast = useToast();
const confirm = useConfirm();
const authStore = useAuthStore();
const toggle = (event) => {
    menu.value.toggle(event);
};
const isOpened = ref(false)

const toggleDialog = () => {
    isOpened.value = !isOpened.value
}

const updateAssignment = (data) => {
    emit('update',data)
}

const confirmDelete = (event) => {
    confirm.require({
        target: event.currentTarget,
        message: 'Do you want to delete this Assignment?',
        icon: 'pi pi-info-circle',
        acceptClass: 'p-button-danger',
        accept: () => {
            emit('delete', props.id)
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
                    toggleDialog()

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
</script>
<style lang="scss "> </style>
<template>
    <Panel :header="props.name + ' - Due date: ' + moment(props.deadline).format('YYYY-MM-DD HH:mm')" toggleable collapsed>
        <template #icons>
            <button class="p-panel-header-icon p-link mr-2" @click="toggle">
                <span class="pi pi-cog"></span>
            </button>
            <Menu ref="menu" id="config_menu" :model="items" popup />
        </template>
        <slot></slot>
    </Panel>
    <Dialog v-model:visible="isOpened" modal :style="{ width: '50rem' }" header="Update assignment">
        <AssignmentForm @close="toggleDialog" @modifyAssignment="updateAssignment" :id="props.id" :name="props.name"
        :description="props.description"
        :dueDate="props.deadline"
        ></AssignmentForm>
    </Dialog>
</template>
