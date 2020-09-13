<template>
  <div class="flex flex-col text-center">
    <ul class="grid sm:grid-cols-2 xl:grid-cols-3 gap-4 mb-4" v-if="preview && this.files.length > 0">
      <li :key="index"
          class="border border-gray-200 rounded-md pl-3 pr-4 py-3 flex items-center justify-between text-sm leading-5" v-for="(file, index) in this.files">
        <div class="w-0 flex-1 flex items-center text-left">
          <svg class="flex-shrink-0 h-5 w-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
            <path clip-rule="evenodd"
                  d="M8 4a3 3 0 00-3 3v4a5 5 0 0010 0V7a1 1 0 112 0v4a7 7 0 11-14 0V7a5 5 0 0110 0v4a3 3 0 11-6 0V7a1 1 0 012 0v4a1 1 0 102 0V7a3 3 0 00-3-3z"
                  fill-rule="evenodd"/>
          </svg>
          <span class="ml-2 flex-1 w-0 truncate">
            {{ file.name }}
          </span>
        </div>
        <div class="ml-4 flex-shrink-0">
          <button
                  @click="remove(files.indexOf(file))"
                  class="font-medium text-orange-400 hover:text-orange-500 transition duration-150 ease-in-out"
                  title="Remove file"
                  type="button"
          >x
          </button>
        </div>
      </li>
    </ul>

    <div @dragleave="dragleave" @dragover="dragover" @drop="drop"
         class="p-6 bg-gray-100 border border-dashed border-gray-300 rounded">
      <input :accept="accepted" @change="onChange" class="w-px h-px opacity-0 overflow-hidden absolute" id="attachment"
             multiple name="fields[attachment][]" ref="file" type="file"/>

      <label class="block cursor-pointer" for="attachment">
        <div>
          <span class="underline">Browse</span> or drop your files here
        </div>
      </label>
    </div>
  </div>
</template>

<script>
  export default {
    name: "FileUpload",
    props: {
      value: {
        type: Array,
        required: true
      },
      accepted: {
        type: String,
        required: false,
        default: ''
      },
      preview: {
        type: Boolean,
        required: false,
        default: true
      }
    },
    data() {
      return {
        files: []
      }
    },
    methods: {
      onChange() {
        this.files.push(...this.$refs.file.files)
        this.$refs.file.value = ""

        this.$emit('input', this.files)
      },
      remove(i) {
        this.files.splice(i, 1);
      },
      dragover(event) {
        event.preventDefault();
        if (!event.currentTarget.classList.contains('bg-orange-300')) {
          event.currentTarget.classList.remove('bg-gray-100');
          event.currentTarget.classList.add('bg-orange-300');
        }
      },
      dragleave(event) {
        event.currentTarget.classList.add('bg-gray-100');
        event.currentTarget.classList.remove('bg-orange-300');
      },
      drop(event) {
        event.preventDefault();
        this.files.push(...event.dataTransfer.files)

        this.onChange();
        this.dragleave(event)
      }
    }
  }
</script>
