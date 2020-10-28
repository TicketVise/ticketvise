<template>
  <div class="w-full p-4 pt-2 mb-3">
    <div v-if="ticket.attachments.length > 0" class="w-full grid sm:grid-cols-2 xl:grid-cols-3 gap-4">
      <Attachment v-for="(attachment, index) in ticket.attachments" :key="index" :attachment="attachment" @remove="ticket.attachments.splice(index, 1)" />
    </div>
    <div v-if="ticket.attachments.length === 0" class="text-center mb-4">
      <img src="/static/img/svg/undraw_upload_87y9.svg" alt="Nothing here" class="w-1/2 md:w-1/4 mx-auto mb-8">
      <span class="text-gray-600 text-lg md:text-xl">There are no attachments</span>
    </div>

    <div class="flex flex-col justify-center w-full p-4 px-0">
      <file-upload ref="upload" v-bind:value="files" v-on:input="setFiles" class="mb-4 w-full" :preview="false"></file-upload>
      <error v-for="error in this.errors.attachments" :key="error" :message="error"></error>
    </div>
  </div>
</template>

<script>
  import Card from "../elements/card/Card";
  import '@toast-ui/editor/dist/toastui-editor-viewer.css';
  import 'codemirror/lib/codemirror.css';

  import '@toast-ui/editor/dist/toastui-editor.css';

  export default {
    components: {
      Card
    },
    props: {
      ticket: {
        type: Object,
        required: true
      },
    },
    data: () => ({
      files: [],
      errors: []
    }),
    methods: {
      submit() {
        let formData = new FormData()

        this.files.forEach(file => formData.append("files", file))

        axios.defaults.xsrfCookieName = 'csrftoken'
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

        axios.post("/api" + window.location.pathname + '/attachments', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }).then(() => {
          this.$emit('uploaded')
          this.$refs.upload.clear()
        }).catch(error => {
          this.errors = error.response.data
          this.$refs.upload.clear()
        })
      },
      setFiles(files) {
        this.files = files

        this.submit()
      }
    }
  }
</script>
