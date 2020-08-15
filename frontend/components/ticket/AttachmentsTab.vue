<template>
  <div class="flex flex-col flex-wrap w-full mb-3">
    <ul v-if="ticket.attachments" class="border border-gray-200 rounded-md">
      <li class="pl-3 pr-4 py-3 flex items-center justify-between text-sm leading-5"
          v-for="attachment in ticket.attachments">
        <div class="w-0 flex-1 flex items-center">
          <svg class="flex-shrink-0 h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd"
                  d="M8 4a3 3 0 00-3 3v4a5 5 0 0010 0V7a1 1 0 112 0v4a7 7 0 11-14 0V7a5 5 0 0110 0v4a3 3 0 11-6 0V7a1 1 0 012 0v4a1 1 0 102 0V7a3 3 0 00-3-3z"
                  clip-rule="evenodd"/>
          </svg>
          <span class="ml-2 flex-1 w-0 truncate">
            {{ getFilename(attachment.file) }}
          </span>
        </div>
        <div class="ml-4 flex-shrink-0">
          <a :href="attachment.file" :download="getFilename(attachment.file)"
             class="font-medium text-orange-400 hover:text-orange-500 transition duration-150 ease-in-out">
            Download
          </a>
        </div>
      </li>
    </ul>
    <span v-if="!ticket.attachments" class="ml-2 text-sm leading-5">
      No attachments have been uploaded
    </span>
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
  methods: {
    getFilename: function (url) {
      return url.substring(url.lastIndexOf('/') + 1);
    }
  }
}
</script>

<style scoped>

</style>