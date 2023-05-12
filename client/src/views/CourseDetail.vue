<script lang="ts" setup>
import { API_URL } from "@/utils/config";
import { sanitize } from "@/utils/santizie";
import axios from "axios";
import { useRoute } from "vue-router";
import { onBeforeMount, reactive, ref, nextTick, onBeforeUpdate } from "vue";
import { defineAsyncComponent } from "vue";
import { useAuthStore } from "@/stores/auth";
import AssignmentPanel from "@/components/AssignmentPanel.vue";
import AssignmentForm from "@/components/Form/AssignmentForm.vue";
import TaskPanel from "@/components/TaskPanel.vue";
import moment from "moment";
import router from "@/router";
import { useDialog } from "primevue/usedialog";
import { useToast } from "primevue/usetoast";
import TaskForm from "@/components/Form/TaskForm.vue";
import { useTasksStore } from "@/stores/tasks";
const dialog = useDialog();
const TaskGraph = defineAsyncComponent(
  () => import("@/components/TaskGraph.vue")
);
// stores
const route = useRoute();
const authStore = useAuthStore();
const toast = useToast();
let courseData = ref({});
const assignments = ref([]);
const errorMsg = ref([]);
// hooks
onBeforeMount(async () => {
  const courseCode = route.params.coursecode;
  const config = {
    headers: {
      Authorization: `Bearer ${authStore.accessToken}`,
    },
  };
  try {
    const response = await axios(
      API_URL + `/course/registered-course/${courseCode}`,
      config
    );
    courseData.value = response.data;
    assignments.value = response.data.assignments;
  } catch (error) {
    console.log(error);
  }
});

const updateAssignmentTasks = async (assignment_id, newTasks) => {
  const assignmentIndex = assignments.value.findIndex(
    (e) => e.id === assignment_id
  );
  await nextTick();
  assignments.value[assignmentIndex].tasks = newTasks;
  await nextTick();
};

const validateInput = (taskInput) => {
  errorMsg.value = [];
  if (!taskInput.title) errorMsg.value.push("Task title is empty");

  if (!taskInput.est_hours) errorMsg.value.push("Task estimate hours is empty");

  return errorMsg.value.length === 0;
};
const showCreateTaskDialog = async (assignment) => {
  const options = assignment.tasks.map((task) => ({
    title: task.title,
    id: task.id,
  }));
  const dialogRef = dialog.open(TaskForm, {
    props: {
      header: "Add taks",
      style: {
        width: "50rem",
      },
      modal: true,
    },
    data: {
      options: options,
    },
    emits: {
      onCreate: (newTaskInfo) => {
        if (!validateInput(newTaskInfo)) {
          broadcastErrorMessage();
          return;
        }
        newTaskInfo.assignment_id = assignment.id;
        const config = {
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        };
        axios
          .post(API_URL + "/task", newTaskInfo, config)
          .then(async (response) => {
            dialogRef.close();
            toast.add({
              severity: "success",
              Summary: "Success",
              detail: "Create task success",
              life: 1000,
            });
            fetchAssighnmentTasks(assignment.id)
              .then((res) => {
                updateAssignmentTasks(assignment.id, res.data);
              })
              .catch((err) => {
                console.log(err);
              });
          })
          .catch((error) => {
            console.log(error.response);
          });
      },
      onCancel: () => {
        dialogRef.close();
      },
    },
  });
};

const deleteTask = (taskID, assignmentID) => {
  const config = {
    headers: {
      Authorization: `Bearer ${authStore.accessToken}`,
    },
  };

  axios
    .delete(API_URL + `/task/${taskID}`, config)
    .then((response) => {
      if (response.status === 200) {
        toast.add({
          severity: "success",
          Summary: "Success",
          detail: "Delete task success",
          life: 1000,
        });
      }
      fetchAssighnmentTasks(assignmentID)
        .then((res) => {
          updateAssignmentTasks(assignmentID, res.data);
        })
        .catch((err) => {
          console.log(err);
        });
    })
    .catch((error) => {
      console.log(error);
    });
};

function broadcastErrorMessage() {
  errorMsg.value.forEach((msg) => {
    toast.add({ severity: "error", summary: "Error", detail: msg, life: 1000 });
  });
}

