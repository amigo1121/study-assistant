<script setup lang="ts">
import FormTask from '@/components/Form/FormTask.vue';
import BaseCard from '@/components/Card/BaseCard.vue';
import AssigmentCard from '@/components/Card/AssignmentCard.vue';
import TaskCard from '@/components/Card/TaskCard.vue'
import BaseDialog from '@/components/Dialog/BaseDialog.vue';
import TextEditor from '@/components/TextEditor.vue';
import AssignmentForm from '@/components/Form/AssignmentForm.vue';
import TaskForm from '@/components/Form/TaskForm.vue';
import { useAssignmentsStore } from '@/stores/assignments';
import { useTasksStore } from '@/stores/tasks';
import { storeToRefs } from 'pinia';
import { ref, onMounted, computed } from 'vue';
import { userItemStore } from '@/stores/items';
import { socket } from '@/utils/sockets';
const itemStore = userItemStore();

const { items } = storeToRefs(itemStore)
const textContent = ref("")
const print = () => {
    try {
        itemStore.addItem({
            content: textContent.value
        });
        textContent.value = ""
    } catch (error) {
        console.log(error)
    }
}

onMounted(() => {
    console.log("todo mounted")
    itemStore.fetchItems()
})
socket.start();

const test =  ()=>{
    socket.disconnect()
}

</script>
<style lang="scss" scoped>
li {
    list-style: none;
    margin-bottom: 1rem;
}
</style>
<template>
    <div class="todos">
        <ul>
            <li v-for="(item, index) in items" :key="index">{{ item.content }}</li>
        </ul>

        <form @submit.prevent="print">
            <label for="content">Content</label>
            <input type="text" id="content" v-model="textContent">
            <button type="submit">Submit</button>
        </form>
        <h3>Socket.io status: {{ socket.connected }}</h3>
        <button @click="test">test</button>
    </div>
</template>
