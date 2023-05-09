<script lang="ts" setup>
import { useAuthStore } from "@/stores/auth";
import { API_URL } from "@/utils/config";
import { onMounted, ref } from "vue";
import axios from "axios";
import moment from "moment";

const authStore = useAuthStore();
const assignments = ref([]);
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
        let assignment_required_time = assignment.tasks.reduce(
          (accumulate, task) => accumulate + task.est_hours,
          0
        );
        assignment.remained_time =
          moment(assignment.due_date).diff(moment(), "hours") -
          assignment_required_time;
      });
      console.log(assignments.value);
    })
    .catch((error) => console.log(error));
}
// courses.map(course=>{cour})
onMounted(async () => {
  await fetchData();
});
</script>
<style lang="scss" scope></style>
<template>
  <div>
    <h1>My Day</h1>
    <div class="grid gap-2">
      <div class="card col">
        <h3>Suggested</h3>
      </div>
      <div class="card col">
        <h3>In progress</h3>
      </div>
      <div class="card col">
        <h3>Complete</h3>
      </div>
    </div>
  </div>
</template>
