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
import { ArrowSmallDownIcon, ArrowSmallUpIcon } from '@heroicons/vue/24/solid'

const stats = [
  { name: 'Total Students', stat: '125', previousStat: '', change: '', changeDirection: '', changeType: 'increase' },
  { name: 'Active Students', stat: '61', previousStat: '54', change: '18.34%', changeDirection: 'up', changeType: 'increase' },
  { name: 'Open Tickets', stat: '4', previousStat: '5', change: '20.00%', changeDirection: 'down', changeType: 'increase' },
  { name: 'Average Tickets per user', stat: '2.4', previousStat: '', change: '', changeDirection: '', changeType: 'decrease' }
]

export default {
  name: 'InsightsStudents',
  components: {
    ArrowSmallDownIcon,
    ArrowSmallUpIcon
  },
  setup () {
    return {
      stats
    }
  }
}
</script>
