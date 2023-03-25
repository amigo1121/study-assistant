import {defineStore} from 'pinia'


const assignments = [
  {
    title: 'Assignment 1',
    description: 'Lorem ipsum dolor sit amet',
    dueDate: new Date('2023-04-01'),
    dueTime: '23:59',
    importance: 'High',
  },
  {
    title: 'Assignment 2',
    description: 'Consectetur adipiscing elit',
    dueDate: new Date('2023-04-15'),
    dueTime: '18:00',
    importance: 'Medium',
  },
  {
    title: 'Assignment 3',
    description: 'Sed do eiusmod tempor incididunt',
    dueDate: new Date('2023-04-30'),
    dueTime: '09:00',
    importance: 'Low',
  },
];

export const useAssignmentsStore = defineStore({
  id: 'assignments',
  state: () => ({
    assignments: assignments,
  }),
  actions: {
    setAssignments(assignments) {
      this.assignments = assignments
    },
    modifiyAssignment(assignmentId, newAssignment) {
      const index = this.assignments.findIndex(
        (assignment) => assignment.id === assignmentId
      )
      this.assignments[index] = newAssignment
    },
  },
})
