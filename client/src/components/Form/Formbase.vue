<script setup lang="ts"></script>
<style lang="scss" scoped>
.formbase {
  display: block;
  border: 1px solid orange;
  width: fit-content;
  padding: 1rem;
  border-radius: 6px;
}
</style>
<template>
  <div class="formbase">
    <slot></slot>
  </div>
</template>
