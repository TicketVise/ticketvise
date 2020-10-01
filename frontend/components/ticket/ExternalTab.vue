<template>
  <div class="flex flex-column flex-wrap w-full pr-4">
    <div class="mt-3 w-full">
      <comment :comment="ticket"/>
      <div v-for="entry in content">
        <comment v-if="entry.content" :comment="entry" :key="`comment-${entry.id}`" :ticket="ticket"/>
        <ticket-event v-else :event="entry" :key="`event-${entry.id}`" />
      </div>
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
  import TicketEvent from "./TicketEvent";
  import moment from "moment";

  export default {
    components: {
      TicketEvent,
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
      events: {
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
      },
      content: function () {
        const mergeMinutes = 5
        const entries = []
        const tempEntries = this.replies.concat(this.events).concat(this.ticket.attachments)
        tempEntries.sort((a, b) => moment(a.date_created).diff(moment(b.date_created)))

        for (let entry of tempEntries) {
          if (entries.length > 0) {
            const top = entries[entries.length - 1]

            const timeDiffMinutes = moment(entry.date_created).diff(moment(top.date_created), "m")

            console.log(timeDiffMinutes)
            // merge label events
            if (entry.hasOwnProperty("label")) {
              if (top.hasOwnProperty("labels")
                  && timeDiffMinutes <= mergeMinutes
                  && top.is_added === entry.is_added
                  && JSON.stringify(entry.initiator) === JSON.stringify(top.initiator)) {
                top.labels.push(entry.label)
              } else {
                entry.labels = [entry.label]
                entries.push(entry)
              }
            } else if (entry.hasOwnProperty("file")) {
              if (top.hasOwnProperty("attachments")
                  && timeDiffMinutes <= mergeMinutes
                  && JSON.stringify(entry.uploader) === JSON.stringify(top.uploader)) {
                top.attachments.push(entry)
              } else {
                entry.attachments = [{...entry}]
                entries.push(entry)
              }
            } else {
              entries.push(entry)
            }

          } else {
            entries.push(entry)
          }
        }

        return entries
      }
    }

  }
</script>

<style scoped>

</style>
