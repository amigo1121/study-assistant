<script lang="ts" setup>
import draggable from "vuedraggable";
import { useAuthStore } from "@/stores/auth";
import { API_URL } from "@/utils/config";
import { onMounted, ref, computed, onBeforeMount, nextTick } from "vue";
import { TaskPriorityTree } from "@/utils/TaskPriorityTree";
import TaskPanel from "@/components/TaskPanel.vue";
import { useToast } from "primevue/usetoast";

import axios from "axios";
import moment from "moment";

const authStore = useAuthStore();
const assignments = ref([]);
const inProgressTasks = ref([]);
const completeTasks = ref([]);
const pendingTasks = ref([]);
const toast = useToast();

function assignmentFilterOutTask(assignment) {
  assignment.tasks = assignment.tasks.filter((t) => t.status === "NOT_STARTED");
}

function filterOutTasks() {
  assignments.value.forEach((assignment) => {
    assignmentFilterOutTask(assignment);
  });
}

function calcRemainTime() {
  assignments.value.forEach((assignment) => {
    assignment.remained_time = assignemntRemainTime(assignment);
  });
}

function sortAssignment() {
  assignments.value.sort((a, b) => a.remained_time - b.remained_time);
}

function getTaskList() {
  pendingTasks.value = assignments.value.reduce(
    (accumList, assignment) => accumList.concat(assignment.tasks),
    []
  );
}

function processNotStartedTasks() {
  filterOutTasks();
  calcRemainTime();
  sortAssignment();
  getTaskList();
}

function processInprogressAndCompleteTasks() {
  assignments.value.forEach((assignment) => {
    inProgressTasks.value = inProgressTasks.value.concat(
      assignment.tasks.filter((t) => t.status === "IN_PROGRESS")
    );
    completeTasks.value = completeTasks.value.concat(
      assignment.tasks.filter((t) => t.status === "COMPLETE")
    );
  });
}

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
  processInprogressAndCompleteTasks();
  processNotStartedTasks();
  await nextTick();
});

function updateTasks(task) {
  const config = {
    headers: {
      Authorization: `Bearer ${authStore.getAccessToken}`,
    },
  };
  const updateData = {
    id: task.id,
    status: task.status,
  };
  return axios.put(API_URL + "/task/status", updateData, config);
}

function getAssignmentTask(assignment_id) {
  const config = {
    headers: {
      Authorization: `Bearer ${authStore.getAccessToken}`,
    },
  };
  return axios.get(API_URL + `/task/todos/assignment/${assignment_id}`, config);
}
async function onAdd(event, str, list) {
  const oldTaskStatus = list[event.newDraggableIndex].status;
  list[event.newDraggableIndex].status = str;
  await updateTasks(list[event.newDraggableIndex])
    .then(async (response) => {
      const updatedTask = response.data;
      if (
        updatedTask.status === "NOT_STARTED" ||
        oldTaskStatus === "NOT_STARTED"
      )
        await fetchData();
      processNotStartedTasks();
      await nextTick();
      toast.add({
        severity: "success",
        Summary: "Success",
        detail: "Update task success",
        life: 3000,
      });
    })
    .catch((error) => {
      console.log(error);
    });
}

const dragOptions = computed(() => {
  return {
    animation: 200,
    group: "description",
    disabled: false,
    ghostClass: "ghost",
  };
});
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
      <draggable
        class="card col"
        :list="pendingTasks"
        group="task"
        v-bind="dragOptions"
        itemKey="id"
        :sort="false"
        @add="(event) => onAdd(event, 'NOT_STARTED', pendingTasks)"
      >
        <template #header>
          <h3>Not started</h3>
          <div v-if="pendingTasks.length === 0">
            <p><i>No task</i></p>
          </div>
        </template>
        <template #item="{ element, index }">
          <TaskPanel v-bind="element" :readOnly="true">
            <div v-html="element.description"></div>
          </TaskPanel>
        </template>
      </draggable>
      <draggable
        class="card col"
        :list="inProgressTasks"
        group="task"
        v-bind="dragOptions"
        itemKey="id"
        @add="(event) => onAdd(event, 'IN_PROGRESS', inProgressTasks)"
      >
        <template #header>
          <h3>In progress</h3>
          <div v-if="inProgressTasks.length === 0">
            <p><i>No task</i></p>
          </div>
        </template>
        <template #item="{ element, index }">
          <TaskPanel v-bind="element" :readOnly="true">
            <div v-html="element.description"></div>
          </TaskPanel>
        </template>
      </draggable>
      <draggable
        class="card col mb-3"
        :list="completeTasks"
        group="task"
        v-bind="dragOptions"
        itemKey="id"
        @add="(event) => onAdd(event, 'COMPLETE', completeTasks)"
      >
        <template #header>
          <h3>Complete</h3>
          <div v-if="completeTasks.length === 0">
            <p><i>No task</i></p>
          </div>
        </template>
        <template #item="{ element, index }">
          <TaskPanel v-bind="element" :readOnly="true">
            <div v-html="element.description"></div>
          </TaskPanel>
        </template>
      </draggable>
    </div>
  </div>
</template>
