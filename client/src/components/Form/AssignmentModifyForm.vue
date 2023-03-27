<script lang="ts">
import Formbase from './Formbase.vue';
import { defineComponent, inject } from 'vue';
import _ from 'lodash';
import { useAssignmentsStore } from '@/stores/assignments';
const store = useAssignmentsStore();
export default defineComponent({
    name: 'AssignmentModifyForm',
    components: {
        Formbase
    },
    data() {
        return {
                id: this.assignment.id,
                title: this.assignment.title,
                importance: this.assignment.importance,
                description: this.assignment.description,
                dueDate: this.assignment.dueDate,
                dueTime: this.assignment.dueTime
        }
    },
    emits: ['close'],
    inject: ['closeDialog', 'assignment'],
    methods: {
        modifyAssignment(){
            if(!_.isEqual(this.assignment, this.$data)){
                const {id,...data} = this.$data;
                store.modifyAssignment(id, data);
            }
            this.closeDialog();
        }
    },
})
</script>

<template>
    <Formbase>
        <form @submit.prevent="modifyAssignment">
            <div class="form-group">
                <label for="asssignment-name">Assignment Name</label>
                <input type="text" id="" v-model="title" @keydown.enter.prevent/>
            </div>

            <div class="form-group">
                <label for="importance">Importance</label>
                <select name="importance" id="" v-model="importance">
                    <option value="Low">Low</option>
                    <option value="Medium">Medium</option>
                    <option value="High">High</option>
                </select>
            </div>

            <div class="form-group">
                <label for="description">Description</label>
                <textarea name="description" id="" cols="30" rows="10" v-model="description"></textarea>
            </div>

            <div class="form-group">
                <label for="due-date">Due Date</label>
                <input type="date" name="due-date" id="" v-model="dueDate"/>  
            </div>
        
            <div class="form-group">
                <label for="due-time">Due Time</label>
                <input type="time" name="due-time" id="" v-model="dueTime"/>
            </div>

            <div class="form-group">
                <button type="submit">Submit</button>
                <button type="button" @click="closeDialog">Cancel</button>
            </div>
        </form>
    </Formbase>
</template>