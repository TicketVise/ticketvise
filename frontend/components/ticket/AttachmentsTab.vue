<template>
  <div class="w-full p-4 mb-3">
    <ul v-if="ticket.attachments.length > 0" class="grid sm:grid-cols-2 xl:grid-cols-3 gap-4">
      <li class="border border-gray-200 rounded-md pl-3 pr-4 py-3 flex items-center justify-between text-sm leading-5"
          v-for="(attachment, index) in ticket.attachments" :key="index">
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
    <div v-if="ticket.attachments.length === 0" class="text-center mb-8">
      <img src="/static/img/svg/undraw_upload_87y9.svg" alt="Nothing here" class="w-1/2 md:w-1/4 mx-auto mb-8">
      <span class="text-gray-600 text-lg md:text-xl">There are no attachments</span>
    </div>

    <div class="flex w-full p-4">
      <div class="flex flex-col items-center flex-grow w-full mb-4">
        <button @click="upload"
                class="group relative w-full sm:w-auto flex justify-center sm:justify-start items-center py-2 px-4 border border-transparent text-sm leading-5 font-medium rounded-md text-white bg-primary hover:bg-orange-500 focus:outline-none focus:border-orange-700 focus:shadow-outline-orange active:bg-orange-700 transition duration-150 ease-in-out">
          <i class="fa fa-upload text-orange-200 absolute sm:relative left-4 sm:left-auto mr-2"></i>
          Upload file
        </button>
      </div>
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
    methods: {
      getFilename(url) {
        return url.substring(url.lastIndexOf('/') + 1);
      },
      upload() {
        console.log('test')
      }
    }
  }
</script>

<style scoped>

</style>
