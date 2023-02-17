<template>
  <div class="overflow-y-auto">
    <!-- Tabs -->
    <div class="p-4 sm:p-0 pb-0">
      <div class="sm:hidden">
        <label for="tabs" class="sr-only">Select a tab</label>
        <!-- Use an "onChange" listener to redirect the user to the selected tab URL. -->
        <select id="tabs" name="tabs" @change="switchTab($event.target.value)" class="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm rounded-md">
          <option v-for="tab in tabs" :key="tab.name" :selected="tab.current">
            {{ tab.name }}
          </option>
        </select>
      </div>
      <div class="hidden sm:block">
        <div class="flex items-center border-b border-gray-200">
          <nav class="flex-1 -mb-px flex space-x-6 xl:space-x-8 px-4" aria-label="Tabs">
            <router-link v-for="tab in tabs" :key="tab.name" :aria-current="tab.current ? 'page' : undefined" :to="{ name: 'Insights', params: { inboxId: this.$route.params.inboxId, tab: tab.name.toLowerCase() } }" :class="[tab.current ? 'border-primary text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300', 'cursor-pointer group inline-flex items-center py-4 px-1 border-b-2 font-medium text-sm']">
              <component :is="tab.icon" :class="[tab.current ? 'text-primary' : 'text-gray-400 group-hover:text-gray-500', '-ml-0.5 mr-2 h-5 w-5']" aria-hidden="true" />
              <span>{{ tab.name }}</span>
            </router-link>
          </nav>
        </div>
      </div>
    </div>

    <div class="p-4">
      <InsightsGeneral
        v-if="tabs.find((t) => t.current).name === 'General'"
      />
      <InsightsTickets
        v-if="tabs.find((t) => t.current).name === 'Tickets'"
      />
      <InsightsLabels v-if="tabs.find((t) => t.current).name === 'Labels'" />
      <InsightsStudents
        v-if="tabs.find((t) => t.current).name === 'Students'"
      />
      <InsightsStaff v-if="tabs.find((t) => t.current).name === 'Staff'" />
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";
import {
  BookmarkIcon,
  RectangleGroupIcon,
  TicketIcon,
  UserIcon,
  UsersIcon,
} from "@heroicons/vue/24/solid";
import InsightsGeneral from "@/components/insights/InsightsGeneral.vue";
import InsightsTickets from "@/components/insights/InsightsTickets.vue";
import InsightsLabels from "@/components/insights/InsightsLabels.vue";
import InsightsStudents from "@/components/insights/InsightsStudents.vue";
import InsightsStaff from "@/components/insights/InsightsStaff.vue";

export default {
  components: {
    InsightsGeneral,
    InsightsTickets,
    InsightsLabels,
    InsightsStudents,
    InsightsStaff,
  },
  data: () => ({
    tabs: [
      { name: "General", current: true, icon: RectangleGroupIcon },
      { name: "Tickets", current: false, icon: TicketIcon },
      { name: "Labels", current: false, icon: BookmarkIcon },
      { name: "Students", current: false, icon: UsersIcon },
      { name: "Staff", current: false, icon: UserIcon },
    ],
  }),
  created() {
    if (this.$route.params.tab) {
      this.tabs.forEach((t) => (t.current = false))
      this.tabs.find((t) => t.name.toLowerCase() === this.$route.params.tab.toLowerCase()).current = true
    }
  },
  methods: {
    switchTab(name) {
      this.$router.push({ name: 'Insights', params: { inboxId: this.$route.params.inboxId, tab: name.toLowerCase() } })
    }
  },
  computed: {
    ...mapState({
      user: (state) => state.user,
    }),
  },
};
</script>
