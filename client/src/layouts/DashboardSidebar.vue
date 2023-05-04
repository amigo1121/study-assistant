<script setup lang="ts">
import { ref, defineProps } from "vue";
import {useRoute} from 'vue-router';
const props = defineProps(['model'])
</script>
<style scoped lang="scss">
ul {
    width: 100%;
    margin-top: 0px;
    li {
        border-radius: 6px;
        padding: 1rem;
        width: 100%;
        margin-bottom: 1rem;
        list-style: none;
        text-decoration: none;
        cursor: pointer;
        &:hover{
            background: rgba($color: #000000, $alpha: 0.1);
        }
    }
}
</style>
<template>
    <ul class="font-medium text-xl">
        <template v-for="(item, index) in model" :key="index">
                <router-link :to="'/dashboard/'+item.name" class="text-50">
                    <li>  {{ item.label }} </li>
                </router-link>
        </template>
    </ul>
</template>
