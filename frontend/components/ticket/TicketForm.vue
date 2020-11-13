<template>
  <div class="flex flex-col">
    <div class="container mx-auto m-2 mb-4 px-4">
      <h2 class="text-xl font-bold leading-7 text-gray-900 sm:text-3xl sm:leading-9 sm:truncate mb-4">
        Create a new ticket
      </h2>
      <!-- Labels -->
      <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2" for="title">
          Title
        </label>
        <error class="mb-2" v-for="error in this.errors.title" :key="error" :message="error"></error>
        <input
          class="appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none"
          id="title"
          name="title"
          placeholder="Give your question a title"
          type="text"
          v-model="title"
        >
      </div>

      <!-- Question content -->
      <h4 class="block text-gray-700 font-bold mb-2">Question</h4>
      <error class="mb-2" v-for="error in this.errors.content" :key="error" :message="error"></error>
      <card outlined class="mb-4 w-full">
        <editor ref="editor" initialEditType="wysiwyg" previewStyle="tab"/>
      </card>

      <!-- Labels -->
      <h4 class="block text-gray-700 font-bold mb-2">Labels</h4>
      <error class="mb-2" v-for="error in this.errors.labels" :key="error" :message="error"></error>
      <div class="flex flex-wrap mb-2" v-if="labels.length > 0">
        <chip :background="label.color" :key="label.id" class="m-1" v-for="label in labels">
          {{ label.name }}
        </chip>
      </div>
      <div class="flex flex-wrap mb-2" v-else>
        No labels selected
      </div>
      <div class="mb-4">
        <label-dropdown :values="inbox_labels" v-model="labels"/>
      </div>

      <!-- Share with -->
      <div class="mb-4">
        <edit-share-with :shared_with="shared_with" :errors="errors" class="mb-2 w-1/5" :inbox_id="inbox_id"
                         v-on:input="updateSharedWith"></edit-share-with>
      </div>

      <!-- Attachments -->
      <h4 class="block text-gray-700 font-bold mb-2">Attachments</h4>
      <error class="mb-2" v-for="error in this.errors.attachments" :key="error" :message="error"></error>
      <file-upload v-bind:value="files" v-on:input="setFiles" class="mb-4"></file-upload>

      <submit-button v-on:click.native="submit" text="Submit" class="bg-primary hover:bg-orange-500 text-white">
        <i class="fa fa-paper-plane mr-2"></i>
      </submit-button>
    </div>
  </div>
</template>

<script>
  import Chip from "../elements/chip/Chip";
  import LabelDropdown from "../elements/dropdown/LabelDropdown";
  import axios from "axios";
  import {Editor} from "@toast-ui/vue-editor";
  import FileUpload from "../elements/FileUpload";
  import SubmitButton from "../elements/buttons/SubmitButton";
  import Error from "../elements/message/Error";
  import EditShareWith from "./EditShareWith";

  export default {
    name: "Form",
    components: {EditShareWith, Error, SubmitButton, FileUpload, LabelDropdown, Editor, Chip},
    data() {
      return {
        files: [],
        title: "",
        labels: [],
        inbox_labels: null,
        inbox_id: window.location.pathname.split('/')[2],
        errors: [],
        shared_with: [],
      }
    },
    mounted() {
      axios.get("/api/inboxes/" + this.inbox_id + "/labels/all").then(response => {
        this.inbox_labels = response.data;
      })
    },
    methods: {
      submit() {
        let content = this.$refs.editor.invoke('getMarkdown');
        let formData = new FormData();

        formData.append("content", content);
        formData.append("title", this.title);
        formData.append("inbox", this.inbox_id);

        this.labels.forEach(label => formData.append("labels", label.id))
        this.files.forEach(file => formData.append("files", file))
        this.shared_with.forEach(shared_with => formData.append("shared_with", shared_with.id))

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

        axios.post("/api" + window.location.pathname, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }).then(() => {
          window.location.href = "/inboxes/" + this.inbox_id + "/tickets";
        }).catch(error => {
          this.errors = error.response.data
        })
      },
      setFiles(files) {
        this.files = files
      },
      updateSharedWith: function (list) {
        this.shared_with = list
      }
    },
  }

</script>

<style scoped>

</style>
