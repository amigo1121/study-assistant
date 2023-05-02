<script setup lang="ts">
import Editor from '@tinymce/tinymce-vue'
</script>

<template>
    <Editor
      api-key="srw8stxcb4tpixmawtc13361k70hzzy8osf8f7vx35kknueb"
      :init="{
        plugins: 'lists link image table code help wordcount'
      }"
    />
</template>
