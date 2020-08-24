<template>
  <div class="flex flex-column flex-wrap w-full pr-4">
    <div class="mt-3 w-full">
      <div class="text-center mb-8" v-if="comments.length === 0">
        <img alt="Nothing here" class="w-1/2 md:w-1/4 mx-auto mb-8"
             src="/static/img/svg/undraw_a_moment_to_relax_bbpa.svg">
        <span class="text-gray-600 text-lg md:text-xl">There are no messages here yet...</span>
      </div>
      <comment :comment="comment" :key="comment.id" :ticket="ticket" v-for="comment in comments"/>
    </div>

    <div class="flex w-full">
      <avatar :source="user.avatar_url" size="w-12 h-12 m-3"/>
      <div class="flex flex-col items-end flex-grow w-full mb-4">
        <card class="mb-2 w-full" outlined>
          <mention :ticket="ticket" :users="staff">
            <editor initialEditType="wysiwyg" previewStyle="tab" ref="commentEditor"/>
          </mention>
        </card>
        <button
                @click="submitComment"
                class="group relative w-full sm:w-auto flex justify-center sm:justify-start items-center py-2 px-4 border border-transparent text-sm leading-5 font-medium rounded-md text-white bg-primary hover:bg-orange-500 focus:outline-none focus:border-orange-700 focus:shadow-outline-orange active:bg-orange-700 transition duration-150 ease-in-out">
          <i class="fa fa-reply text-orange-200 absolute sm:relative left-4 sm:left-auto mr-2"></i>
          Comment
        </button>
      </div>
    </div>
  </div>
</template>

<script>
  import Comment from "./Comment";
  import Avatar from "../elements/Avatar";
  import axios from "axios";
  import '@toast-ui/editor/dist/toastui-editor-viewer.css';
  import 'codemirror/lib/codemirror.css';
  import VueTribute from 'vue-tribute';

  import '@toast-ui/editor/dist/toastui-editor.css';
  import {Editor, Viewer} from '@toast-ui/vue-editor';
  import Card from "../elements/card/Card";
  import Mention from "../elements/mention/Mention";
  import SubmitButton from "../elements/buttons/SubmitButton";

  export default {
    components: {
      SubmitButton,
      Mention,
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
      comments: {
        required: true,
        default: []
      },
      user: {
        type: Object,
        required: true
      },
      staff: {
        required: true,
        default: []
      }
    },
    data() {
      return {
        commentEditor: "",
      }
    },
    methods: {
      submitComment() {
        let content = this.$refs.commentEditor.invoke('getMarkdown');
        this.$refs.commentEditor.invoke('setMarkdown', '');

        let formData = new FormData();
        formData.append("content", content);

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

        axios.post("/api" + window.location.pathname + "/comments/post", formData)
            .then(() => {
              this.$emit("post", true)
            })
      },
    },
  }
</script>

<style scoped>

</style>
