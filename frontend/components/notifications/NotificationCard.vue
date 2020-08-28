<template>
  <a :href="`/inboxes/${notification.inbox.id}/tickets/${notification.ticket.ticket_inbox_id}`" class="border rounded w-full p-2" :class="{ 'text-gray-900': !notification.is_read, 'text-gray-400': notification.is_read }">
    <!-- Link to inbox -->
    <div class="flex justify-between">
      <span class="flex flex-1 space-x-1 items-center">
        <span class="relative h-2 w-2 rounded-full mb-1" :style="`background-color: ${notification.inbox.color};`"></span>
        <a class="text-xs hover:underline" :href="`/inboxes/${notification.inbox.id}/tickets`">{{ notification.inbox.name }}</a>
      </span>
      <button @click="flipRead()" class="text-xs fa focus:outline-none" :class="{ 'fa-envelope': !notification.is_read, 'fa-envelope-open-o': notification.is_read }"></button>
    </div>
    <div class="leading-4 font-bold">{{ notification.content }}</div>
    <div class="text-sm">#{{ notification.ticket.ticket_inbox_id }} - {{ notification.ticket.title }}</div>
    <div class="text-sm">
      <i class="fa fa-calendar text-xs"></i>
      {{ date }}
    </div>
    <!-- <avatar :source="notification.receiver.avatar_url" class="h-12 m-2"></avatar>
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
    </div> -->
  </a>
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
