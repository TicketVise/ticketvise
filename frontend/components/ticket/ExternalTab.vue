<template>
  <div class="flex flex-column flex-wrap w-full pr-4">
    <div class="mt-3 w-full">
      <comment :comment="ticket"/>
      <comment :comment="comment" :key="comment.id" :ticket="ticket" v-for="comment in replies"/>
    </div>

    <div class="flex w-full">
      <avatar :source="user.avatar_url" class="w-12 h-12 m-3"/>
      <div class="flex flex-col items-end flex-grow w-full mb-4">
        <card class="mb-2 w-full" outlined>
          <editor ref="replyEditor" />
        </card>
        <button @click="submitReply"
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
  import Editor from "../elements/markdown/Editor";
  import axios from "axios";

  export default {
    components: {
      Avatar,
      Comment,
      Editor,
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
        staff: [],
      }
    },
    methods: {
      submitReply() {
        let content = this.$refs.replyEditor.getContent()
        this.$refs.replyEditor.clear()

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

        axios.post("/api" + window.location.pathname + "/replies/post", {"content": content})
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
