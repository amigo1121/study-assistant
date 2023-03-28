import { defineStore } from "pinia";
import { formatDate, formatTime } from "../utils/datetime";
type Task = {
  id: string;
  title: string;
  description: string;
  dueDate: string;
  dueTime: string;
  importance: string;
  estHours: number;
  assignmentId: string;
  dependencies: string[]; // id of denpendent tasks
};

const tasks: Task[] = [
  {
    id: "1",
    title: "Finish Project Report",
    description: "Write up and submit the final project report",
    dueDate: "2023-04-01",
    dueTime: "23:59",
    importance: "High",
    estHours: 10,
    assignmentId: "123",
    dependencies: [],
  },
  {
    id: "2",
    title: "Prepare for Interview",
    description: "Research the company, practice interview questions",
    dueDate: "2023-03-30",
    dueTime: "10:00",
    importance: "Medium",
    estHours: 3,
    assignmentId: "456",
    dependencies: ["1"],
  },
  {
    id: "3",
    title: "Buy Groceries",
    description: "Buy milk, eggs, bread, and vegetables",
    dueDate: "2023-03-28",
    dueTime: "18:00",
    importance: "Low",
    estHours: 1,
    assignmentId: "789",
    dependencies: ["2"],
  },
  {
    id: "4",
    title: "Finish Coding Project",
    description: "Complete the coding tasks and submit the final project",
    dueDate: "2023-04-15",
    dueTime: "23:59",
    importance: "High",
    estHours: 15,
    assignmentId: "321",
    dependencies: ["2", "3"],
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
            this.tasks.push({ id: `Task-${Math.floor(Math.random()*1000)}`, ...task });
        },
        getTask(taskId) {
            return this.tasks.find((task) => task.id === taskId);
        },
        getTasksByAssignment(assignmentId) {
            return this.tasks.filter((task) => task.assignmentId === assignmentId);
        },
    }
});

export type { Task }