<template>
  <div class="flex flex-col text-center">
    <ul
      class="grid sm:grid-cols-2 xl:grid-cols-3 gap-4 mb-4"
      v-if="preview && this.files.length > 0"
    >
      <li
        :key="index"
        class="border border-gray-200 rounded-md pl-3 pr-4 py-3 flex items-center justify-between text-sm leading-5"
        v-for="(file, index) in this.files"
      >
        <div class="w-0 flex-1 flex items-center text-left">
          <DocumentAddIcon class="flex-shrink-0 h-5 w-5 text-gray-500" />
          <span class="ml-2 flex-1 w-0 truncate">
            {{ file.name }}
          </span>
        </div>
        <div class="ml-2 flex-shrink-0 flex items-center">
          <button
            @click="remove(files.indexOf(file))"
            class="font-medium text-orange-400 hover:text-orange-500 transition duration-150 ease-in-out"
            title="Remove file"
            type="button"
          >
            <XIcon class="h-5 w-5 text-gray-400" />
          </button>
        </div>
      </li>
    </ul>

    <div
      @dragleave="dragleave"
      @dragover="dragover"
      @drop="drop"
      class="bg-gray-50 text-gray-600 hover:text-gray-800 border border-dashed border-gray-300 hover:border-gray-400 rounded"
    >
      <input
        :accept="accepted"
        @change="onChange"
        class="w-px h-px hidden overflow-hidden absolute"
        id="attachment"
        multiple
        name="fields[attachment][]"
        ref="file"
        type="file"
      />

      <label class="inset-0 w-full h-16 cursor-pointer flex justify-center items-center" for="attachment">
        <div><span class="underline">Browse</span> or drop your files here</div>
      </label>
    </div>
  </div>
</template>

<script>
import { DocumentAddIcon } from '@heroicons/vue/outline'
import { XIcon } from '@heroicons/vue/solid'

export default {
  name: 'FileUpload',
  components: { DocumentAddIcon, XIcon },
  props: {
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
  data () {
    return {
      files: []
    }
  },
  methods: {
    onChange () {
      this.files.push(...this.$refs.file.files)
      this.$refs.file.value = ''

      this.$emit('input', this.files)
    },
    remove (i) {
      this.files.splice(i, 1)
    },
    dragover (event) {
      event.preventDefault()
      if (!event.currentTarget.classList.contains('bg-orange-300')) {
        event.currentTarget.classList.remove('bg-gray-100')
        event.currentTarget.classList.add('bg-orange-300')
      }
    },
    dragleave (event) {
      event.currentTarget.classList.add('bg-gray-100')
      event.currentTarget.classList.remove('bg-orange-300')
    },
    drop (event) {
      event.preventDefault()
      this.files.push(...event.dataTransfer.files)

      this.onChange()
      this.dragleave(event)
    },
    clear () {
      this.files = []
    }
  }
}
</script>
