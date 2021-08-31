<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:max-w-7xl lg:px-8">
    <h1 class="sr-only">Profile</h1>
    <div class="grid grid-cols-1 gap-4 items-start">
      <section aria-labelledby="profile-overview-title">
        <div class="rounded-lg bg-white overflow-hidden shadow">
          <h2 class="sr-only" id="profile-overview-title">Profile Overview</h2>
          <div class="bg-white p-6">
            <div class="sm:flex sm:items-center sm:justify-between">
              <div class="sm:flex sm:space-x-5">
                <div class="mt-4 text-center sm:mt-0 sm:pt-1 sm:text-left">
                  <p class="text-xl font-bold text-gray-900 sm:text-2xl">Your Notifications</p>
                </div>
              </div>
              <div class="mt-5 flex justify-center sm:mt-0">
                <button @click="markAllAsRead" class="flex justify-center items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                  Mark all as read
                </button>
              </div>
            </div>
          </div>

          <div class="border-t">
            <nav class="relative z-0 rounded-lg flex divide-x divide-gray-200" aria-label="Tabs">
              <button v-for="(tab, tabIdx) in tabs" :key="tab.name" @click="tabs.forEach(t => t.current = false); tab.current = true; is_read = tab.is_read" :class="[tab.current ? 'text-gray-900' : 'text-gray-500 hover:text-gray-700', tabIdx === 0 ? 'rounded-l-lg' : '', tabIdx === tabs.length - 1 ? 'rounded-r-lg' : '', 'group relative min-w-0 flex-1 overflow-hidden bg-white py-4 px-4 text-sm font-medium text-center hover:bg-gray-50 focus:z-10']" :aria-current="tab.current ? 'page' : undefined">
                <span>
                  {{ tab.name }}
                  <span v-if="tab.count" :class="[tab.current ? 'bg-primary-100 text-primary-600' : 'bg-gray-100 text-gray-900', 'hidden ml-3 py-0.5 px-2.5 rounded-full text-xs font-medium md:inline-block']">{{ tab.count }}</span>
                </span>
                <span aria-hidden="true" :class="[tab.current ? 'bg-primary' : 'bg-transparent', 'absolute inset-x-0 bottom-0 h-0.5']" />
              </button>
            </nav>
          </div>
        </div>
      </section>

      <div class="flow-root mt-6">
        <div v-if="notifications.results && notifications.results.length == 0" class="text-center py-8">
          <img :src="completeTask" alt="Nothing here" class="w-1/2 md:w-1/4 mx-auto mb-8">
          <span class="text-gray-600 text-lg md:text-xl">You have no notifications</span>
        </div>

        <ul role="list" class="-mt-5 divide-y divide-gray-200">
          <li v-for="notification in notifications.results" :key="notification.id" class="relative py-4">
            <div class="flex justify-between space-x-3">
              <div class="min-w-0 flex-1">
                <router-link :to="`/inboxes/${notification.inbox.id}/tickets/${notification.ticket.ticket_inbox_id}`" class="block focus:outline-none">
                  <span class="absolute inset-0" aria-hidden="true" />
                  <p class="text-sm font-medium truncate" :class="notification.is_read ? 'text-gray-400' : 'text-gray-900'">{{ notification.content }}</p>
                  <p class="text-xs" :class="notification.is_read ? 'text-gray-300' : 'text-gray-600'">{{ notification.inbox.name }}</p>
                  <p class="text-sm truncate" :class="notification.is_read ? 'text-gray-300' : 'text-gray-500'">{{ notification.ticket.title }}</p>
                </router-link>
              </div>
              <time :datetime="notification.date_created" class="flex-shrink-0 whitespace-nowrap text-sm text-gray-500">{{ date(notification.date_created) }}</time>
            </div>
          </li>
        </ul>

        <nav v-show="notifications.next || notifications.previous" class="border-t border-gray-200 px-4 flex items-center justify-between sm:px-0">
          <div class="-mt-px w-0 flex-1 flex">
            <button v-show="notifications.previous" @click="prevPage" class="border-t-2 border-transparent pt-4 pr-1 inline-flex items-center text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300">
              <ArrowNarrowLeftIcon class="mr-3 h-5 w-5 text-gray-400" aria-hidden="true" />
              Previous
            </button>
          </div>
          <div class="hidden md:-mt-px md:flex">
            <button v-show="notifications.previous" @click="prevPage" class="border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 border-t-2 pt-4 px-4 inline-flex items-center text-sm font-medium" aria-current="page">
              {{ pageNumber - 1 }}
            </button>
            <span class="border-primary text-primary-600 border-t-2 pt-4 px-4 inline-flex items-center text-sm font-medium" aria-current="page">
              {{ pageNumber }}
            </span>
            <button v-show="notifications.next" @click="nextPage" class="border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 border-t-2 pt-4 px-4 inline-flex items-center text-sm font-medium" aria-current="page">
              {{ pageNumber + 1 }}
            </button>
          </div>
          <div class="-mt-px w-0 flex-1 flex justify-end">
            <button v-show="notifications.next" @click="nextPage" class="border-t-2 border-transparent pt-4 pl-1 inline-flex items-center text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300">
              Next
              <ArrowNarrowRightIcon class="ml-3 h-5 w-5 text-gray-400" aria-hidden="true" />
            </button>
          </div>
        </nav>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
