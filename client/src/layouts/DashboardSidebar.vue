<script setup lang="ts">
import { ref, defineProps } from "vue";
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
        font-size: 1.2rem;
        cursor: pointer;
        &:hover{
            background: rgba($color: #000000, $alpha: 0.1);
        }
    }
}
</style>
<template>
    <ul class="font-medium">
        <template v-for="(item, index) in model" :key="index">
            <li>
                <a>{{ item.label }}</a>
            </li>
        </template>
    </ul>
</template>
