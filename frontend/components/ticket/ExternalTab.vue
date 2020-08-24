<template>
  <div class="flex flex-column flex-wrap w-full pr-4">
    <div class="mt-3 w-full">
      <comment :comment="ticket"/>
      <comment v-for="comment in replies" :key="comment.id" :comment="comment" :ticket="ticket"/>
    </div>

    <div class="flex w-full">
      <avatar :source="user.avatar_url" size="w-12 h-12 m-3"/>
      <div class="flex flex-col items-end flex-grow w-full mb-4">
        <card outlined class="mb-4 w-full">
          <editor ref="replyEditor" initialEditType="wysiwyg" previewStyle="tab"/>
        </card>
        <button
                @click="submitReply"
                class="group relative w-full sm:w-auto flex justify-center sm:justify-start items-center py-2 px-4 border border-transparent text-sm leading-5 font-medium rounded-md text-white bg-primary hover:bg-orange-500 focus:outline-none focus:border-orange-700 focus:shadow-outline-orange active:bg-orange-700 transition duration-150 ease-in-out">
          <i class="fa fa-reply text-orange-200 absolute sm:relative left-4 sm:left-auto mr-2"></i>
          {{ button_text }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
  import Comment from "./Comment";
  import Avatar from "../elements/Avatar";
  import Card from "../elements/card/Card";
  import axios from "axios";
  import '@toast-ui/editor/dist/toastui-editor-viewer.css';
  import 'codemirror/lib/codemirror.css';
  import VueTribute from 'vue-tribute';

  import '@toast-ui/editor/dist/toastui-editor.css';
  import {Editor, Viewer} from '@toast-ui/vue-editor';
  import SubmitButton from "../elements/buttons/SubmitButton";

  export default {
    components: {
      SubmitButton,
      Avatar,
      Comment,
      Viewer,
      editor: Editor,
      VueTribute,
      Card
    },
    props: {
      ticket: {
        type: Object,
        required: true
      },
      replies: {
        required: true,
        default: []
      },
      user: {
        type: Object,
        required: true
      }
    },
    data() {
      return {
        replyEditor: "",
        staff: [],
      }
    },
    methods: {
      submitReply() {
        let content = this.$refs.replyEditor.invoke('getMarkdown');
        this.$refs.replyEditor.invoke('setMarkdown', '');
        let formData = new FormData();
        formData.append("content", content);

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

        axios.post("/api" + window.location.pathname + "/replies/post", formData)
            .then(() => {
              this.$emit("post", true)
            })
      }
    },
    computed: {
      button_text: function () {
        if (this.ticket.status === "CLSD") {
          return "Reply and reopen ticket"
        } else {
          return "Reply"
        }
      }
    }

  }
</script>

<style scoped>

</style>
