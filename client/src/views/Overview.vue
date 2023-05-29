<script setup lang="ts">
import { ref, onMounted, onBeforeMount, computed, nextTick } from "vue";
import { useAuthStore } from "@/stores/auth";
import Chart from "primevue/chart";
import Diagram from "@/components/Diagram.vue";
import { API_URL } from "@/utils/config";
import axios from "axios";
import moment from "moment";
const authStore = useAuthStore();
const tasks = ref([]);
const assignments = ref([]);
const courses = ref([]);

const assignmentsNames = () => {
  return assignments.value.map((e) => e.name);
};

const assignmentsEstimateTime = () => {
  console.log(assignments.value.map((e) => e.est_time));
  return assignments.value.map((e) => e.est_time);
};

const assignemntsRemainTime = () => {
  return assignments.value.map((e) => e.remained_time);
};

const chartData = computed(() => {
  const documentStyle = getComputedStyle(document.documentElement);

  return {
    labels: assignmentsNames(),
    datasets: [
      {
        type: "bar",
        label: "Estimate time to complete",
        backgroundColor: documentStyle.getPropertyValue("--blue-500"),
        data: assignmentsEstimateTime(),
      },
      {
        type: "bar",
        label: "Remained time",
        backgroundColor: documentStyle.getPropertyValue("--green-500"),
        data: assignemntsRemainTime(),
      },
    ],
  };
});

const chartOptions = computed(() => {
  const documentStyle = getComputedStyle(document.documentElement);
  const textColor = documentStyle.getPropertyValue("--text-color");
  const textColorSecondary = documentStyle.getPropertyValue(
    "--text-color-secondary"
  );
  const surfaceBorder = documentStyle.getPropertyValue("--surface-border");

  return {
    indexAxis: "y",
    maintainAspectRatio: false,
    aspectRatio: 0.8,
    plugins: {
      legend: {
        labels: {
          fontColor: textColor,
        },
      },
    },
    scales: {
      x: {
        ticks: {
          color: textColorSecondary,
          font: {
            weight: 500,
          },
        },
        grid: {
          display: false,
          drawBorder: false,
        },
      },
      y: {
        ticks: {
          color: textColorSecondary,
        },
        grid: {
          color: surfaceBorder,
          drawBorder: false,
        },
      },
    },
  };
});

function filterOutdatedAssignments() {
  assignments.value = assignments.value.filter(
    (assignment) => moment(assignment.due_date).diff(moment(), "hours") > 0
  );
}

function calcRemainTime() {
  assignments.value.forEach((assignment) => {
    assignment.remained_time = assignemntRemainTime(assignment);
  });
}

function assignemntRemainTime(assignment) {
  const remaintime = moment(assignment.due_date).diff(moment(), "hours");
  return remaintime;
}

function assignemntEstimateTime(assignment) {
  const estTime = assignment.tasks.reduce((sum, t) => {
    if (t.status !== "COMPLETE") return sum + t.est_hours;
    else return sum;
  }, 0);
  return estTime;
}

function calcEstTime() {
  assignments.value.forEach((assignment) => {
    assignment.est_time = assignemntEstimateTime(assignment);
  });
}

onBeforeMount(async () => {
  let config = {
    headers: {
      Authorization: `Bearer ${authStore.accessToken}`,
    },
  };
  try {
    const response = await axios.get(API_URL + "/task/user/assignment", config);
    if (response.status === 200) {
      assignments.value = response.data;
      filterOutdatedAssignments();
      calcEstTime();
      calcRemainTime();
      await nextTick();
      console.log("assignment", assignments.value);
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
    tasks.value = tasks.value.filter((e) => e.status !== "Complete");
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
</script>
<style scoped></style>
<template>
  <div class="flex gap-3 w-full">
    <div class="w-full">
      <div class="card">
        <h5>Tasks</h5>
        <DataTable
          :value="tasks"
          :rows="5"
          :paginator="true"
          responsiveLayout="scroll"
          v-if="tasks.length > 0"
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
        <div v-else><i>No task</i></div>
      </div>

      <div class="card w-full">
        <h5>Task by priority</h5>
        <Diagram :data="taskPriority" v-if="tasks.length > 0"></Diagram>
        <div v-else><i>No task</i></div>
      </div>
    </div>
    <div class="w-full">
      <div class="card w-full">
        <h5>Assignments</h5>
        <DataTable
          :value="assignments"
          :rows="5"
          :paginator="true"
          responsiveLayout="scroll"
          v-if="assignments.length > 0"
        >
          <Column field="id" header="Assignment ID" :sortable="true"></Column>
          <Column field="name" header="Name" :sortable="true"></Column>
          <Column
            field="remained_time"
            header="Time left(hours)"
            :sortable="true"
          ></Column>
          <Column
            field="est_time"
            header="Estimate time(hours)"
            :sortable="true"
          ></Column>
        </DataTable>
        <div v-else><i>No Assignment</i></div>
      </div>
      <div class="card w-full">
        <h5>Assignments stats</h5>
        <Chart
          type="bar"
          :data="chartData"
          :options="chartOptions"
          class="h-20rem"
          v-if="assignments.length > 0"
        />
        <div v-else><i>No Assignment</i></div>
      </div>
    </div>
  </div>
</template>
