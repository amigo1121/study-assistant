<script lang="ts">
import BaseCard from '@/components/Card/BaseCard.vue';
import BaseDialog from '@/components/Dialog/BaseDialog.vue';
import AssigmentModifyDialog from '@/components/Dialog/AssigmentModifyDialog.vue';
import AssignmentForm from '@/components/Form/AssignmentForm.vue';
import TextEditor from '@/components/TextEditor.vue';
import Dialog from 'primevue/dialog';
import { ref, defineComponent } from 'vue';
// import { Assignment } from '@/stores/assignments.ts'
import { useAssignmentsStore } from '@/stores/assignments';
import { formatDate, formatTime } from '@/utils/datetime';
const assignmentStore = useAssignmentsStore();
export default defineComponent({
    name: 'AssignmentCard',
    components: {
        BaseCard,
        BaseDialog,
        AssigmentModifyDialog,
        Dialog,
        AssignmentForm,
        TextEditor
    },
    props: {
        id: Number,
        title: String,
        importance: String,
        description: String,
        dueDate: String,
    },
    data() {
        return {
            openDialog: false
        }
    },
    methods: {
        openDialogHandler() {
            this.openDialog = true;
        },
        closeDialogHandler() {
            this.openDialog = false;
        },
        updateAssignment(assignment) {
            let {id, title , importance, description, dueDate, dueTime} = assignment;
            assignment.dueDate= formatDate(dueDate);
            assignment.dueTime= formatTime(dueTime);
            console.log(assignment)
            assignmentStore.modifyAssignment(assignment.id, assignment);
        }
    },
})
</script>

<style scoped></style>

<template>
    <BaseCard @click="openDialogHandler">
        <div>
            <h2>{{ title }}</h2>
            <div class="bg-yellow-100 border-round-xl p-3">
                <h4>Description:</h4>
                <div v-html="description"></div>
            </div>
            <p>Priority: {{ importance }}</p>
            <p>Due date: {{ dueDate }}</p>
        </div>

    </BaseCard>

    <!-- <AssigmentModifyDialog v-if="openDialog" @close="closeDialogHandler"></AssigmentModifyDialog> -->

    <Dialog v-model:visible="openDialog" modal :style="{ width: '50vw' }" header="Header">
        <AssignmentForm @close="closeDialogHandler" @modify-assignment="updateAssignment" v-bind="this.$props">
        </AssignmentForm>
    </Dialog>
</template>
