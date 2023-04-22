<script setup lang="ts">

import { useAssignmentsStore } from '@/stores/assignments';
import { useTasksStore } from '@/stores/tasks';
import { storeToRefs } from 'pinia';
import { ref, onMounted, computed } from 'vue';
import { useItemStore } from '@/stores/items';
const textContent = ref("")
// const print = () => {
//     try {
//         itemStore.addItem({
//             content: textContent.value
//         });
//         textContent.value = ""
//     } catch (error) {
//         console.log(error)
//     }
// }

onMounted(() => {
    console.log("todo mounted")
    // itemStore.fetchItems()
})

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
        <!-- <ul>
            <li v-for="(item, index) in items" :key="index">{{ item.content }}</li>
        </ul>

        <form @submit.prevent="print">
            <label for="content">Content</label>
            <input type="text" id="content" v-model="textContent">
            <button type="submit">Submit</button>
        </form>
        <h3>Socket.io status: {{ socket.connected }}</h3>
        <button @click="test">test</button> -->
    </div>
</template>
