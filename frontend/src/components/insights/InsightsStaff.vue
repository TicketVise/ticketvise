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
            <ArrowSmUpIcon v-if="item.changeDirection === 'up'" class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5" :class="[item.changeType === 'increase' ? 'text-green-500' : 'text-red-500']" aria-hidden="true" />
            <ArrowSmDownIcon v-else class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5" :class="[item.changeType === 'increase' ? 'text-green-500' : 'text-red-500']" aria-hidden="true" />
            <span class="sr-only"> {{ item.changeType === 'increase' ? 'Increased' : 'Decreased' }} by </span>
            {{ item.change }}
          </div>
        </dd>
      </div>
    </dl>

    <!-- Some general graphs here -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-4">
      <div class="col-span-1 border rounded-lg p-4 pt-2">
        <h2 class="text-lg font-semibold text-primary-600">Helpfulness of staff</h2>
        <ul role="list" class="divide-y divide-gray-200">
          <li v-for="member in staff.sort((a, b) => b.helpfulness.percentage - a.helpfulness.percentage)" :key="member.id">
            <div class="p-3">
              <div class="flex items-center justify-between">
                <span class="inline-flex items-center px-2 py-0.5 rounded-full text-sm text-gray-800 truncate space-x-2">
                  <img class="inline-block h-6 w-6 rounded-full" :src="member.image" alt="" />
                  <span class="truncate">{{ member.name }}</span>
                </span>
                <div class="ml-2 flex-shrink-0 flex">
                  <p class="px-2 inline-flex leading-5 font-medium rounded-full text-primary text-xl items-baseline">
                    {{ member.helpfulness.percentage }}
                    <span class="text-gray-400 text-xs font-normal">/{{ member.helpfulness.count }}</span>
                  </p>
                </div>
              </div>
            </div>
          </li>
        </ul>
      </div>

      <div class="col-span-1 border rounded-lg p-4 pt-2">
        <h2 class="text-lg font-semibold text-primary-600">Most answered topic</h2>
        <ul role="list" class="divide-y divide-gray-200">
          <li v-for="member in staff" :key="member.id">
            <div class="p-3">
              <div class="flex items-center justify-between">
                <span class="inline-flex items-center px-2 py-0.5 rounded-full text-sm text-gray-800 truncate space-x-2">
                  <img class="inline-block h-6 w-6 rounded-full" :src="member.image" alt="" />
                  <span class="truncate">{{ member.name }}</span>
                </span>
                <div class="ml-2 flex-shrink-0 flex">
                  <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-primary-100 text-primary-700">
                    {{ member.mainTopic }}
                  </span>
                </div>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios'
import { ArrowSmDownIcon, ArrowSmUpIcon } from '@heroicons/vue/solid'

const stats = [
  { name: 'Total Staff', stat: '6', previousStat: '', change: '', changeDirection: '', changeType: 'increase' },
  { name: 'Average time to respond', stat: '2.3h', previousStat: '2.4h', change: '3.15%', changeDirection: 'down', changeType: 'increase' },
  { name: 'Open Tickets', stat: '4', previousStat: '5', change: '20.00%', changeDirection: '', changeType: 'decrease' },
  { name: 'Average Tickets per user', stat: '2.4', previousStat: '', change: '', changeDirection: '', changeType: 'decrease' }
]

export default {
  name: 'InsightsStaff',
  components: {
    ArrowSmDownIcon,
    ArrowSmUpIcon
  },
  setup () {
    return {
      stats
    }
  },
  data: () => ({
    staff: []
  }),
  async mounted () {
    const { inboxId } = this.$route.params

    const testTopics = ['Assignment', 'Lecture', 'Slides', 'Code']

    /* Getting the staff data. */
    const staffResponse = await axios.get(`/api/inboxes/${inboxId}/staff`)
    this.staff = staffResponse.data.map(member => {
      return {
        name: member.first_name + ' ' + member.last_name,
        helpfulness: {
          percentage: (Math.random() * 100).toPrecision(3),
          count: Math.floor(Math.random() * 100)
        },
        image: member.avatar_url,
        mainTopic: testTopics[Math.floor(Math.random() * testTopics.length)]
      }
    })
  }
}
</script>
