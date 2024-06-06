<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:max-w-7xl lg:px-8">
    <header class="bg-white shadow rounded-lg pb-4 mb-4">
      <div class="max-w-7xl mx-auto p-4">
        <div class="sm:flex sm:items-center sm:justify-between">
          <div class="flex-1 min-w-0">
            <router-link
              :to="{ name: 'Admin' }"
              class="text-gray-600 text-sm truncate flex items-center space-x-1"
            >
              <ChevronLeftIcon class="h-3 w-3" />
              <span>Admin</span>
            </router-link>
            <h2
              class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:leading-9 truncate"
            >
              {{ deployment ? deployment.name : 'Loading...' }}
            </h2>
          </div>
        </div>
      </div>

      <div class="grid md:grid-cols-3 gap-4 mx-4">
        <div
          class="rounded-md border flex-grow py-2 px-4 flex md:flex-col-reverse space-x-2 md:space-x-0 items-center md:items-start"
        >
          <div class="flex items-baseline sm:mt-1">
            <h2 class="text-2xl font-medium text-primary">
              {{ deployment?.inboxes.length ?? '...' }}
            </h2>
          </div>
          <h3 class="text-lg leading-6 font-medium text-gray-900">Inboxes</h3>
        </div>

        <div
          class="rounded-md border flex-grow py-2 px-4 flex md:flex-col-reverse space-x-2 md:space-x-0 items-center md:items-start"
        >
          <div class="flex items-baseline mt-1">
            <h2 class="text-2xl font-medium text-primary">{{ deployment?.statistics.users ?? '...' }}</h2>
          </div>
          <h3 class="text-lg leading-6 font-medium text-gray-900">Users</h3>
        </div>

        <div
          class="rounded-md border flex-grow py-2 px-4 flex md:flex-col-reverse space-x-2 md:space-x-0 items-center md:items-start"
        >
          <div class="flex items-baseline mt-1">
            <h2 class="text-2xl font-medium text-primary">{{ deployment?.statistics.tickets ?? '...' }}</h2>
          </div>
          <h3 class="text-lg leading-6 font-medium text-gray-900">Tickets</h3>
        </div>
      </div>
    </header>

    <div v-if="deployment" class="w-full border rounded-lg divide-y bg-white shadow mb-4">
      <div class="p-4">
        <SelectInput label="Inbox" :data="deployment.inboxes" v-model="selectedInbox" />
      </div>

      <InboxStats v-if="selectedInbox?.name" :key="selectedInbox" :inbox="selectedInbox" />
    </div>

    <div v-if="deployment" class="w-full border rounded-lg divide-y bg-white shadow">
      <UsersPerYear :data="deployment.statistics.usersPerYear" />
    </div>
  </div>
</template>

<script>
import InboxStats from "@/components/admin/InboxStats.vue";
import UsersPerYear from "@/components/admin/UsersPerYear.vue";
import SelectInput from "@/components/inputs/SelectInput.vue";
import axios from "axios";
import { ChevronLeftIcon } from "@heroicons/vue/20/solid";

export default {
  name: "Deployment",
  components: {
    ChevronLeftIcon,
    InboxStats,
    SelectInput,
    UsersPerYear
  },
  data: () => ({
    deployment: null,
    selectedInbox: null
  }),
  mounted() {
    const { deploymentId } = this.$route.params;

    axios.get(`/api/admin/lti/${deploymentId}`).then((response) => {
      this.deployment = response.data;
      this.selectedInbox = this.deployment.inboxes[0];

      this.deployment.statistics.usersPerYear.datasets = [{
        fill: false,
        label: 'Users',
        backgroundColor: '#ed8936',
        borderColor: '#fbd38d',
        data: this.deployment.statistics.usersPerYear.data
      }]
    })
  }
}
</script>
