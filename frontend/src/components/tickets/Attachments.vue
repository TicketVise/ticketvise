<template>
  <div class="w-full">
    <div v-if="ticket.attachments.length > 0" class="w-full grid grid-cols-1 sm:grid-cols-2 gap-4">
      <attachment v-for="(attachment, index) in ticket.attachments" :key="index" :attachment="attachment"
                  @remove="$emit('uploaded')" :show-delete="showDeleteButton(attachment.uploader.id)"/>
<!-- @remove="ticket.attachments.splice(index, 1)" -->
    </div>
    <!-- <div v-if="ticket.attachments.length === 0" class="text-center mb-4">
      <img :src="upload" alt="Nothing here" class="w-1/2 md:w-1/4 mx-auto mb-8">
      <span class="text-sm leading-8 text-gray-500">There are no attachments</span>
    </div> -->

    <div class="flex flex-col justify-center w-full mt-4">
      <file-upload ref="upload" v-bind:value="files" v-on:input="setFiles" class="mb-4 w-full" :preview="false" />
      <error :key="errors" :message="errors" v-if="errors"></error>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

import FileUpload from '@/components/inputs/FileInput'
import Error from '@/components/inputs/Error'
import Attachment from './Attachment'

const Upload = require('@/assets/img/svg/upload.svg')

export default {
  components: {
    Attachment,
    Error,
    FileUpload
  },
  props: {
    ticket: {
      type: Object,
      required: true
    }
  },
  data: () => ({
    files: [],
    errors: '',
    upload: Upload
  }),
  methods: {
    submit () {
      const formData = new FormData()
      this.files.forEach(file => formData.append('files', file))
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
          this.errors = 'Filesize too large, max filesize is 25MB.'
        }
        this.$refs.upload.clear()
      })
    },
    setFiles (files) {
      this.files = files
      this.submit()
    },
    showDeleteButton (uploaderId) {
      return (this.is_staff || uploaderId === this.user.id)
    }
  },
  computed: {
    user () {
      return this.$store.state.user
    }
  }
}
</script>
