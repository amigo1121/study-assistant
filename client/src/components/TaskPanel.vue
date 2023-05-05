<script lang="ts" setup>
import { defineProps, defineEmits, ref } from 'vue'
import { useConfirm } from 'primevue/useconfirm'
import { useToast } from 'primevue/usetoast'
import moment from 'moment'
import TaskForm from '@/components/Form/TaskForm.vue'

const props = defineProps({
    name: {
        type: String,
        required: true
    },
    description: {
        type: String,
        required: true
    },
    est_hour: {
        type: Number,
        required: true
    },
    assignment_id: {
        type: Number,
        required: true
    }
});
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
<style lang="scss" scoped></style>
<template>
    <Panel :header="props.name" toggleable collapsed>
        <template #icons>
            <button class="p-panel-header-icon p-link mr-2" @click="toggle">
                <span class="pi pi-cog"></span>
            </button>
            <Menu ref="menu" id="config_menu" :model="items" popup />
        </template>
        <slot></slot>
    </Panel>
</template>
