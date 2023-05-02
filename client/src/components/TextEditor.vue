<script setup lang="ts">
import Editor from '@tinymce/tinymce-vue'
</script>
<style>
.tox-tinymce-aux {
  z-index: 99999999999 !important;
}
</style>
<template>
  <Editor api-key="srw8stxcb4tpixmawtc13361k70hzzy8osf8f7vx35kknueb" :init="{
    plugins: 'lists link image table code help wordcount'
  }" />
</template>
