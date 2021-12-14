<template>
  <div class="flex h-full overflow-y-auto w-full">
    <div class="w-screen max-w-screen-lg mx-auto px-4 my-4">
      <!-- Actions header -->
      <div class="mb-1">
        <h2 class="text-gray-700 text-xl font-bold leading-6">Actions</h2>
        <span class="text-gray-400"
          >Perform actions to incoming tickets based on given conditions.</span
        >
      </div>
      <div class="flex flex-col space-y-2 mb-4">
        <!-- <draggable
          :animation="200"
          ghost-class="moving-card"
          :list="items"
          handle=".handle"
          class="space-y-2"
        > -->
          <automation-filter v-for="item of items" :key="item" :item="item" />
        <!-- </draggable> -->
        <button
          @click="items.push(items.length)"
          class="
            relative
            flex
            items-center
            space-x-1
            text-primary
            cursor-pointer
            self-center
            focus:outline-none
          "
        >
          <plus-icon class="h-6 w-6" />
          <span>Add another filter</span>
        </button>
      </div>

      <!-- Default header -->
      <div class="mb-1">
        <h2 class="text-gray-700 text-xl font-bold leading-6">Default</h2>
        <span class="text-gray-400"
          >What to do with a ticket if no action applies.</span
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
import axios from 'axios'
import Draggable from "vuedraggable";
import AutomationDefault from "@/components/automation/AutomationDefault";
import AutomationFilter from "@/components/automation/AutomationFilter";

import {
  ExclamationIcon,
  PlusIcon
} from "@heroicons/vue/solid";

export default {
  name: "Automation",
  components: {
    PlusIcon,
    AutomationDefault,
    ExclamationIcon,
    AutomationFilter,
    Draggable,
  },
  data: () => ({
    items: [],
  }),
  mounted () {
    axios.get(`/api/inboxes/${this.$route.params.inboxId}/automations`) 
      .then((response) => {
        this.items = response.data
      })
  },
};
</script>
