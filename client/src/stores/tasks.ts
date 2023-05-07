import { defineStore } from "pinia";
import { formatDate, formatTime } from "../utils/datetime";
type Task = {
  id: string;
  title: string;
  description: string;
  dueDate: string;
  priority: string;
  hours: number;
  assignmentId: string;
  dependencies: string[]; // id of denpendent tasks
};

const tasks = [
  {
    id: "t001",
    title: "Task 1",
    description: "Description of Task 1",
    dueDate: "2023-05-01",
    priority: "high",
    hours: 5,
    assignmentId: "a001",
    dependencies: ["t002"],
  },
  {
    id: "t002",
    title: "Task 2",
    description: "Description of Task 2",
    dueDate: "2023-05-02",
    priority: "medium",
    hours: 8,
    assignmentId: "a001",
    dependencies: [],
  },
  {
    id: "t003",
    title: "Task 3",
    description: "Description of Task 3",
    dueDate: "2023-05-03",
    priority: "low",
    hours: 3,
    assignmentId: "a002",
    dependencies: ["t001", "t002"],
  },
  {
    id: "t004",
    title: "Task 4",
    description: "Description of Task 4",
    dueDate: "2023-05-04",
    priority: "high",
    hours: 7,
    assignmentId: "a002",
    dependencies: ["t001"],
  },
  {
    id: "t005",
    title: "Task 5",
    description: "Description of Task 5",
    dueDate: "2023-05-05",
    priority: "medium",
    hours: 4,
    assignmentId: "a003",
    dependencies: ["t003"],
  },
  {
    id: "t006",
    title: "Task 6",
    description: "Description of Task 6",
    dueDate: "2023-05-06",
    priority: "low",
    hours: 6,
    assignmentId: "a003",
    dependencies: ["t002", "t004"],
  },
];

export const useTasksStore = defineStore({
  id: "tasks",
  state: () => ({
    tasks: tasks,
  }),
  actions: {
    setTasks(tasks) {
      this.tasks = tasks;
    },
    modifyTask(taskId, newTask) {
      const index = this.tasks.findIndex((task) => task.id === taskId);
      this.tasks[index] = newTask;
    },
    addTask(task) {
      task.dueDate = formatDate(task.dueDate);
      task.dueTime = formatTime(task.dueTime);
      this.tasks.push({
        id: `Task-${Math.floor(Math.random() * 1000)}`,
        ...task,
      });
    },
    getTask(taskId) {
      return this.tasks.find((task) => task.id === taskId);
    },
    getTasksByAssignment(assignmentId) {
      return this.tasks.filter((task) => task.assignmentId === assignmentId);
    },
  },
});

export type { Task };
