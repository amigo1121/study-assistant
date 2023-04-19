<script lang="ts" setup>
import DashboardSidebar from '@/layouts/DashboardSidebar.vue';
import {ref} from 'vue';
const sidebarItems=ref([
    {
        // Statistic of Assignments, Tasks, etc
        label: 'Overview',
    },
    {
        // Calendar of events, classes
        label: 'Calendar'
    },
    {
        // Show a list of task that need to do today
        label: 'My day'
    },
    {
        // List of assignments, create new, etc
        label: 'Assignment'
    },
    {
        // list of classes, crud
        label: 'Classes'
    },
    {
        // List of groups
        label: 'Groups'
    }
]);
</script>
<style lang="scss" scoped>
.dashboard {
    width: 100%;
    height: 100%;
}

.task-list, .assignment-list {
    height: 50vh;
    overflow-y: auto;
}
.dashboard{
    display: flex;
    gap: 1rem;

    .dashboard__sidebar{
        height: 100vh;
        max-width: 20rem;
        padding: 1rem;
    }

    .dashboard__content{

    }
}

</style>
<template>
    <div class="dashboard">
        <div class="dashboard__sidebar bg-primary">
            <DashboardSidebar :model="sidebarItems"/>
        </div>
        <div class="dashboard__content">
            <router-view></router-view>
        </div>
    </div>
</template>
