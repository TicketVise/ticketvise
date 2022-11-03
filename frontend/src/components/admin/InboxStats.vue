<template>
  <div>
    <div class="pl-6 pr-2 py-4 flex justify-between">
      <div class="flex-grow grid sm:grid-cols-2">
        <div class="flex space-x-4">
          <img
            class="h-12 w-12 rounded-full object-cover border-2"
            :style="`border-color: ${inbox.color}`"
            :src="inbox.image || `/img/default-inbox.png`"
          />
          <div class="flex flex-col">
            <router-link
              class="text-primary break-words hover:underline"
              :to="`/inboxes/${inbox.id}/tickets`"
            >
              {{ inbox.name }}
            </router-link>
            <div class="flex items-center text-sm leading-5 text-gray-500">
              <UserIcon class="mr-1 w-4 h-4" />
              {{
                stats
                  ? stats.coordinator.first_name +
                    " " +
                    stats.coordinator.last_name
                  : ""
              }}
            </div>
          </div>
        </div>
        <div class="hidden md:flex flex-col">
          <span class="text-gray-800">
            <span class="font-bold">Started:</span>
            {{ date(inbox.date_created) }}
          </span>
          <span class="text-gray-800 flex items-center">
            <ClipboardDocumentListIcon class="mr-1 w-4 h-4" />
            <span>{{ inbox.scheduling_algorithm }}</span>
          </span>
        </div>
      </div>
      <div
        class="flex md:items-center hover:bg-gray-200 rounded-full cursor-pointer select-none p-2 w-10 h-10 mr-2"
        @click="open = !open"
      >
        <ChevronDownIcon v-if="!open" class="w-6 h-6" />
        <ChevronUpIcon v-else class="w-6 h-6" />
      </div>
    </div>
    <div v-if="open" class="border-t py-2 sm:px-6">
      <div class="grid grid-cols-3 divide-x">
        <div class="flex flex-col items-center">
          <span class="text-primary text-2xl">
            {{ stats ? stats.users : "" }}
          </span>
          <span class="text-gray-700">Users</span>
        </div>
        <div class="flex flex-col items-center">
          <span class="text-primary text-2xl">
            {{ stats ? stats.total_tickets : "" }}
          </span>
          <span class="text-gray-700">Tickets</span>
        </div>
        <div class="flex flex-col items-center">
          <span class="text-primary text-2xl">
            {{ stats ? stats.labels : "" }}
          </span>
          <span class="text-gray-700">Labels</span>
        </div>
      </div>
      <div class="mt-2">
        <h2 class="font-bold text-gray-800 ml-12">Number of Tickets</h2>
        <TicketsChart :inboxId="inbox.id" :height="200" />
      </div>
    </div>
  </div>
</template>

<script>
import TicketsChart from "@/components/insights/TicketsChart.vue";
import axios from "axios";
import moment from "moment";

import {
  ChevronDownIcon,
  ChevronUpIcon,
  ClipboardDocumentListIcon,
  UserIcon,
} from "@heroicons/vue/24/outline";

export default {
  components: {
    ChevronDownIcon,
    ChevronUpIcon,
    ClipboardDocumentListIcon,
    UserIcon,
    TicketsChart,
  },
  data: () => ({
    open: false,
    stats: null,
  }),
  props: {
    inbox: {
      required: true,
      type: Object,
    },
  },
  methods: {
    date(date) {
      return moment.parseZone(date).calendar(null, {
        lastDay: "[Yesterday at] HH:mm",
        sameDay: "[Today at] HH:mm",
        nextDay: "[Tomorrow at] HH:mm",
        lastWeek: "[Last] dddd [at] HH:mm",
        nextWeek: "dddd [at] HH:mm",
        sameElse: "L [at] HH:mm",
      });
    },
  },
  mounted() {
    axios.get(`/api/inboxes/${this.inbox.id}/statistics`).then((response) => {
      this.stats = response.data;
    });
  },
};
</script>
