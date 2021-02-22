<template>
  <div>
    <ckeditor :editor="editor" v-model="editorData" :config="editorConfig"></ckeditor>
  </div>
</template>

<script>
  import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
  import CKEditor from '@ckeditor/ckeditor5-vue2';

  export default {
    name: 'Editor',
    components: {
      // Use the component of the ckeditor5-vue2
      ckeditor: CKEditor.component
    },
    data() {
      return {
        // ClassicalEditor is the style of the editor
        editor: ClassicEditor,
        editorData: "",
        editorConfig: {
          toolbar: {
            items: [
              'heading',
              '|',
              'bold',
              'italic',
              '|',
              'bulletedList',
              'numberedList',
              '|',
              'insertTable',
              '|',
              'imageUpload',
              '|',
              'undo',
              'redo'
            ]
          },
          image: {
            toolbar: [
              'imageStyle:full',
              'imageStyle:side',
              '|',
              'imageTextAlternative'
            ]
          },
          table: {
            contentToolbar: ['tableColumn', 'tableRow', 'mergeTableCells']
          },
        }
      };
    }
  }
</script>

<!--
  Deep scoped styles will affect the style of the editor in this component only
-->
<style scoped>
  /deep/ .ck-editor__editable {
    min-height: 300px;
  }
</style>