function getDependedTasks(task, assignment) {
  let ans = [];
  if (task.depended_by.length > 0) {
    task.depended_by.forEach(({ task_id }) => {
      const t = assignment.tasks.find((e) => e.id === task_id);
      ans.push(task_id);
      ans = ans.concat(getDependedTasks(t, assignment));
    });
    return ans;
  }
  return [];
}

const updateTask = (taskID, assignmentID) => {
  // const assignment
  const assignment = assignments.value.find((e) => e.id === assignmentID);
  const task = assignment.tasks.find((e) => e.id === taskID);
  const dependedTaskOnThis = getDependedTasks(task, assignment);
  const options = assignment.tasks
    .map((task) => ({ title: task.title, id: task.id }))
    .filter((e) => e.id !== taskID && !dependedTaskOnThis.includes(e.id));
  const dialogRef = dialog.open(TaskForm, {
    props: {
      header: "Update taks",
      style: {
        width: "50rem",
      },
      modal: true,
    },
    data: {
      options: options,
      state: {
        title: task.title,
        status: task.status,
        priority: task.priority,
        description: task.description,
        est_hours: task.est_hours,
        id: task.id,
        dependencies: task.depends_on.map((e) => e.depend_on_task_id),
      },
    },
    emits: {
      onUpdate: (newTask) => {
        if (!validateInput(newTask)) {
          broadcastErrorMessage();
          return;
        }
        const config = {
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        };
        axios
          .put(API_URL + `/task/${taskID}`, newTask, config)
          .then((response) => {
            dialogRef.close();
            toast.add({
              severity: "success",
              Summary: "Success",
              detail: "Update task success",
              life: 1000,
            });
            fetchAssighnmentTasks(assignment.id)
              .then((res) => {
                updateAssignmentTasks(assignment.id, res.data);
              })
              .catch((err) => {
                console.log(err);
              });
          })
          .catch((error) => {
            console.log(error);
          });
      },
      onCancel: () => {
        dialogRef.close();
      },
    },
  });
  // console.log({ taskID, assignment })
  // console.log(task)
};

const fetchAssighnmentTasks = (assignment_id) => {
  const config = {
    headers: {
      Authorization: `Bearer ${authStore.accessToken}`,
    },
  };
  return axios(API_URL + `/task/${assignment_id}/tasks`, config);
};
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
  <div class="m-auto">
    <h1>{{ courseData.name + " - " + courseData.code }}</h1>
    <h2>
      Professor: {{ courseData.teacher?.first_name }}
      {{ courseData.teacher?.last_name }}
    </h2>
    <div class="mb-3">
      <h3>Schedule:</h3>
      <ul class="list-none mb-0 pl-3">
        <li
          v-for="(schedule, index) in courseData.schedules"
          :key="index"
          class="mb-2"
        >
          {{ schedule.week_day }}:
          {{ moment(schedule.start_time, "HH:mm:ss").format("HH:mm") }} -
          {{ moment(schedule.end_time, "HH:mm:ss").format("HH:mm") }}
        </li>
      </ul>
    </div>
    <h3>Assignments</h3>
    <div v-if="assignments.length > 0">
      <div class="card">
        <AssignmentPanel
          v-for="(assignment, index) in assignments"
          :key="index"
          :name="assignment.name"
          :description="assignment.description"
          :deadline="assignment.due_date"
          :id="assignment.id"
          readOnly
        >
          <TabView>
            <TabPanel header="Description">
              <div v-html="sanitize(assignment.description)"></div>
            </TabPanel>
            <TabPanel header="Tasks">
              <div class="flex justify-content-end">
                <Button class="mb-3" @click="showCreateTaskDialog(assignment)"
                  >Add task</Button
                >
              </div>
              <TaskPanel
                v-for="(task, index) in assignment.tasks"
                :key="index"
                :title="task.title"
                :id="task.id"
                :assignment_id="assignment.id"
                :description="task.description"
                :status="task.status"
                :est_hours="task.est_hours"
                @delete="deleteTask"
                @update="updateTask"
              >
                <div v-html="sanitize(task.description)"></div>
              </TaskPanel>
            </TabPanel>
            <TabPanel header="Task graph">
              <TaskGraph :assignment_id="assignment.id"></TaskGraph>
            </TabPanel>
          </TabView>
        </AssignmentPanel>
      </div>
    </div>
    <div v-else>
      <div class="card">
        <i>No assignments</i>
      </div>
    </div>
    <ConfirmDialog></ConfirmDialog>
  </div>
</template>
