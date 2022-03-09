<template>
  <section aria-labelledby="tickets-heading">
    <h2 id="tickets-heading" class="sr-only">Ticket insights</h2>

    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <!-- Imformation about the staff. -->
      <div class="col-span-1 sm:col-span-2 border rounded-lg p-4 pt-2">
        <h2 class="text-lg font-semibold text-primary-600">Staff overview</h2>
        <ul role="list" class="divide-y divide-gray-200">
          <li v-for="member in staff.sort((a, b) => b.helpfulness.percentage - a.helpfulness.percentage)" :key="member.id">
            <div class="p-3">
              <div class="grid grid-cols-8 gap-2 items-center justify-between">
                <span class="col-span-4 inline-flex items-center px-2 rounded-full text-sm text-gray-800 truncate space-x-2">
                  <img class="inline-block h-8 w-8 rounded-full mr-2" :src="member.image" alt="" />
                  <div class="flex flex-col">
                    <span class="truncate text-base font-semibold leading-none">{{ member.name }}</span>
                    <div class="space-x-2">
                      <span class="text-gray-600 leading-none">Tickets: {{ member.helpfulness.count + Math.floor(Math.random() * 10) }}</span>
                      <span class="text-gray-600 leading-none">Response time: {{ (Math.random() * 10).toPrecision(2) }}h</span>
                    </div>
                  </div>
                </span>
                <span class="col-span-2 inline-flex ml-auto items-center px-2 py-0.5 rounded text-xs font-medium bg-primary-100 text-primary-700 w-full">
                  <BookmarkIcon class="w-4 h-4 mr-1" />
                  <span class="flex-shrink-0 truncate">{{ member.mainTopic }}</span>
                </span>
                <p class="col-span-2 px-2 inline-flex ml-auto leading-5 font-medium rounded-full text-primary text-xl items-baseline">
                  <span>{{ member.helpfulness.percentage }}%</span>
                  <span class="text-gray-400 text-xs font-normal">/{{ member.helpfulness.count }}</span>
                  <ThumbUpIcon class="w-5 h-5 ml-1 self-end" />
                </p>
              </div>
            </div>
          </li>
        </ul>
      </div>

      <!-- Some basic stats -->
      <dl class="flex space-x-4 col-span-1 sm:col-span-2 w-full items-start">
        <div v-for="item in stats" :key="item.name" class="px-4 py-3 rounded-lg border w-full">
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
    </div>
  </section>
</template>

<script>
import axios from 'axios'
import { ArrowSmDownIcon, ArrowSmUpIcon, BookmarkIcon, ThumbUpIcon } from '@heroicons/vue/solid'

const stats = [
  { name: 'Average time to respond', stat: '2.3h', previousStat: '2.4h', change: '3.15%', changeDirection: 'down', changeType: 'increase' },
  { name: 'Average Tickets per user', stat: '2.4', previousStat: '', change: '', changeDirection: '', changeType: 'decrease' }
]

export default {
  name: 'InsightsStaff',
  components: {
    ArrowSmDownIcon,
    ArrowSmUpIcon,
    BookmarkIcon,
    ThumbUpIcon
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

    const testTopics = ['Assignment 1 van het boek over meganica', 'Lecture', 'Slides', 'Code']

    /* Getting the staff data. */
    const staffResponse = await axios.get(`/api/inboxes/${inboxId}/staff`)
    this.staff = staffResponse.data.map(member => {
      return {
        name: member.first_name + ' ' + member.last_name,
        helpfulness: {
          percentage: (Math.random() * 50 + 50).toPrecision(3),
          count: Math.floor(Math.random() * 90)
        },
        image: member.avatar_url,
        mainTopic: testTopics[Math.floor(Math.random() * testTopics.length)]
      }
    })
  }
}
</script>
