<script lang="ts">
import BaseDialog from './BaseDialog.vue';
import { defineComponent } from 'vue';
import AssignmentModifyForm from '../Form/AssignmentModifyForm.vue';

export default defineComponent({
    name: 'AssigmentModifyDialog',
    components: {
        BaseDialog,
        AssignmentModifyForm
    }

})
</script>
<template>
    <BaseDialog>
        <AssignmentModifyForm></AssignmentModifyForm>
    </BaseDialog>
</template>