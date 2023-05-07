<script setup lang="ts">
import { ref, onMounted, onBeforeMount, computed } from "vue";
import { useTasksStore } from "@/stores/tasks";
import { useAuthStore } from "@/stores/auth";
import Diagram from "@/components/Diagram.vue";
import { API_URL } from "@/utils/config";
import axios from "axios";
const authStore = useAuthStore();
const tasks = ref([]);
const assignments = ref([]);
const courses = ref([]);

onBeforeMount(async () => {
  let config = {
    headers: {
      Authorization: `Bearer ${authStore.accessToken}`,
    },
  };
  try {
    const response = await axios.get(
      API_URL + "/course/registered-courses",
      config
    );
    if (response.status === 200) {
      courses.value = response.data.registered_courses;

      courses.value.forEach((course) => {
        assignments.value = assignments.value.concat(course.assignments);
      });

      console.log(courses.value);
      console.log(assignments.value);
    } else throw new Error("Can't fetch Assignments");
  } catch (error) {
    console.log(error);
  }

  try {
    const response = await axios.get(API_URL + "/task/users", config);
    tasks.value = response.data;
    tasks.value.forEach((e) => {
      e.priority = e.priority[0] + e.priority.slice(1).toLowerCase();
      e.status =
        e.status[0] + e.status.slice(1).replace("_", " ").toLowerCase();
    });
  } catch (err) {
    console.log(err);
  }
});

const taskPriority = computed(() => {
  const stat = {
    low: 0,
    medium: 0,
    high: 0,
  };
  tasks.value
    .filter((e) => e.status !== "Complete")
    .forEach((task) => {
      stat[task.priority.toLowerCase()] += 1;
    });

  // console.log([stat.Low, stat.Medium, stat.High]);
  return [stat.low, stat.medium, stat.high];
});

const assignmentPriority = () => {
  const stat = {
    Low: 0,
    Medium: 0,
    High: 0,
  };
  assignments.value.forEach((assignment) => {
    stat[assignment.priority] += 1;
  });

  console.log([stat.Low, stat.Medium, stat.High]);
  return [stat.Low, stat.Medium, stat.High];
};
</script>
<style scoped></style>
<template>
  <div class="grid">
    <div class="col-6">
      <div class="card">
        <h5>Tasks</h5>
        <DataTable
          :value="tasks"
          :rows="5"
          :paginator="true"
          responsiveLayout="scroll"
        >
          <Column field="id" header="Task ID" :sortable="true"></Column>
          <Column field="title" header="Title" :sortable="true"></Column>
          <Column
            field="est_hours"
            header="Est. Hours"
            :sortable="true"
          ></Column>
          <Column field="priority" header="Priority" :sortable="true"></Column>
          <Column field="status" header="Status" :sortable="true"></Column>
        </DataTable>
      </div>
    </div>
    <div class="col-6">
      <div class="card">
        <h5>Assignments</h5>
        <DataTable
          :value="assignments"
          :rows="5"
          :paginator="true"
          responsiveLayout="scroll"
        >
          <Column field="id" header="Assignment ID" :sortable="true"></Column>
          <Column field="title" header="Title" :sortable="true"></Column>
          <Column field="due_date" header="Due date" :sortable="true"></Column>
          <Column field="priority" header="Priority" :sortable="true"></Column>
        </DataTable>
      </div>
    </div>
    <div class="col-6">
      <div class="card">
        <h5>Task by priority</h5>
        <Diagram :data="taskPriority"></Diagram>
      </div>
    </div>
  </div>
</template>
