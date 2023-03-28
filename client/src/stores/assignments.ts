import {defineStore} from 'pinia'
import {formatDate, formatTime} from '../utils/datetime'
type Assignment = {
  id: string
  title: string
  description: string
  dueDate: string
  dueTime: string
  importance: string

}

const assignments: Assignment[] = [
  {
    id: '2',
    title: 'Lab Report',
    description: '<h2>Experiment Analysis</h2> <p>Conduct a statistical analysis on the data collected from the lab experiment and write a report on your findings.</p>',
    dueDate: '2023-04-15',
    dueTime: '17:00',
    importance: 'High',
  },
  {
    id: '3',
    title: 'Group Project',
    description: '<h3>Collaboration</h3> <p>Work with your assigned team to develop a project proposal and presentation on a chosen topic.</p>',
    dueDate: '2023-05-01',
    dueTime: '23:59',
    importance: 'Medium',
  },
  {
    id: '4',
    title: 'Reading Assignment',
    description: '<h4>Chapter Review</h4> <p>Read and summarize chapters 5-7 of the assigned textbook.</p>',
    dueDate: '2023-04-05',
    dueTime: '12:00',
    importance: 'Low',
  }
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
    modifyAssignment(assignmentId, newAssignment) {
      const index = this.assignments.findIndex(
        (assignment) => assignment.id === assignmentId
      )
      this.assignments[index] = newAssignment
    },
    addAssignment(assignment) {
      assignment.dueDate = formatDate(assignment.dueDate)
      assignment.dueTime = formatTime(assignment.dueTime)
      this.assignments.push({id:`${Math.random()}`,...assignment})
    }
  },
})

export type {Assignment}