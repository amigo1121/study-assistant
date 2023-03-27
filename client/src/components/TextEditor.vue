<script>
import  Editor from '@tinymce/tinymce-vue'
import { QuillEditor } from '@vueup/vue-quill'
export default {
  
  components: {
    Editor,
    QuillEditor
  }
}
</script>

<template>
    <Editor
      api-key="srw8stxcb4tpixmawtc13361k70hzzy8osf8f7vx35kknueb"
      :init="{
        plugins: 'lists link image table code help wordcount'
      }"
    />
</template>
