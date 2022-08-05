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
          <!-- <automation-filter v-for="i of items" :key="i" /> -->
        <!-- </draggable> -->
        <!-- <button
          @click="items.push(items.length)"
          class="relative flex items-center space-x-1 text-primary cursor-pointer self-center focus:outline-none"
        >
          <plus-icon class="h-6 w-6" />
          <span>Add another filter</span>
        </button> -->

        <div class="rounded-md bg-yellow-50 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <ExclamationIcon class="h-5 w-5 text-yellow-400" aria-hidden="true" />
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-yellow-800">
                Coming soon
              </h3>
              <div class="mt-2 text-sm text-yellow-700">
                <p>
                  Automation is currently under development and will be available soon so you can start filtering tickets on different criteria.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div class="control-section">
        </div>
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
// import Draggable from 'vuedraggable'

import AutomationDefault from '@/components/automation/AutomationDefault.vue'
// import AutomationFilter from '@/components/automation/AutomationFilter.vue'

import {
  ExclamationIcon
  // PlusIcon
} from '@heroicons/vue/solid'

export default {
  name: 'Automation',
  components: {
    // PlusIcon,
    AutomationDefault,
    ExclamationIcon
    // AutomationFilter
    },
  data: () => ({
    items: [],
    values: ['Mr.', 'Mrs.', 'Ms.']
  })
}
</script>
