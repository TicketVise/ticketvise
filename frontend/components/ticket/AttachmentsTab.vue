<template>
  <div class="w-full p-4 pt-2 mb-3">
    <div v-if="ticket.attachments.length > 0" class="w-full grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
      <attachment v-for="(attachment, index) in ticket.attachments" :key="index" :attachment="attachment"
                  @remove="ticket.attachments.splice(index, 1)" :show-delete="showDeleteButton(attachment.uploader.id)"/>
    </div>
    <div v-if="ticket.attachments.length === 0" class="text-center mb-4">
      <img src="/static/img/svg/undraw_upload_87y9.svg" alt="Nothing here" class="w-1/2 md:w-1/4 mx-auto mb-8">
      <span class="text-gray-600 text-lg md:text-xl">There are no attachments</span>
    </div>

    <div class="flex flex-col justify-center w-full p-4 px-0">
      <file-upload ref="upload" v-bind:value="files" v-on:input="setFiles" class="mb-4 w-full"
                   :preview="false"></file-upload>
      <error :key="errors" :message="errors" v-if="errors"></error>
    </div>
  </div>
</template>

<script>
  import Card from "../elements/card/Card";
  import '@toast-ui/editor/dist/toastui-editor-viewer.css';
  import 'codemirror/lib/codemirror.css';

  import '@toast-ui/editor/dist/toastui-editor.css';
  import FileUpload from "../elements/FileUpload";
  import Error from "../elements/message/Error";
  import Attachment from "./Attachment";

  import axios from 'axios'

  export default {
    components: {
      Attachment,
      Error,
      FileUpload,
      Card
    },
    props: {
      ticket: {
        type: Object,
        required: true
      },
      is_staff: {
        type: Boolean,
        required: true,
      },
      user: {
        type: Object,
        required: true,
      },
    },
    data: () => ({
      files: [],
      errors: ""
    }),
    methods: {
      submit() {
        let formData = new FormData()

        this.files.forEach(file => formData.append("files", file))
        const inboxId = this.$route.params.inboxId
        const ticketInboxId = this.$route.params.ticketInboxId

        axios.post(`/api/inboxes/${inboxId}/tickets/${ticketInboxId}/attachments`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }).then(() => {
          this.$emit('uploaded')
          this.$refs.upload.clear()
        }).catch(error => {
          if (error.response && error.response.status === 413) {
            this.errors = "Filesize too large, max filesize is 25MB."
          }
          this.$refs.upload.clear()
        })
      },
      setFiles(files) {
        this.files = files

        this.submit()
      },
      showDeleteButton(uploader_id) {
        return (this.is_staff || uploader_id === this.user.id)
      }
    }
  }
</script>
