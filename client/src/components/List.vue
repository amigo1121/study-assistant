<script lang="ts" setup>
const props = defineProps ({
    items: {
        type: Array,
        required: true
    },
    height: {
        type: String,
        required: true
    },
    width : {
        type: String,
        required: true
    }
})
</script>
<style lang="scss" scoped>
.list {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: #f5f5f5;
    padding: 1rem;
    overflow: scroll;
    position:absolute;
    ul{
        height: 100%;
        width: 100%;
        list-style: none;
    }
}
</style>
<template>
    <div class="list" :style="{ height:height, width:width }">
        <ul>
            <li v-for="item in items" :key="item.id">
                {{ item.name }}
            </li>
        </ul>
    </div>
</template>