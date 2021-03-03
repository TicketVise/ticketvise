<template>
  <div>
    <publish-confirmation @click="submitReplyPublish" @cancel="publishConfirmationModal = false"
                          v-if="publishConfirmationModal"></publish-confirmation>
    <div class="flex flex-column flex-wrap w-full pr-4">
      <div class="mt-3 w-full">
        <comment :comment="ticket"/>
        <div v-for="entry in content" :key="entry.id">
          <comment v-if="entry.content" :comment="entry" :key="`comment-${entry.id}`" :ticket="ticket"/>
          <ticket-event v-else :ticket_event="entry" :key="`event-${entry.id}`"/>
        </div>
      </div>

      <div class="flex w-full">
        <avatar :source="user.avatar_url" class="w-12 h-12 m-3"/>
        <div class="flex flex-col items-end flex-grow w-full mb-4">
          <card class="mb-2 w-full" outlined>
            <editor ref="replyEditor"/>
          </card>
          <div class="flex content-between space-x-2">
            <button @click="submitReply"
                    class="group relative w-full sm:w-auto flex justify-center sm:justify-start items-center py-2 px-4 border border-transparent text-sm leading-5 font-medium rounded-md text-white bg-primary hover:bg-orange-500 focus:outline-none focus:border-orange-700 focus:shadow-outline-orange active:bg-orange-700 transition duration-150 ease-in-out">
              <i class="fa fa-reply text-orange-200 absolute sm:relative left-4 sm:left-auto mr-2"></i>
              {{ button_text }}
            </button>
            <button @click="publishConfirmationModal = true"
                    v-if="is_staff && !ticket.publish_requested && !ticket.is_public"
                    class="group relative w-full sm:w-auto flex justify-center sm:justify-start items-center py-2 px-4 border border-transparent text-sm leading-5 font-medium rounded-md text-white bg-primary hover:bg-orange-500 focus:outline-none focus:border-orange-700 focus:shadow-outline-orange active:bg-orange-700 transition duration-150 ease-in-out">
              <i class="fa fa-reply text-orange-200 absolute sm:relative left-4 sm:left-auto mr-2"></i>
              Reply and Publish
            </button>
          </div>
        </div>
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
  import PublishConfirmation from "./PublishConfirmation";

  export default {
    components: {
      PublishConfirmation,
      TicketEvent,
      Avatar,
      Comment,
      Editor,
      Card
    },
    props: {
      is_staff: {
        type: Boolean,
        required: false,
        default: false
      },
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
        publishConfirmationModal: false,
      }
    },
    methods: {
      submitReply() {
        const inboxId = this.$route.params.inboxId
        const ticketInboxId = this.$route.params.ticketInboxId
        const content = this.$refs.replyEditor.getContent()

        this.$refs.replyEditor.clear()

        axios.post(`/api/inboxes/${inboxId}/tickets/${ticketInboxId}/replies/post`, {"content": content})
            .then(() => {
              this.$emit("post", true)
            }).catch(response => {
          return response
        })
      },
      submitReplyPublish() {
        if (!this.submitReply()) {
          // only request publish if no error is returned
          const inboxId = this.$route.params.inboxId
          const ticketInboxId = this.$route.params.ticketInboxId

          this.publishConfirmationModal = false
          axios.put(`/api/inboxes/${inboxId}/tickets/${ticketInboxId}/request-publish`,
              {"publish_requested": true}).then(
              response => this.ticket.publish_requested = response.data
          )
        }
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
        const sharedWith = this.ticket.shared_with_by.map(shared_user => {
          shared_user.shared_with = shared_user.user

          return shared_user
        })

        const tempEntries = this.replies.concat(this.events).concat(this.ticket.attachments).concat(sharedWith);

        tempEntries.sort((a, b) => moment(a.date_created).diff(moment(b.date_created)))


        for (let entry of tempEntries) {
          if (entries.length > 0) {
            const top = entries[entries.length - 1]

            const timeDiffMinutes = moment(entry.date_created).diff(moment(top.date_created), "m")

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
            } else if (entry.hasOwnProperty("shared_with")) {
              if (top.hasOwnProperty("shared_with_users")
                  && timeDiffMinutes <= mergeMinutes
                  && JSON.stringify(entry.sharer) === JSON.stringify(top.sharer)) {
                top.shared_with_users.push(entry.shared_with)
              } else {
                entry.shared_with_users = [entry.shared_with]
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
