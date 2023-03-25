<template>
    <BaseCard @click="openDialogHandler">
        <div class="assignment-card">
            <h2>{{ props.title }}</h2>
            <p>{{ props.importance }}</p>
        </div>
    </BaseCard>

    <AssigmentModifyDialog v-if="openDialog" @close="closeDialogHandler" v-bind="props"></AssigmentModifyDialog>
</template>
  
<script lang="ts" setup>
import BaseCard from '@/components/Card/BaseCard.vue';
import BaseDialog from '@/components/Dialog/BaseDialog.vue';
import AssigmentModifyDialog from '@/components/Dialog/AssigmentModifyDialog.vue';
import { ref } from 'vue';

type AssignmentCardProps = {
    title: string;
    description: string;
    dueDate: Date;
    dueTime: string;
    importance: string;
};

const props = defineProps<AssignmentCardProps>();

const openDialog = ref(false);

const openDialogHandler = () => {
    openDialog.value = true;
};

const closeDialogHandler = () => {
    openDialog.value = false;
};

</script>
  
<style scoped>
    .assignment-card {
       display: inline-block;
       width: 400px;
       padding: 1rem;
    }
</style>
  