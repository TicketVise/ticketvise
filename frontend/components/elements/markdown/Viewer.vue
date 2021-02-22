<template>
  <div>
    <ckeditor :editor="editor" :disabled="true" :value="initialValue" :config="editorConfig"></ckeditor>
  </div>
</template>

<script>
  import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
  import CKEditor from "@ckeditor/ckeditor5-vue2";

  export default {
    name: 'app',
    props: {
      initialValue: ""
    },
    components: {
      // Use the component of the ckeditor5-vue2
      ckeditor: CKEditor.component
    },
    data() {
      return {
        editor: ClassicEditor,
        // This editor will be read–only when created.
        editorDisabled: true,
        editorConfig: {
          toolbar: {
            items: []
          },
        }
      };
    }
  }
</script>

<!--
  Deep scoped styles will affect the style of the viewer in this component only
-->
<style scoped>
  /deep/ .ck-editor__editable {
    min-height: 0;
  }
</style>