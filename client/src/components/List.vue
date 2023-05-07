<script lang="ts" setup>
const props = defineProps({
  items: {
    type: Array,
    required: true,
  },
  height: {
    type: String,
    required: true,
    default: "20rem",
  },
  width: {
    type: String,
    required: true,
    default: "100%",
  },
});
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
  position: absolute;
}
</style>
<template>
  <div class="list" :style="{ height: height, width: width }"></div>
</template>
