<script lang="ts" setup>
import { useAuthStore } from "@/stores/auth";
import { API_URL } from "@/utils/config";
import { onMounted, ref, computed, onBeforeMount, nextTick } from "vue";
import { TaskPriorityTree } from "@/utils/TaskPriorityTree";
import TaskPanel from "@/components/TaskPanel.vue";
import axios from "axios";
import moment from "moment";

const authStore = useAuthStore();
const assignments = ref([]);
const inProgressTasks = ref([]);
const completeTasks = ref([]);
const pendingTasks = ref([]);

async function fetchData() {
  const config = {
    headers: {
      Authorization: `Bearer ${authStore.getAccessToken}`,
    },
  };
  await axios
    .get(API_URL + "/task/user/assignment", config)
    .then((response) => {
      assignments.value = response.data;
      assignments.value.forEach((assignment) => {
        inProgressTasks.value = inProgressTasks.value.concat(
          assignment.tasks.filter((t) => t.status === "IN_PROGRESS")
        );
        completeTasks.value = completeTasks.value.concat(
          assignment.tasks.filter((t) => t.status === "COMPLETE")
        );
        assignment.tasks = assignment.tasks.filter(
          (t) => t.status === "NOT_STARTED"
        );
        assignment.remained_time = assignemntRemainTime(assignment);
      });

      assignments.value.sort((a, b) => a.remained_time - b.remained_time);
      assignments.value.forEach((assignment) => {
        if (assignment.tasks.length > 0)
          pendingTasks.value = pendingTasks.value.concat(assignment.tasks);
      });
      console.log(assignments.value);
    })
    .catch((error) => console.log(error));
}

function assignemntRemainTime(assignment) {
  const assignemntTaskTime = assignment.tasks.reduce(
    (accumulate, task) => accumulate + task.est_hours,
    0
  );
  const remaintime =
    assignemntTaskTime > 0
      ? moment(assignment.due_date).diff(moment(), "hours") - assignemntTaskTime
      : Infinity;
  return remaintime;
}

onMounted(async () => {
  await fetchData();
  await nextTick();
});

function updateTasks(task, newStatus: string) {}
</script>
<style scoped>
:deep(.p-panel .p-panel-header, .p-panel-content) {
  border-radius: 0px;
}

:deep(.p-panel .p-panel-content) {
  border-radius: 0px;
}
</style>
<template>
  <div>
    <h1>My Day</h1>
    <div class="grid gap-2">
      <div class="card col">
        <h3>Suggested</h3>

        <div v-if="pendingTasks.length > 0">
          <TaskPanel
            v-for="(task, index) in pendingTasks"
            :key="task.id"
            :title="task.title"
            :id="task.id"
            :assignment_id="task.assignment_id"
            :description="task.description"
            :est_hour="task.est_hours"
            :status="task.status"
            :readOnly="true"
          />
        </div>
        <div v-else>
          <p><i>No task</i></p>
        </div>
      </div>

      <div class="card col">
        <h3>In progress</h3>
        <TaskPanel
          v-for="(task, index) in inProgressTasks"
          :key="index"
          :title="task.title"
          :id="task.id"
          :assignment_id="task.assignment_id"
          :description="task.description"
          :est_hour="task.est_hours"
          :status="task.status"
          :readOnly="true"
        />
      </div>
      <div class="card mb-3 col">
        <h3>Complete</h3>
        <TaskPanel
          v-for="(task, index) in completeTasks"
          :key="index"
          :title="task.title"
          :id="task.id"
          :assignment_id="task.assignment_id"
          :description="task.description"
          :est_hour="task.est_hours"
          :status="task.status"
          :readOnly="true"
        />
      </div>
    </div>
  </div>
</template>
