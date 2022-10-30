<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:max-w-7xl lg:px-8">
    <header class="bg-white shadow rounded-lg pb-4 mb-4">
      <div class="max-w-7xl mx-auto p-4">
        <div class="sm:flex sm:items-center sm:justify-between">
          <div class="flex-1 min-w-0">
            <span class="sm:hidden float-right">
              <a
                href="/api/admin/django"
                class="inline-flex items-center py-2 text-sm leading-5 font-medium text-gray-700 hover:text-gray-500 focus:outline-none active:text-gray-800 active:bg-gray-50 transition duration-150 ease-in-out"
              >
                <CogIcon class="mr-3 h-5 w-5 text-gray-400" />
              </a>
            </span>

            <h2
              class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:leading-9 truncate"
            >
              Admin overview
            </h2>
          </div>
          <div class="mt-2 sm:mt-0 sm:ml-4 space-x-4 hidden sm:flex">
            <span class="shadow-sm rounded-md">
              <a
                href="/api/admin/django"
                class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm leading-5 font-medium rounded-md text-gray-700 bg-white hover:text-gray-500 focus:outline-none focus:ring-blue focus:border-blue-300 active:text-gray-800 active:bg-gray-50 transition duration-150 ease-in-out"
              >
                <CogIcon class="mr-3 h-5 w-5 text-gray-400" />
                Django admin
              </a>
            </span>
          </div>
        </div>
      </div>

      <div class="grid md:grid-cols-3 gap-4 mx-4">
        <div
          class="rounded-md border flex-grow py-2 px-4 flex md:flex-col-reverse space-x-2 md:space-x-0 items-center md:items-start"
        >
          <div class="flex items-baseline sm:mt-1">
            <h2 class="text-2xl font-medium text-primary">
              {{ inboxes.length }}
            </h2>
          </div>
          <h3 class="text-lg leading-6 font-medium text-gray-900">Inboxes</h3>
        </div>

        <div
          class="rounded-md border flex-grow py-2 px-4 flex md:flex-col-reverse space-x-2 md:space-x-0 items-center md:items-start"
        >
          <div class="flex items-baseline mt-1">
            <h2 class="text-2xl font-medium text-primary">{{ users }}</h2>
          </div>
          <h3 class="text-lg leading-6 font-medium text-gray-900">Users</h3>
        </div>

        <div
          class="rounded-md border flex-grow py-2 px-4 flex md:flex-col-reverse space-x-2 md:space-x-0 items-center md:items-start"
        >
          <div class="flex items-baseline mt-1">
            <h2 class="text-2xl font-medium text-primary">{{ tickets }}</h2>
          </div>
          <h3 class="text-lg leading-6 font-medium text-gray-900">Tickets</h3>
        </div>
      </div>
    </header>

    <div class="w-full border rounded-lg divide-y bg-white shadow">
      <InboxStats v-for="inbox in inboxes" :key="inbox.id" :inbox="inbox" />
    </div>
  </div>
</template>

<script>
import InboxStats from "@/components/admin/InboxStats.vue";
import axios from "axios";

import { CogIcon } from "@heroicons/vue/24/outline";

export default {
  components: {
    CogIcon,
    InboxStats,
  },
  data: () => ({
    inboxes: [],
    users: 0,
    tickets: 0,
  }),
  async mounted() {
    const response = await axios.get("/api/inboxes");
    this.inboxes = response.data;
    const users = await axios.get("/api/admin/statistics/users/count");
    this.users = users.data.users;
    const tickets = await axios.get("/api/admin/statistics/tickets/count");
    this.tickets = tickets.data.tickets;
  },
};
</script>
