<script setup lang="ts">
import {ref, onMounted} from 'vue';
import { useTasksStore } from '@/stores/tasks';
import Diagram from '@/components/Diagram.vue'
const tasks = ref([]);

onMounted(()=>{
   const taskStore = useTasksStore()
   tasks.value = taskStore.tasks
})



</script>
<style></style>
<template>

    <div class="grid">
       <div class="col-4">
        <div class="card">
            <h5>On going</h5>
        </div>
       </div>

       <div class="col-4">
        <div class="card">
            <h5>In Progress</h5>
        </div>
       </div>

       <div class="col-4">
        <div class="card">
            <h5>Not Started</h5>
        </div>
       </div>

        <div class="col-6">
            <div class="card">
                <h5>Tasks</h5>
                <DataTable :value="tasks" :rows="5" :paginator="true" responsiveLayout="scroll">
                    <Column field="id" header="Task ID" :sortable="true"></Column>
                    <Column field="title" header="Title" :sortable="true"></Column>
                    <Column field="dueDate" header="Due date" :sortable="true"></Column>
                    <Column field="hours" header="Est. Hours" :sortable="true"></Column>
                    <Column field="priority" header="Priority" :sortable="true"></Column>
                </DataTable>
            </div>
        </div>
        <div class="col-6">
            <div class="card">
                <h5>Assignments</h5>
                <DataTable :value="tasks" :rows="5" :paginator="true" responsiveLayout="scroll">
                    <Column field="id" header="Task ID" :sortable="true"></Column>
                    <Column field="title" header="Title" :sortable="true"></Column>
                    <Column field="dueDate" header="Due date" :sortable="true"></Column>
                    <Column field="hours" header="Est. Hours" :sortable="true"></Column>
                    <Column field="priority" header="Priority" :sortable="true"></Column>
                </DataTable>
            </div>
        </div>

        <div class="col-6">
            <div class="card">
                <h5>Tasks by priority</h5>
                <Diagram :data="[10,50,40]"/>
            </div>
        </div>
        <div class="col-6">
            <div class="card">
                <h5>Assignments by priority</h5>
                <Diagram :data="[10,50,40]"/>
            </div>
        </div>
    </div>
</template>
