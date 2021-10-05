<template>
  <div class="overflow-y-auto">
    <div class="pt-8 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex">
        <h1 class="flex-1 text-2xl font-bold text-gray-900">Insights</h1>
      </div>

      <!-- Tabs -->
      <div class="mt-3 sm:mt-2">
        <div class="sm:hidden">
          <label for="tabs" class="sr-only">Select a tab</label>
          <!-- Use an "onChange" listener to redirect the user to the selected tab URL. -->
          <select id="tabs" name="tabs" @change="switchTab(); tabs.find(t => t.name === $event.target.value).current = true" class="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm rounded-md">
            <option v-for="tab in tabs" :key="tab.name" :selected="tab.current">{{ tab.name }}</option>
          </select>
        </div>
        <div class="hidden sm:block">
          <div class="flex items-center border-b border-gray-200">
            <nav class="flex-1 -mb-px flex space-x-6 xl:space-x-8" aria-label="Tabs">
              <a v-for="tab in tabs" :key="tab.name" :aria-current="tab.current ? 'page' : undefined" @click="switchTab(); tabs.find(t => t.name === tab.name).current = true" :class="[tab.current ? 'border-primary text-primary-600' : 'cursor-pointer border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300', 'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm']">
                {{ tab.name }}
              </a>
            </nav>
          </div>
        </div>
      </div>

      <InsightsTickets v-show="tabs.find(t => t.current).name === 'Tickets'" />
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

import InsightsTickets from '@/components/insights/InsightsTickets'

export default {
  components: {
    InsightsTickets
  },
  data: () => ({
    tabs: [
      { name: 'Tickets', current: true },
      { name: 'Labels', current: false },
      { name: 'Users', current: false }
    ]
  }),
  methods: {
    switchTab () {
      this.tabs.forEach(t => (t.current = false))
    }
  },
  computed: {
    ...mapState({
      user: state => state.user
    })
  }
}
</script>
