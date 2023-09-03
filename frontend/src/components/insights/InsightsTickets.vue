<template>
  <section aria-labelledby="tickets-heading" class="mx-auto flex max-w-3xl flex-col space-y-4 overflow-y-auto">
    <!-- Some basic stats first -->
    <div class="grid w-full grid-cols-2 gap-2">
      <div class="flex items-center overflow-hidden rounded-lg border bg-white p-2 px-4">
        <div class="hidden flex-shrink-0 sm:flex">
          <TicketIcon class="h-6 w-6 text-gray-400" />
        </div>
        <dl class="w-0 flex-1 sm:ml-5">
          <dt class="truncate text-sm font-medium text-gray-500">Tickets</dt>
          <dd class="flex items-center justify-between">
            <div class="text-xl font-medium text-primary">
              {{ this.statsData?.total_tickets || 0 }}
            </div>
          </dd>
        </dl>
      </div>

      <div class="flex items-center overflow-hidden rounded-lg border bg-white p-2 px-4">
        <div class="hidden flex-shrink-0 sm:flex">
          <GlobeEuropeAfricaIcon class="h-6 w-6 text-gray-400" />
        </div>
        <div class="w-0 flex-1 sm:ml-5">
          <dl>
            <dt class="truncate text-sm font-medium text-gray-500">Public tickets</dt>
            <dd class="flex items-center justify-between">
              <div class="text-xl font-medium text-primary">
                {{ this.statsData?.total_public_tickets || 0 }}
              </div>
            </dd>
          </dl>
        </div>
      </div>
    </div>

    <!-- Some general graphs here -->
    <div>
      <div class="flex justify-between items-center mb-1">
        <h2 class="text-lg font-semibold text-primary-600">Tickets</h2>
        <span class="isolate inline-flex rounded-md">
          <button @click="ticketChartType = 'date'" type="button" :class="[ticketChartType == 'date' ? 'text-primary bg-gray-100' : 'text-gray-700 bg-white', 'relative inline-flex items-center rounded-l-md border border-gray-300 px-2 py-1 text-sm font-medium hover:bg-gray-50 focus:z-10 focus:outline-none']">
            Days
          </button>
          <button @click="ticketChartType = 'week_day'" type="button" :class="[ticketChartType == 'week_day' ? 'text-primary bg-gray-100' : 'text-gray-700 bg-white', 'relative -ml-px inline-flex items-center border border-gray-300 px-2 py-1 text-sm font-medium hover:bg-gray-50 focus:z-10 focus:outline-none']">
            Week day
          </button>
          <button @click="ticketChartType = 'hour'" type="button" :class="[ticketChartType == 'hour' ? 'text-primary bg-gray-100' : 'text-gray-700 bg-white', 'relative -ml-px inline-flex items-center rounded-r-md border border-gray-300 px-2 py-1 text-sm font-medium hover:bg-gray-50 focus:z-10 focus:outline-none']">
            Hours
          </button>
        </span>
      </div>
      <TicketsTimeChart :inbox-id="$route.params.inboxId" :height="200" :type="ticketChartType" />
    </div>

    <!-- <div class="rounded-md bg-blue-50 p-4">
      <div class="flex">
        <div class="flex-shrink-0">
          <ClockIcon class="h-5 w-5 text-blue-400" aria-hidden="true" />
        </div>
        <div class="ml-3">
          <h3 class="text-sm font-medium text-blue-700">Best times</h3>
          <div class="mt-1 text-sm text-blue-700">
            <p>Based on the times the tickets come in, we advise you check your page at the following times to optimize the shortest response time: <strong>13h</strong> and <strong>21h</strong>.</p>
          </div>
        </div>
      </div>
    </div> -->
  </section>
</template>

<script>
import axios from 'axios'
import { ArrowSmallDownIcon, ArrowSmallUpIcon, CalendarDaysIcon, ClockIcon } from '@heroicons/vue/24/solid'
import { GlobeEuropeAfricaIcon, TicketIcon } from '@heroicons/vue/24/outline'

import TicketsTimeChart from '@/components/insights/TicketsTimeChart.vue'

export default {
  name: 'InsightsTickets',
  components: {
    ArrowSmallDownIcon,
    ArrowSmallUpIcon,
    TicketIcon,
    TicketsTimeChart,
    CalendarDaysIcon,
    ClockIcon,
    GlobeEuropeAfricaIcon
},
  data: () => ({
    statsData: null,
    ticketChartType: 'hour'
  }),
  async mounted () {
    const { inboxId } = this.$route.params

    /* Gettings general statistics. */
    const statsResponse = await axios.get(`/api/inboxes/${inboxId}/statistics`)
    this.statsData = statsResponse.data
  },
  computed: {
    stats () {
      return [
        { name: 'Total Tickets', stat: this.statsData?.total_tickets || 0, previousStat: '', change: '', changeDirection: '', changeType: 'increase' },
        { name: 'Public Tickets', stat: this.statsData?.total_public_tickets || 0, previousStat: '', change: '', changeDirection: '', changeType: 'increase' },
        { name: 'Open Tickets', stat: this.statsData?.total_open_tickets || 0, previousStat: '3', change: '33%', changeDirection: 'down', changeType: 'increase' },
        { name: 'Average Tickets per user', stat: this.statsData?.avg_ticket_per_student || 0, previousStat: '', change: '', changeDirection: '', changeType: 'increase' }
      ]
    }
  }
}
</script>
