<template>
    <div class="flex text-center">
        <div class="p-6 bg-gray-100 border border-dashed border-gray-300" @dragover="dragover" @dragleave="dragleave" @drop="drop">
            <input type="file" multiple name="fields[attachment][]" id="attachment"
                   class="w-px h-px opacity-0 overflow-hidden absolute" @change="onChange" ref="file"
                   :accept="accepted"/>

            <label for="attachment" class="block cursor-pointer">
                <div>
                    <span class="underline">Browse</span> or drop your files here
                </div>
            </label>
            <ul class="mt-4" v-if="this.files.length" v-cloak>
                <li class="text-sm p-1" v-for="file in files">
                    {{file.name}}
                    <button type="button" @click="remove(files.indexOf(file))" title="Remove file">x</button>
                </li>
            </ul>
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
                this.files = [...this.$refs.file.files];
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
                this.$refs.file.files = event.dataTransfer.files;
                this.onChange();
                this.dragleave(event)
            }
        }
    }
</script>

<style scoped>

</style>