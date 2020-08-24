<template>
  <div>
    <!-- Header -->
    <div class="border-b shadow flex justify-center">
      <div class="container px-4 my-4 xl:flex xl:items-center xl:justify-between">
        <div class="flex-1 min-w-0">
          <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:leading-9 sm:truncate">
            <span class="font-semibold" v-if="this.count">{{ this.count }}</span> Notifications
          </h2>
        </div>
      </div>
    </div>
    <div class="container mx-auto divide-y divide-gray-100">
      <nav class="m-3">
        <div class="divide-x divide-gray-400 flex items-center">
          <span @click="toggleAll" class="font-semibold text-center flex-grow cursor-pointer"
                v-if="is_read === ''">All</span>
          <a @click="toggleAll" class="text-center flex-grow text-blue-500 cursor-pointer" v-else>All</a>

          <span @click="toggleRead" class="text-center font-semibold flex-grow cursor-pointer" v-if="is_read === 'True'">Read</span>
          <a @click="toggleRead" class="text-center flex-grow text-blue-500 cursor-pointer" v-else>Read</a>

          <span @click="toggleUnread" class="text-center font-semibold flex-grow cursor-pointer"
                v-if="is_read === 'False'">Unread</span>
          <a @click="toggleUnread" class="text-center flex-grow text-blue-500 cursor-pointer" v-else>Unread</a>

          <submit-button text="Mark all as read" v-on:click.native="markAllAsRead"
                         class="bg-primary text-white border-none hover:bg-orange-500 flex-wrap md:flex-wrap-0"></submit-button>
        </div>
      </nav>

      <notification-card v-for="notification in notifications.results" :key="notification.id"
                         :notification="notification" v-on:input="getNotificationCount"></notification-card>

      <div class="flex justify-center w-full">
        <submit-button v-on:click.native=prevPage() text="Prev" class="m-2"
                       v-if="notifications.previous"></submit-button>
        <span v-if="notifications.next || notifications.previous" class="m-3">{{pageNumber}}</span>
        <submit-button v-on:click.native=nextPage() text="Next" class="m-2"
                       v-if="notifications.next"></submit-button>
      </div>
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
        is_read: "",
        pageNumber: 1,
        count: 0
      }
    },
    created() {
      axios.get("/api/notifications").then(response => {
        this.notifications = response.data;
        this.getNotificationCount()
      })
    },
    methods: {
      nextPage() {
        if (this.notifications.next) {
          axios.get(this.notifications.next.substr(this.notifications.next.indexOf("/", 7))).then(response => {
            this.notifications = response.data;
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
            axios.get(this.notifications.previous.substr(this.notifications.previous.indexOf("/", 7))).then(response => {
              this.notifications = response.data;
              this.pageNumber -= 1;
            })
          }
        }
      },
      getNotifications() {
        axios.get("/api/notifications", {
          params: {
            is_read: this.is_read
          }
        }).then(response => {
          this.notifications = response.data
          this.getNotificationCount()
        })
      },
      getNotificationCount() {
        axios.get("/api/notifications/unread").then(response => {
          this.count = response.data
        })
      },
      toggleRead() {
        this.is_read = "True";
        this.getNotifications()
      },
      toggleUnread() {
        this.is_read = "False";
        this.getNotifications()
      },
      toggleAll() {
        this.is_read = "";
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