<script setup lang="ts">
import FormAssignment from '@/components/Form/FormAssignment.vue';
import FormTask from '@/components/Form/FormTask.vue';
import BaseCard from '@/components/Card/BaseCard.vue';
import AssigmentCard from '@/components/Card/AssigmentCard.vue';
import BaseDialog from '@/components/Dialog/BaseDialog.vue';


const assignments = [
  {
    title: 'Assignment 1',
    description: 'Lorem ipsum dolor sit amet',
    dueDate: new Date('2023-04-01'),
    dueTime: '23:59',
    importance: 'High',
  },
  {
    title: 'Assignment 2',
    description: 'Consectetur adipiscing elit',
    dueDate: new Date('2023-04-15'),
    dueTime: '18:00',
    importance: 'Medium',
  },
  {
    title: 'Assignment 3',
    description: 'Sed do eiusmod tempor incididunt',
    dueDate: new Date('2023-04-30'),
    dueTime: '09:00',
    importance: 'Low',
  },
];

</script>
<style lang="scss" scoped>
    li {
        list-style: none;
        margin-bottom: 1rem;
    }
</style>
<template>
    <div class="todos">
        <FormAssignment></FormAssignment>

        <FormTask></FormTask>
        <ul>
            <li v-for="assignment in assignments" :key="assignment.title">
                <AssigmentCard v-bind="assignment" />
            </li>
        </ul>
    </div>
</template>