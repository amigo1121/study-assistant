<script setup lang="ts">
import FormTask from '@/components/Form/FormTask.vue';
import BaseCard from '@/components/Card/BaseCard.vue';
import AssigmentCard from '@/components/Card/AssigmentCard.vue';
import BaseDialog from '@/components/Dialog/BaseDialog.vue';
import TextEditor from '@/components/TextEditor.vue';
import AssignmentForm from '@/components/Form/AssignmentForm.vue';
import { useAssignmentsStore } from '@/stores/assignments';
import { storeToRefs } from 'pinia';
import {ref} from 'vue';


const store = useAssignmentsStore();
const assignments  = store.assignments;

const handleSubmit = (assignment) => {
    store.addAssignment(assignment);
}
const temp = ref('<h1>dit is een test</h1>');
</script>
<style lang="scss" scoped>
    li {
        list-style: none;
        margin-bottom: 1rem;
    }
</style>
<template>
    <div class="todos">

        <FormTask></FormTask>
        <ul>
            <li v-for="assignment in assignments" :key="assignment.title">
                <AssigmentCard v-bind="assignment" />
            </li>
        </ul>

        <div class="card">
            <AssignmentForm @add-assignment="handleSubmit"></AssignmentForm>
        </div> 
    
    </div>
</template>