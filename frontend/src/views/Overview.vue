<template>
  <div v-if="role == 'AGENT'"></div>

  <div v-else-if="role == 'MANAGER'">
    <div class="p-4">
      <div class="max-w-3xl mx-auto flex flex-col space-y-4">
        <router-link
          :to="`/inboxes/1/tickets/1`"
          class="group border rounded-lg flex flex-col p-3"
        >
          <div class="flex justify-between">
            <div class="flex space-x-2 text-red-600">
              <ExclamationCircleIcon class="w-5 h-5" />
              <span class="font-medium text-sm">HIGH</span>
            </div>
            <span
              class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800"
              >Created</span
            >
          </div>

          <h2
            class="font-semibold text-lg group-hover:underline mt-1 leading-6"
          >
            Should we write the individual report in the passive form?
          </h2>

          <div class="flex justify-between items-center">
            <h3 class="text-xs text-gray-500 dark:text-gray-400">
              <span class="font-medium">Ivan de Wolf</span>・Today at 00:35
            </h3>
          </div>

          <div class="flex mt-2">
            <chip background="#FF0000">Assignment</chip>
          </div>
        </router-link>

        <router-link
          :to="`/inboxes/1/tickets/1`"
          class="group border rounded-lg flex flex-col p-3"
        >
          <div class="flex justify-between">
            <div class="flex space-x-2 text-yellow-600">
              <BellIcon class="w-5 h-5" />
              <span class="font-medium text-sm">MEDIUM</span>
            </div>
            <span
              class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-yellow-100 text-yellow-800"
              >Reaction</span
            >
          </div>

          <h2
            class="font-semibold text-lg group-hover:underline mt-1 leading-6"
          >
            Is there a lecture on the day of the demo?
          </h2>

          <div class="flex justify-between items-center">
            <h3 class="text-xs text-gray-500 dark:text-gray-400">
              <span class="font-medium">Jurre Brandsen</span>・Yesterday 17:36
            </h3>
          </div>

          <div class="flex mt-2">
            <chip background="#0000FF">Lectures</chip>
          </div>
        </router-link>

        <!-- <div class="flex flex-col space-y-4 items-center">
          <img
            :src="HighFive"
            alt="Nothing here"
            class="w-64 h-64"
          />
          <span class="text-gray-800 text-lg md:text-xl font-semibold">
            Concrats you are all up to date, nothing you need to do now!
          </span>
        </div> -->
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import store from "@/store";
import { mapState } from "vuex";

import Chip from "@/components/chip/Chip.vue";

import { BellIcon, ExclamationCircleIcon } from "@heroicons/vue/24/outline";

export default {
  name: "Overview",
  components: {
    BellIcon,
    Chip,
    ExclamationCircleIcon,
  },
  data: () => ({
    role: "STUDENT",
  }),
  created() {
    axios
      .get(`/api/inboxes/${this.$route.params.inboxId}/role`)
      .then((response) => {
        if (response.data.key === "MANAGER") this.role = "MANAGER";
        else if (response.data.key === "AGENT") this.role = "AGENT";
        else this.role = "STUDENT";
      });
  },
  computed: {
    ...mapState({
      user: (state) => state.user,
      tickets() {
        return store.getters.inbox(this.$route.params.inboxId)?.tickets;
      },
    }),
  },
};
</script>
