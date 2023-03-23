<template>
  <div class="flex h-full overflow-y-auto w-full">
    <div class="w-screen max-w-screen-lg mx-auto px-4 my-4">
      <!-- Actions header -->
      <div class="mb-1">
        <h2 class="text-gray-700 text-xl font-bold leading-6">Filters</h2>
        <span class="text-gray-400"
          >Apply filters to incoming tickets and perform actions based on
          conditions.</span
        >
      </div>
      <div class="flex flex-col space-y-2">
        <!-- <draggable
          :animation="200"
          ghost-class="moving-card"
          :list="items"
          handle=".handle"
          class="space-y-2"
        > -->
        <automation-filter
          v-for="filter of filters"
          :key="filter"
          :filterId="filter.id"
          @update="retrieveFilters()"
        />
        <!-- </draggable> -->
        <button
          v-if="!filters.find((filter) => filter.id < 0)"
          @click="addFilter"
          type="button"
          class="relative block w-full border-2 border-gray-300 border-dashed rounded-lg p-4 text-center hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink"
            aria-hidden="true"
            role="img"
            class="mx-auto h-8 w-8 text-gray-400"
            preserveAspectRatio="xMidYMid meet"
            viewBox="0 0 24 24"
          >
            <path
              d="M15 17h3v-3h2v3h3v2h-3v3h-2v-3h-3v-2m-2 2.88c.04.3-.06.62-.28.83c-.4.39-1.03.39-1.42 0L7.29 16.7a.989.989 0 0 1-.29-.83v-5.12L2.21 4.62a1 1 0 0 1 .17-1.4c.19-.14.4-.22.62-.22h14c.22 0 .43.08.62.22a1 1 0 0 1 .17 1.4L13 10.75v9.13M5.04 5L9 10.07v5.51l2 2v-7.53L14.96 5H5.04z"
              fill="currentColor"
            ></path>
          </svg>
          <span class="mt-2 block text-sm font-medium text-gray-900">
            {{ filters?.length > 0 ? "Add another filter" : "Add a filter" }}
          </span>
        </button>
      </div>

      <!-- Default header -->
      <div class="mb-1 mt-12">
        <h2 class="text-gray-700 text-xl font-bold leading-6">Default</h2>
        <span class="text-gray-400"
          >What to do with a ticket if no filter applies.</span
        >
      </div>

      <div class="pb-4">
        <!-- Default card -->
        <automation-default></automation-default>
      </div>
    </div>
  </div>
</template>

<script>
import store from "@/store";
import { mapState } from "vuex";

import axios from "axios";
import Draggable from "vuedraggable";
import AutomationDefault from "@/components/automation/AutomationDefault.vue";
import AutomationFilter from "@/components/automation/AutomationFilter.vue";

import { ExclamationTriangleIcon, PlusIcon } from "@heroicons/vue/24/solid";

export default {
  name: "Automation",
  components: {
    PlusIcon,
    AutomationDefault,
    ExclamationTriangleIcon,
    AutomationFilter,
    Draggable,
  },
  mounted() {
    this.retrieveFilters();
  },
  methods: {
    retrieveFilters() {
      axios
        .get(`/api/inboxes/${this.$route.params.inboxId}/automations`)
        .then((response) =>
          store.commit("automation/updateFilters", response.data)
        );
    },
    addFilter() {
      store.commit("automation/newFilter");
    },
  },
  computed: {
    ...mapState("automation", {
      filters: (state) => state.filters,
    }),
  },
};
</script>
