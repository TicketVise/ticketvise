<template>
  <div class="w-full border border-gray-200 rounded pl-3 pr-4 py-3 flex text-sm leading-5 items-center">
    <font-awesome-icon class="text-2xl text-orange-400 group-hover:text-orange-500" :icon="icon" />
    <span class="w-full ml-2 flex-1 truncate text-gray-900">
      {{ getFilename(attachment.file) }}<span class="text-gray-400">.{{ getExtension(attachment.file) }}</span>
    </span>

    <!-- More menu -->
    <div class="relative">
      <div @click="menu = !menu" class="flex items-center justify-center relative ml-auto rounded-full cursor-pointer w-6 h-6 text-center -mr-2 hover:bg-gray-100">
        <i class="fa fa-ellipsis-v"></i>
      </div>

      <!-- Items -->
      <div v-if="menu" v-on-clickaway="away" class="absolute mt-2 right-0 bg-white shadow-md rounded text-left py-2 z-10">
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
  </div>
</template>

<script>
import axios from 'axios'
import { mixin as clickaway } from 'vue-clickaway'

export default {
  mixins: [ clickaway ],
  props: {
    attachment: {
      type: Object,
      required: true
    }
  },
  data: () => ({
    menu: false,
    icons: {
      pdf: 'file-pdf',
      jpg: 'file-image',
      jpeg: 'file-image',
      png: 'file-image',
      svg: 'file-image',
      c: 'file-code',
      mp3: 'file-audio',
      mp4: 'file-video',
      zip: 'file-archive',
      java: 'java',
      py: 'python',
      vue: 'vuejs',
      js: 'js',
      json: 'file-code'
    }
  }),
  computed: {
    icon() {
      return this.icons[this.getExtension(this.attachment.file)] || 'file'
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
      axios.delete('/api/attachments/' + attachment.id)
      this.$emit('remove')
    },
    away() {
      this.menu = false
    }
  }
}
</script>
