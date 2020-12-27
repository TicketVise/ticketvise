<template>
  <div class="border rounded w-full p-2" :class="{ 'text-gray-900': !read, 'text-gray-400': read }">
    <!-- Link to inbox -->
    <div class="flex justify-between">
      <span class="flex flex-1 space-x-1 items-center">
        <span class="relative h-2 w-2 rounded-full" :style="`background-color: ${notification.inbox.color};`"></span>
        <router-link class="text-xs hover:underline" :to="`/inboxes/${notification.inbox.id}/tickets`">{{ notification.inbox.name }}</router-link>
      </span>
      <button @click="flipRead()" class="text-xs fa focus:outline-none" :class="{ 'fa-envelope': !read, 'fa-envelope-open-o': read }"></button>
    </div>
    <router-link :to="`/inboxes/${notification.inbox.id}/tickets/${notification.ticket.ticket_inbox_id}`" class="leading-4 font-bold hover:underline">{{ notification.content }}</router-link>
    <div class="text-sm">#{{ notification.ticket.ticket_inbox_id }} - {{ notification.ticket.title }}</div>
    <div class="text-sm">
      <i class="fa fa-calendar text-xs"></i>
      {{ date(this.notification.date_created) }}
    </div>
  </div>
</template>

<script>
  import Avatar from "../elements/Avatar";
  import axios from "axios"
  import {calendarDate} from "../../utils";

  export default {
    name: "NotificationCard",
    components: {Avatar},
    data: () => ({
      read: false
    }),
    props: {notification: {type: Object, default: null, required: true}},
    computed: {
      borderColor() {
        return {
          "border-color": this.notification.inbox.color
        }
      },
      ticketUrl() {
        return `/inboxes/${this.notification.inbox.id}/tickets/${this.notification.ticket.ticket_inbox_id}`
      }
    },
    mounted() {
      this.read = this.notification.is_read
    },
    methods: {
      date: calendarDate,
      flipRead() {
        let formData = new FormData;
        formData.append("is_read", this.notification.is_read ? "False" : "True");

        axios.put("/api/notifications/" + this.notification.id + "/read", formData).then(response => {
          Vue.set(this.notification, 'is_read', response.data.is_read)
          this.read = !this.read
          this.$emit("input")
        })
      }
    }
  }
</script>

<style scoped>

</style>
