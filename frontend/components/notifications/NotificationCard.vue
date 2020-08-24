<template>
  <div class="flex w-full my-1">
    <avatar :source="notification.receiver.avatar_url" class="h-12 m-2"></avatar>
    <div :style="borderColor" class="flex-grow m-2 pl-2 border-l-4">
      <div class="flex-row" v-if="notification.is_read">
        <a :href="ticketUrl">{{ notification.ticket.title }}</a> <span class="text-sm">{{ notification.author }} - <span
              class="whitespace-no-wrap">{{ date }}</span></span>
      </div>
      <div class="flex-row font-semibold" v-else>
        <a :href="ticketUrl">{{ notification.ticket.title }}</a> <span class="text-sm">{{ notification.author }} - <span
              class="whitespace-no-wrap">{{ date }}</span></span>
      </div>
      <div class="flex-row">
        {{ notification.content }}
      </div>
    </div>
    <div class="py-2">
      <button @click="flipRead()" class="fa fa-envelope" v-if="!notification.is_read"></button>
      <button @click="flipRead()" class="fa fa-envelope-open-o" v-if="notification.is_read"></button>
    </div>
  </div>
</template>

<script>
  import Avatar from "../elements/Avatar";
  import moment from "moment"
  import axios from "axios"

  export default {
    name: "NotificationCard",
    components: {Avatar},
    props: {notification: {type: Object, default: null, required: true}},
    computed: {
      date: function () {
        return moment.parseZone(this.notification.date_created).fromNow()
      },
      borderColor() {
        return {
          "border-color": this.notification.inbox.color
        }
      },
      ticketUrl() {
        return `/inboxes/${this.notification.inbox.id}/tickets/${this.notification.ticket.ticket_inbox_id}`
      }
    },
    methods: {
      flipRead() {
        let formData = new FormData;
        formData.append("is_read", this.notification.is_read ? "False" : "True");

                axios.defaults.xsrfCookieName = "csrftoken";
                axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

                axios.put("/api/notifications/" + this.notification.id + "/read", formData).then(response => {
                    this.notification.is_read = response.data.is_read
                    this.$emit("input")
                })
            }
        }
    }
</script>

<style scoped>

</style>