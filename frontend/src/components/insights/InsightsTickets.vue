<template>
  <section aria-labelledby="tickets-heading">
    <h2 id="tickets-heading" class="sr-only">Ticket insights</h2>

    <!-- Some basic stats first -->
    <dl class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <div v-for="item in stats" :key="item.name" class="px-4 py-3 rounded-lg border">
        <dt class="text-base font-normal text-gray-900">
          {{ item.name }}
        </dt>
        <dd class="flex justify-between items-baseline md:block lg:flex">
          <div class="flex items-baseline text-2xl font-semibold text-primary-600">
            {{ item.stat }}
            <span v-if="item.previousStat" class="ml-2 text-sm font-medium text-gray-500"> from {{ item.previousStat }} </span>
          </div>

          <div v-if="item.change" :class="[item.changeType === 'increase' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800', 'inline-flex items-baseline px-2.5 py-0.5 rounded-full text-sm font-medium md:mt-2 lg:mt-0']">
            <ArrowSmallUpIcon v-if="item.changeDirection === 'up'" class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5" :class="[item.changeType === 'increase' ? 'text-green-500' : 'text-red-500']" aria-hidden="true" />
            <ArrowSmallDownIcon v-else class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5" :class="[item.changeType === 'increase' ? 'text-green-500' : 'text-red-500']" aria-hidden="true" />
            <span class="sr-only"> {{ item.changeType === 'increase' ? 'Increased' : 'Decreased' }} by </span>
            {{ item.change }}
          </div>
        </dd>
      </div>
    </dl>

    <!-- Some general graphs here -->
  </section>
</template>

<script>
import axios from 'axios'
import { ArrowSmallDownIcon, ArrowSmallUpIcon } from '@heroicons/vue/24/solid'

export default {
  name: 'InsightsTickets',
  components: {
    ArrowSmallDownIcon,
    ArrowSmallUpIcon
  },
  data: () => ({
    statsData: null
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