import moment from 'moment'

import { ArrowNarrowLeftIcon, ArrowNarrowRightIcon } from '@heroicons/vue/solid'

const CompleteTask = require('@/assets/img/svg/completeTask.svg')

export default {
  name: 'Notifications',
  components: {
    ArrowNarrowLeftIcon,
    ArrowNarrowRightIcon
  },
  data: () => ({
    completeTask: CompleteTask,
    notifications: [],
    is_read: 'False',
    pageNumber: 1,
    tabs: [
      { name: 'Unread', is_read: 'False', current: true, count: 1 },
      { name: 'Read', is_read: 'True', current: false },
      { name: 'All', is_read: '', current: false }
    ]
  }),
  watch: {
    is_read: function () {
      this.getNotifications()
    }
  },
  created () {
    axios.get('/api/notifications', {
      params: {
        is_read: this.is_read
      }
    }).then(response => {
      this.notifications = response.data
      this.getNotificationCount()
    })
  },
  methods: {
    nextPage () {
      if (this.notifications.next) {
        axios.get(this.notifications.next.substr(this.notifications.next.indexOf('/', 7))).then(response => {
          this.notifications = response.data
          this.pageNumber += 1
        })
      }
    },
    prevPage () {
      if (this.notifications.previous) {
        if (this.pageNumber === 2) {
          this.pageNumber = 1
          this.getNotifications()
        } else if (this.pageNumber > 2) {
          axios.get(this.notifications.previous.substr(this.notifications.previous.indexOf('/', 7))).then(response => {
            this.notifications = response.data
            this.pageNumber -= 1
          })
        }
      }
    },
    getNotifications () {
      axios.get('/api/notifications', {
        params: {
          is_read: this.is_read
        }
      }).then(response => {
        this.notifications = response.data
        this.getNotificationCount()
      })
    },
    getNotificationCount () {
      axios.get('/api/notifications/unread').then(response => {
        this.tabs[0].count = response.data
      })
    },
    markAllAsRead () {
      axios.put('/api/notifications/read/all').then(_ => {
        this.getNotifications()
      })
    },
    date (date) {
      return moment.parseZone(date).calendar(null, {
        lastDay: '[Yesterday at] HH:mm',
        sameDay: '[Today at] HH:mm',
        nextDay: '[Tomorrow at] HH:mm',
        lastWeek: '[Last] dddd [at] HH:mm',
        nextWeek: 'dddd [at] HH:mm',
        sameElse: 'L [at] HH:mm'
      })
    }
  },
  computed: {
    ...mapState({
      user: state => state.user,
      inboxes: state => state.inboxes
    })
  }
}
</script>
