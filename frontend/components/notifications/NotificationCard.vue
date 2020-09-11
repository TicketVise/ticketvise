<template>
  <div class="border rounded w-full p-2" :class="{ 'text-gray-900': !read, 'text-gray-400': read }">
    <!-- Link to inbox -->
    <div class="flex justify-between">
      <span class="flex flex-1 space-x-1 items-center">
        <span class="relative h-2 w-2 rounded-full mb-1" :style="`background-color: ${notification.inbox.color};`"></span>
        <a class="text-xs hover:underline" :href="`/inboxes/${notification.inbox.id}/tickets`">{{ notification.inbox.name }}</a>
      </span>
      <button @click="flipRead()" class="text-xs fa focus:outline-none" :class="{ 'fa-envelope': !read, 'fa-envelope-open-o': read }"></button>
    </div>
    <a :href="`/inboxes/${notification.inbox.id}/tickets/${notification.ticket.ticket_inbox_id}`" class="leading-4 font-bold hover:underline">{{ notification.content }}</a>
    <div class="text-sm">#{{ notification.ticket.ticket_inbox_id }} - {{ notification.ticket.title }}</div>
    <div class="text-sm">
      <i class="fa fa-calendar text-xs"></i>
      {{ date }}
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
    data: () => ({
      read: false
    }),
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
    mounted() {
      this.read = this.notification.is_read
    },
    methods: {
      flipRead() {
        let formData = new FormData;
        formData.append("is_read", this.notification.is_read ? "False" : "True");

        axios.defaults.xsrfCookieName = "csrftoken";
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

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
