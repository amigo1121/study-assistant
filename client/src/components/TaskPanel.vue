<script lang="ts" setup>
import { defineProps, defineEmits, ref } from "vue";
import { useConfirm } from "primevue/useconfirm";
import { useToast } from "primevue/usetoast";
import moment from "moment";
import TaskForm from "@/components/Form/TaskForm.vue";
import type { TaskStatus } from "@/utils/common";
const menu = ref(null);
const confirm = useConfirm();
const toast = useToast();
const emit = defineEmits(["delete", "update"]);
interface Props {
  title: string;
  description?: string;
  est_hour: number;
  assignment_id: number;
  id: number;
  readOnly?: boolean;
  status: TaskStatus;
}

const props = defineProps<Props>();

const confirmDelete = (event) => {
  confirm.require({
    target: event.currentTarget,
    message: "Do you want to delete this task?",
    icon: "pi pi-info-circle",
    acceptClass: "p-button-danger",
    accept: () => {
      emit("delete", props.id, props.assignment_id);
    },
    reject: () => {
      toast.add({
        severity: "error",
        summary: "Rejected",
        detail: "You have rejected",
        life: 3000,
      });
    },
  });
};

const items = ref([
  {
    label: "Options",
    items: [
      {
        label: "Update",
        icon: "pi pi-refresh",
        command: () => {
          emit("update", props.id, props.assignment_id);
        },
      },
      {
        label: "Delete",
        icon: "pi pi-times",
        command: () => {
          confirmDelete(event);
        },
      },
    ],
  },
]);

const toggle = () => {
  menu.value.toggle(event);
};
function modifyStatus(str) {
  str = str.toLowerCase().replace("_", " ");
  return str[0].toUpperCase() + str.slice(1);
}

function badgeColor() {
  switch (props.status) {
    case "NOT_STARTED":
      return "bg-gray-400";
    case "IN_PROGRESS":
      return "bg-yellow-400";
    case "COMPLETE":
      return "bg-green-400";
    default:
      return "bg-green-500";
  }
}
</script>
<style scoped></style>
<template>
  <Panel toggleable collapsed>
    <template #header>
      <div class="flex">
        <div class="align-self-baseline mr-3">{{ props.title }}</div>
        <Badge
          :value="modifyStatus(props.status)"
          class="align-self-baseline"
          :class="{ [badgeColor()]: true }"
        ></Badge>
      </div>
    </template>
    <template #icons v-if="!props.readOnly">
      <button class="p-panel-header-icon p-link mr-2" @click="toggle">
        <span class="pi pi-cog"></span>
      </button>
      <Menu ref="menu" id="config_menu" :model="items" popup />
    </template>
    <slot></slot>
  </Panel>
</template>
