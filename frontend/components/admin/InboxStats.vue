<template>
  <div>
    <div class="pl-6 pr-2 py-4 flex justify-between">
      <div class="flex-grow grid sm:grid-cols-2">
        <div class="flex space-x-4">
          <img class="h-12 w-12 rounded-full object-cover border-4" :style="`border-color: ${inbox.color}`" :src="inbox.image">
          <div class="flex flex-col">
            <a class="text-orange-500 break-words hover:underline" :href="`/inboxes/${inbox.id}/tickets`">{{ inbox.name }}</a>
            <div class="flex items-center text-sm leading-5 text-gray-500">
              <i class="fa fa-user mr-1"></i>
              {{ stats ? stats.coordinator.first_name + ' ' + stats.coordinator.last_name : '' }}
            </div>
          </div>
        </div>
        <div class="hidden md:flex flex-col">
          <span class="text-gray-800">
            <span class="font-bold">Started:</span> 
            {{ date(inbox.date_created) }}
          </span>
          <span class="text-gray-800">
            <font-awesome-icon class="text-orange-400 group-hover:text-orange-500" icon="clipboard-list" />
            {{ inbox.scheduling_algorithm }}
          </span>
        </div>
      </div>
      <div class="flex md:items-center hover:bg-gray-100 rounded-full cursor-pointer select-none" @click="open = !open">
        <i class="fa p-4" :class="{ 'fa-chevron-down': !open, 'fa-chevron-up': open }"></i>
      </div>
    </div>
    <div v-if="open" class="border-t py-2 sm:px-6">
      <div class="grid grid-cols-3 divide-x">
        <div class="flex flex-col items-center">
          <span class="text-orange-500 text-2xl">
            {{ stats ? stats.users : '' }}
          </span>
          <span class="text-gray-700">Users</span>
        </div>
        <div class="flex flex-col items-center">
          <span class="text-orange-500 text-2xl">
            {{ stats ? stats.tickets : '' }}
          </span>
          <span class="text-gray-700">Tickets</span>
        </div>
        <div class="flex flex-col items-center">
          <span class="text-orange-500 text-2xl">
            {{ stats ? stats.labels : '' }}
          </span>
          <span class="text-gray-700">Labels</span>
        </div>
      </div>
      <div class="mt-2">
        <h2 class="font-bold text-gray-900 ml-12">Number of Tickets</h2>
        <tickets-chart :inboxId="inbox.id" :height="200" />
      </div>
    </div>
  </div>
</template>

<script>
import {calendarDate} from "../../utils";

import { library } from '@fortawesome/fontawesome-svg-core'
import { faClipboardList } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import TicketsChart from "../inbox_statistics/TicketsChart";

library.add(faClipboardList)

export default {
  components: {TicketsChart, FontAwesomeIcon },
  data: () => ({
    open: false,
    stats: null
  }),
  props: {
    inbox: {
      required: true,
      type: Object
    }
  },
  methods: {
    date: calendarDate
  },
  mounted() {
    window.axios.get(`/api/inboxes/${this.inbox.id}/statistics`).then(response => {
      this.stats = response.data
    })
  }
}
</script>
