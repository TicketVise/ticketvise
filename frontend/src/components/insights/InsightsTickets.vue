<template>
  <section class="mt-4" aria-labelledby="tickets-heading">
    <h2 id="tickets-heading" class="sr-only">Ticket insights</h2>

    <!-- Some basic stats first -->
    <dl class="grid grid-cols-1 gap-5 sm:grid-cols-3">
      <div v-for="item in stats" :key="item.name" class="px-4 py-3 rounded-lg border">
        <dt class="text-base font-normal text-gray-900">
          {{ item.name }}
        </dt>
        <dd class="flex justify-between items-baseline md:block lg:flex">
          <div class="flex items-baseline text-2xl font-semibold text-primary-600">
            {{ item.stat }}
            <span class="ml-2 text-sm font-medium text-gray-500"> from {{ item.previousStat }} </span>
          </div>

          <div :class="[item.changeType === 'increase' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800', 'inline-flex items-baseline px-2.5 py-0.5 rounded-full text-sm font-medium md:mt-2 lg:mt-0']">
            <ArrowSmUpIcon v-if="item.changeType === 'increase'" class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5 text-green-500" aria-hidden="true" />
            <ArrowSmDownIcon v-else class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5 text-red-500" aria-hidden="true" />
            <span class="sr-only"> {{ item.changeType === 'increase' ? 'Increased' : 'Decreased' }} by </span>
            {{ item.change }}
          </div>
        </dd>
      </div>
    </dl>

    <!-- Some general graphs here -->
    <TicketsChart :inbox-id="$route.params.inboxId" />
  </section>
</template>

<script>
import { ArrowSmDownIcon, ArrowSmUpIcon } from '@heroicons/vue/solid'

import TicketsChart from '@/components/insights/TicketsChart'

const stats = [
  { name: 'Total Tickets', stat: '165', previousStat: '134', change: '12.75%', changeType: 'increase' },
  { name: 'Public Tickets', stat: '35', previousStat: '28', change: '14.65%', changeType: 'increase' },
  { name: 'Open Tickets', stat: '4', previousStat: '5', change: '20.00%', changeType: 'decrease' }
]

export default {
  name: 'InsightsTickets',
  components: {
    ArrowSmDownIcon,
    ArrowSmUpIcon,
    TicketsChart
  },
  setup () {
    return {
      stats
    }
  }
}
</script>
