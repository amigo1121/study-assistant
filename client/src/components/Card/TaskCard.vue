<script lang="ts">
import { defineComponent } from "vue";
import BaseCard from "./BaseCard.vue";
import { useTasksStore } from "@/stores/tasks";
import { sanitize } from "@/utils/santizie";

export default defineComponent({
  name: "TaskCard",
  components: {
    BaseCard,
  },
  props: {
    id: {
      type: String,
      required: false,
      default: "",
    },
    title: {
      type: String,
      required: false,
      default: "",
    },
    importance: {
      type: String,
      required: false,
      default: "",
    },
    description: {
      type: String,
      required: false,
      default: "",
    },
    dueDate: {
      type: String,
      required: false,
      default: "",
    },
    dueTime: {
      type: String,
      required: false,
      default: "",
    },
    estHours: {
      type: Number,
      required: false,
      default: "",
    },
    assignmentId: {
      type: String,
      required: false,
      default: "",
    },
    dependencies: {
      type: Array,
      required: false,
      default: () => [],
    },
  },
  data() {
    return {
      openDialog: false,
      taskStore: useTasksStore(),
    };
  },
  computed: {
    sanitizedInput() {
      return sanitize(this.description);
    },
  },
});
</script>
<style scoped lang="scss"></style>
<template>
  <BaseCard>
    <div>
      <h2>{{ title }}</h2>
      <div class="bg-yellow-100 border-round-xl p-3">
        <h4>Description:</h4>
        <div v-html="sanitizedInput"></div>
      </div>
      <p>Priority: {{ importance }}</p>
      <p>Due date: {{ dueDate }}</p>
      <p>Due time: {{ dueTime }}</p>
      <p>Estimated hours: {{ estHours }}</p>
      <h3 v-if="dependencies.length > 0">Depends on:</h3>
      <ul>
        <li v-for="taskId in dependencies" :key="taskId">
          <h5>{{ taskStore.getTask(taskId).title }}</h5>
        </li>
      </ul>
    </div>
  </BaseCard>

  <Dialog> </Dialog>
</template>
