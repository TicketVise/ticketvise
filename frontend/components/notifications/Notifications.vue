<template>
  <div>
    <!-- Header -->
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto p-4 py-2 sm:flex sm:items-center sm:justify-between">
        <div class="flex-1 min-w-0">
          <a href="/inboxes" class="text-xs text-gray-700 hover:underline cursor-pointer">
            <i class="fa fa-arrow-left mr-2"></i>
            Dashboard
          </a>
          <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:leading-9 sm:truncate">
            Notifications
          </h2>
        </div>
        <div class="mt-2 flex xl:mt-0 xl:ml-4 space-x-4">
          <span class="shadow-sm rounded-md">
            <button v-on:click="markAllAsRead"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm leading-5 font-medium rounded-md text-white bg-primary hover:bg-orange-500 focus:outline-none focus:shadow-outline-orange focus:border-orange-700 active:bg-orange-700 transition duration-150 ease-in-out">
              Mark all as read
            </button>
          </span>
        </div>
      </div>
      <div class="container max-w-7xl mx-auto overflow-x-auto xl:px-4">
        <ul class="flex border-b" v-if="notifications.results">
          <tab :active="is_read == 'False'" @click="is_read = 'False'" title="Unread"
            :badge="count"/>
          <tab :active="is_read == 'True'" @click="is_read = 'True'" title="Read"/>
          <tab :active="is_read == ''" @click="is_read = ''" title="All"/>
        </ul>
      </div>
    </header>

    <div class="container mx-auto p-4 flex flex-col space-y-2">
      <div v-if="!notifications.results" class="text-center py-8">
        <img src="/static/img/svg/undraw_complete_task_u2c3.svg" alt="Nothing here" class="w-1/2 md:w-1/4 mx-auto mb-8">
        <span class="text-gray-600 text-lg md:text-xl">You have no notifications</span>
      </div>

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

  export default {
    name: "Notifications",
    data() {
      return {
        notifications: [],
        is_read: "False",
        pageNumber: 1,
        count: 0
      }
    },
    watch: {
      is_read: function() {
        this.getNotifications()
      }
    },
    created() {
      axios.get("/api/notifications", {
        params: {
          is_read: this.is_read
        }
      }).then(response => {
        this.notifications = response.data;
        this.getNotificationCount()
        console.log(this.notifications)
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
