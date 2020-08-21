<template>
  <div class="flex flex-col h-full">
    <!-- Header -->
    <div class="border-b shadow flex justify-center">
      <div class="container px-4 mb-4 mt-2 xl:flex xl:items-center xl:justify-between" v-if="inbox">
        <div class="flex-1 min-w-0">
          <a :href="`/inboxes/${inbox.id}/tickets`" class="text-xs text-gray-700 hover:underline cursor-pointer">
            <i class="fa fa-arrow-left mr-2"></i>
            {{ inbox ? inbox.name : '' }}
          </a>
          <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:leading-9 sm:truncate">
            Create a new ticket
          </h2>
        </div>
      </div>
    </div>

    <div class="container mx-auto m-2 mb-4 px-4">
      <!-- Labels -->
      <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2" for="title">
          Title
        </label>
        <input
          class="appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none"
          id="title" type="text" placeholder="Give your question a title" name="title" v-model="title">
      </div>
      <error v-for="error in this.errors.title" :key="error" :message="error"></error>

      <!-- Question content -->
      <h4 class="block text-gray-700 font-bold mb-2">Question</h4>
      <card outlined class="mb-4 w-full">
        <editor ref="editor" initialEditType="wysiwyg" previewStyle="tab"/>
      </card>
      <error v-for="error in this.errors.content" :key="error" :message="error"></error>

      <!-- Labels -->
      <h4 class="block text-gray-700 font-bold mb-2">Labels</h4>
      <error v-for="error in this.errors.labels" :key="error" :message="error"></error>
      <div class="flex flex-wrap mb-2" v-if="labels.length > 0">
        <chip class="m-1" v-for="(label, index) in labels" :key="label.id" :background="label.color">
          {{ label.name }}
          <a class="fa fa-close" @click="removeLabel(index)"></a>
        </chip>
      </div>
      <div class="mb-4">
        <label-dropdown v-bind:value="labels" :values="unused_labels" v-on:input="addLabel"/>
      </div>

      <!-- Attachments -->
      <h4 class="block text-gray-700 font-bold mb-2">Attachments</h4>
      <file-upload v-bind:value="files" v-on:input="setFiles" class="mb-4"></file-upload>
      <error v-for="error in this.errors.attachments" :key="error" :message="error"></error>

      <!-- Share with -->
      <div class="mb-4">
        <edit-share-with :shared_with="shared_with" :errors="errors" class="mb-2 w-1/5" :inbox_id="inbox_id"
            v-on:input="updateSharedWith"></edit-share-with>
      </div>

      <submit-button v-on:click.native="submit" text="Submit" class="bg-primary hover:bg-orange-500 text-white">
        <i class="fa fa-paper-plane mr-2"></i>
      </submit-button>
    </div>
  </div>
</template>

<script>
import EditLabel from "./EditLabel";
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
  components: {EditShareWith, Error, SubmitButton, FileUpload, EditLabel, LabelDropdown, Editor, Chip},
  data() {
    return {
      inbox: null,
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
    axios.get("/api/inboxes/" + this.inbox_id + "/labels").then(response => {
      this.inbox_labels = response.data;
    })

    axios.get("/api/inboxes/" + this.inbox_id).then(response => {
      this.inbox = response.data
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
    addLabel(label) {
      this.labels.push(label)
    },
    removeLabel: function (index) {
      this.labels.splice(index, 1);
    },
    updateSharedWith: function (list) {
      this.shared_with = list
    }
  },
  computed: {
    unused_labels: function () {
      if (!this.inbox_labels) {
        return []
      }

      const label_ids = this.labels.map(label => label.id)
      return this.inbox_labels.filter(label => !label_ids.includes(label.id))
    }
  }

}

</script>

<style scoped>

</style>
