<template>
  <div class="container mx-auto m-2">
    <card class="p-3">
      <h4 class="font-semibold text-gray-800 p-2">Title</h4>
      <error v-for="error in this.errors.title" :key="error" :message="error"></error>

      <card outlined>
        <input class="m-1" v-model="title" placeholder="Title">
      </card>

      <h4 class="font-semibold text-gray-800 m-2">Question</h4>
      <error v-for="error in this.errors.content" :key="error" :message="error"></error>
      <card outlined class="mb-2 w-full">
        <editor ref="editor" initialEditType="wysiwyg" previewStyle="tab"/>
      </card>

      <h4 class="font-semibold text-gray-800 m-2">Attachments</h4>
      <error v-for="error in this.errors.attachments" :key="error" :message="error"></error>

      <file-upload v-bind:value="files" v-on:input="setFiles"></file-upload>

      <h4 class="font-semibold text-gray-800 m-2">Labels</h4>
      <error v-for="error in this.errors.labels" :key="error" :message="error"></error>

      <div class="flex flex-wrap mb-2">
        <chip class="m-1" v-for="(label, index) in labels" :key="label.id" :background="label.color">
          {{ label.name }}
          <a class="fa fa-close" @click="removeLabel(index)"></a>
        </chip>
      </div>
      <div class=" mb-2">
        <label-dropdown v-bind:value="labels" :values="unused_labels" v-on:input="addLabel"/>
      </div>

      <div class="mb-3">
        <h4 class="font-semibold text-gray-800 m-2">Share with</h4>
        <error v-for="error in this.errors.username" :key="error" :message="error"></error>

        <div class="ml-2">
          <card class="my-2 md:w-1/5" outlined>
            <input class="m-1" v-model="username" placeholder="Username">
          </card>
          <submit-button v-on:click.native="username.length ? get_username(username) : {}" class="bg-green-200"
                         text="Add"></submit-button>
        </div>
      </div>

      <submit-button v-on:click.native="submit" text="Submit"></submit-button>

    </card>
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

export default {
  name: "Form",
  components: {Error, SubmitButton, FileUpload, EditLabel, LabelDropdown, Editor, Chip},
  data() {
    return {
      files: [],
      title: "",
      labels: [],
      inbox_labels: null,
      inbox_id: window.location.pathname.split('/')[2],
      errors: [],
      shared_with: [],
      username: ""
    }
  },
  mounted() {
    axios.get("/api/inboxes/" + this.inbox_id + "/labels").then(response => {
      this.inbox_labels = response.data;
    });
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
      this.shared_with.forEach(shared_with => formData.append("shared_with", shared_with))

      axios.defaults.xsrfCookieName = 'csrftoken';
      axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

      axios.post("/api" + window.location.pathname, formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
      ).then(() => {
        window.location.href = "/inboxes/" + this.inbox_id + "/tickets";
      }).catch(error => {
            this.errors = error.response.data
          }
      )
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
    get_username(username) {
      axios.get("/api/inboxes/" + this.inbox_id + "/users/" + username).then(response => {
        this.errors = []
        this.shared_with.push(response.data)
      }).catch(error => {
            this.errors = error.response.data
          }
      )
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