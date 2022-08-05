<template>
  <div class="overflow-y-auto">
    <div>
      <!-- Tabs -->
      <div class="">
        <div class="sm:hidden">
          <label for="tabs" class="sr-only">Select a tab</label>
          <!-- Use an "onChange" listener to redirect the user to the selected tab URL. -->
          <select id="tabs" name="tabs" @change="switchTab(); tabs.find(t => t.name === $event.target.value).current = true" class="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm rounded-md">
            <option v-for="tab in tabs" :key="tab.name" :selected="tab.current">{{ tab.name }}</option>
          </select>
        </div>
        <div class="hidden sm:block">
          <div class="flex items-center border-b border-gray-200">
            <nav class="flex-1 -mb-px flex space-x-6 xl:space-x-8 px-4" aria-label="Tabs">
              <a v-for="tab in tabs" :key="tab.name" :aria-current="tab.current ? 'page' : undefined" @click="switchTab(); tabs.find(t => t.name === tab.name).current = true" :class="[tab.current ? 'border-primary text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300', 'cursor-pointer group inline-flex items-center py-4 px-1 border-b-2 font-medium text-sm']">
                <component :is="tab.icon" :class="[tab.current ? 'text-primary' : 'text-gray-400 group-hover:text-gray-500', '-ml-0.5 mr-2 h-5 w-5']" aria-hidden="true" />
                <span>{{ tab.name }}</span>
              </a>
            </nav>
          </div>
        </div>
      </div>

      <div class="p-4">
        <InsightsGeneral v-if="tabs.find(t => t.current).name === 'General'" />
        <InsightsTickets v-if="tabs.find(t => t.current).name === 'Tickets'" />
        <InsightsLabels v-if="tabs.find(t => t.current).name === 'Labels'" />
        <InsightsStudents v-if="tabs.find(t => t.current).name === 'Students'" />
        <InsightsStaff v-if="tabs.find(t => t.current).name === 'Staff'" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import TicketsChart from '@/components/insights/TicketsChart.vue'
import TicketsTimeChart from '@/components/insights/TicketsTimeChart.vue'
import AgentResponseTimeChart from '@/components/insights/AgentResponseTimeChart.vue'
import LabelsChart from '@/components/insights/LabelsChart.vue'
import IncreaseLabel from '@/components/chip/IncreaseLabel.vue'

export default {
  components: {
    InsightsGeneral,
    InsightsTickets,
    InsightsLabels,
    InsightsStudents,
    InsightsStaff
  },
  data: () => ({
    tabs: [
      { name: 'General', current: true, icon: TemplateIcon },
      { name: 'Tickets', current: false, icon: TicketIcon },
      { name: 'Labels', current: false, icon: BookmarkIcon },
      { name: 'Students', current: false, icon: UsersIcon },
      { name: 'Staff', current: false, icon: UserIcon }
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
