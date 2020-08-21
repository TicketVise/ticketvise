<template>
    <div class="flex flex-col text-center">
        <ul v-if="this.files.length > 0" class="grid sm:grid-cols-2 xl:grid-cols-3 gap-4 mb-4">
            <li class="border border-gray-200 rounded-md pl-3 pr-4 py-3 flex items-center justify-between text-sm leading-5"
                v-for="(file, index) in this.files" :key="index">
                <div class="w-0 flex-1 flex items-center">
                    <svg class="flex-shrink-0 h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd"
                            d="M8 4a3 3 0 00-3 3v4a5 5 0 0010 0V7a1 1 0 112 0v4a7 7 0 11-14 0V7a5 5 0 0110 0v4a3 3 0 11-6 0V7a1 1 0 012 0v4a1 1 0 102 0V7a3 3 0 00-3-3z"
                            clip-rule="evenodd"/>
                    </svg>
                    <span class="ml-2 flex-1 w-0 truncate">
                        {{ file.name }}
                    </span>
                </div>
                <div class="ml-4 flex-shrink-0">
                    <button
                        type="button"
                        @click="remove(files.indexOf(file))"
                        title="Remove file"
                        class="font-medium text-orange-400 hover:text-orange-500 transition duration-150 ease-in-out"
                    >x</button>
                </div>
            </li>
        </ul>

        <div class="p-6 bg-gray-100 border border-dashed border-gray-300 max-w-screen-sm" @dragover="dragover" @dragleave="dragleave" @drop="drop">
            <input type="file" multiple name="fields[attachment][]" id="attachment"
                   class="w-px h-px opacity-0 overflow-hidden absolute" @change="onChange" ref="file"
                   :accept="accepted"/>

            <label for="attachment" class="block cursor-pointer">
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
        props: ["value", "accepted"],
        data() {
            return {
                files: []
            }
        },
        methods: {
            onChange() {
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

                // this.$refs.file.files.push(...event.dataTransfer.files);
                this.onChange();
                this.dragleave(event)
            }
        }
    }
</script>
