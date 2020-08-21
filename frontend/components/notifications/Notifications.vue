<template>
  <div class="container divide-y divide-gray-100">
    <nav class="m-3">
      <div class="divide-x divide-gray-400 flex">
        <span @click="toggleAll" class="font-semibold text-center flex-grow" v-if="read === ''">All</span>
        <a @click="toggleAll" class="text-center flex-grow text-blue-500" v-else>All</a>

        <span @click="toggleRead" class="text-center font-semibold flex-grow" v-if="read === 'True'">Read</span>
        <a @click="toggleRead" class="text-center flex-grow text-blue-500" v-else>Read</a>

        <span @click="toggleUnread" class="text-center font-semibold flex-grow"
              v-if="read === 'False'">Unread</span>
        <a @click="toggleUnread" class="text-center flex-grow text-blue-500" v-else>Unread</a>

        <submit-button text="Mark all as read" v-on:click.native="markAllAsRead"
                       class="bg-orange-400 flex-wrap md:flex-wrap-0"></submit-button>
      </div>
    </nav>
    <notification-card v-for="notification in notifications.results" :key="notification.id"
                       :notification="notification"></notification-card>
    <div class="flex justify-end w-full">
      <submit-button v-on:click.native=prevPage() text="Prev" class="m-2"
                     v-if="notifications.previous"></submit-button>
      <span v-if="notifications.next || notifications.previous" class="m-3">{{pageNumber}}</span>
      <submit-button v-on:click.native=nextPage() text="Next" class="m-2"
                     v-if="notifications.next"></submit-button>
    </div>
  </div>
</template>

<script>
  import axios from "axios";
  import NotificationCard from "./NotificationCard";
  import SubmitButton from "../elements/buttons/SubmitButton";
  import SearchBar from "../elements/SearchBar";

  export default {
    name: "Notifications",
    components: {SearchBar, SubmitButton, NotificationCard},
    data() {
      return {
        notifications: [],
        read: "",
        pageNumber: 1
      }
    },
    created() {
      axios.get("/api/notifications").then(response => {
        this.notifications = response.data
      })
    },
    methods: {
      nextPage() {
        if (this.notifications.next) {
          axios.get(this.notifications.next.substr(this.notifications.next.indexOf("/", 7))).then(response => {
            this.notifications = response.data
            this.pageNumber += 1;
          })
        }
      },
      prevPage() {
        if (this.notifications.previous) {
          if (this.pageNumber === 2) {
            this.pageNumber = 1;
            this.getNotifications()
          } else if (this.pageNumber > 2) {
            axios.get(this.notifications.next.substr(this.notifications.next.indexOf("/", 7))).then(response => {
              this.notifications = response.data
              this.pageNumber -= 1;
            })
          }
        }
      },
      getNotifications() {
        axios.get("/api/notifications", {
          params: {
            read: this.read
          }
        }).then(response => {
          this.notifications = response.data
        })
      },
      toggleRead() {
        this.read = "True";
        this.getNotifications()
      },
      toggleUnread() {
        this.read = "False";
        this.getNotifications()
      },
      toggleAll() {
        this.read = "";
        this.getNotifications()
      },
      markAllAsRead() {
        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

        axios.put("/api/notifications/read/all").then(_ => {
          this.getNotifications()
        })
      }
    }
  }
</script>

<style scoped>

</style>