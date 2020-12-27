<template>
  <div class="w-full border border-gray-200 rounded pl-3 pr-4 py-3 flex text-sm leading-5 items-center">
    <font-awesome-icon class="text-2xl text-orange-400 group-hover:text-orange-500" :icon="[icon.prefix, icon.icon]"/>
    <span class="w-full ml-2 flex-1 truncate text-gray-900">
      {{ getFilename(attachment.file) }}<span class="text-gray-400">.{{ getExtension(attachment.file) }}</span>
    </span>

    <!-- More menu -->
    <div class="relative" v-if="showDelete">
      <div @click="menu = !menu"
           class="flex items-center justify-center relative ml-auto rounded-full cursor-pointer w-6 h-6 text-center -mr-2 hover:bg-gray-100">
        <i class="fa fa-ellipsis-v"></i>
      </div>

      <!-- Items -->
      <div v-if="menu" v-on-clickaway="away"
           class="absolute mt-2 right-0 bg-white shadow-md rounded text-left py-2 z-10">
        <a
            :href="attachment.file"
            :download="getFilename(attachment.file)"
            class="font-medium text-orange-400 group-hover:text-orange-500 flex space-x-2 w-full items-center space-x-2 group px-4 py-2 transition duration-100 ease-in-out hover:bg-orange-100 cursor-pointer"
        >
          <i class="fa fa-download text-orange-400 group-hover:text-orange-500"></i>
          <span>Download</span>
        </a>
        <button
            @click="remove(attachment)"
            class="font-medium text-red-700 group-hover:text-red-800 flex space-x-2 w-full items-center space-x-2 group px-4 py-2 transition duration-100 hover:bg-red-100 cursor-pointer"
        >
          <i class="fa fa-trash text-red-700 group-hover:text-red-800"></i>
          <span>Delete</span>
        </button>
      </div>
    </div>
    <div class="relative" v-else>
      <a :href="attachment.file"
         :download="getFilename(attachment.file)"
         class="flex items-center justify-center relative ml-auto rounded-full cursor-pointer w-6 h-6 text-center -mr-2 text-gray-700 hover:bg-gray-100">
        <i class="fa fa-download"></i>
      </a>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import {mixin as clickaway} from 'vue-clickaway'

import {library} from '@fortawesome/fontawesome-svg-core'
import {
  faFile,
  faFileArchive,
  faFileAudio,
  faFileCode,
  faFileImage,
  faFilePdf,
  faFileVideo
} from '@fortawesome/free-solid-svg-icons'
import {faJava, faJs, faPython, faVuejs} from '@fortawesome/free-brands-svg-icons'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'

library.add([faFilePdf, faFileImage, faFileCode, faFileAudio, faFileVideo,
  faFileArchive, faFile, faJava, faPython, faVuejs, faJs])

export default {
  components: {FontAwesomeIcon},
  mixins: [clickaway],
  props: {
    attachment: {
      type: Object,
      required: true
    },
    showDelete: {
      type: Boolean,
      default: true
    }
  },
  data: () => ({
    menu: false,
    icons: {
      pdf: {icon: 'file-pdf', prefix: 'fas'},
      jpg: {icon: 'file-image', prefix: 'fas'},
      jpeg: {icon: 'file-image', prefix: 'fas'},
      png: {icon: 'file-image', prefix: 'fas'},
      svg: {icon: 'file-image', prefix: 'fas'},
      c: {icon: 'file-code', prefix: 'fas'},
      mp3: {icon: 'file-audio', prefix: 'fas'},
      mp4: {icon: 'file-video', prefix: 'fas'},
      zip: {icon: 'file-archive', prefix: 'fas'},
      java: {icon: 'java', prefix: 'fab'},
      py: {icon: 'python', prefix: 'fab'},
      vue: {icon: 'vuejs', prefix: 'fab'},
      js: {icon: 'js', prefix: 'fab'},
      json: {icon: 'file-code', prefix: 'fas'}
    }
  }),
  computed: {
    icon() {
      return this.icons[this.getExtension(this.attachment.file)] || {icon: 'file', prefix: 'fas'}
    }
  },
  methods: {
    getFilename(url) {
      return url.substring(url.lastIndexOf('/') + 1, url.lastIndexOf('.'))
    },
    getExtension(url) {
      return url.substring(url.lastIndexOf('.') + 1);
    },
    remove(attachment) {
      this.menu = false
      const inboxId = this.$route.params.inboxId
      const ticketInboxId = this.$route.params.ticketInboxId

      axios.delete(`/api/inboxes/${inboxId}/tickets/${ticketInboxId}/attachments/${attachment.id}`)
      this.$emit('remove')
    },
    away() {
      this.menu = false
    }
  }
}
</script>
