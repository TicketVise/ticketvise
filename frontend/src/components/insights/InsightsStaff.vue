<template>
  <section aria-labelledby="tickets-heading">
    <h2 id="tickets-heading" class="sr-only">Ticket insights</h2>

    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <!-- Imformation about the staff. -->
      <div class="col-span-1 sm:col-span-2 border rounded-lg px-4 py-2">
        <h2 class="text-lg font-semibold text-primary-600">Staff overview</h2>
        <ul role="list" class="divide-y divide-gray-200">
          <li v-for="member in statsData.staff?.sort((a, b) => b.helpfulness - a.helpfulness)" :key="member">
            <div class="p-3">
              <div class="grid grid-cols-8 gap-2 items-center justify-between w-full">
                <span class="col-span-4 inline-flex items-center px-2 rounded-full text-sm text-gray-800 truncate space-x-2">
                  <img class="inline-block h-8 w-8 rounded-full mr-2" :src="member.avatar_url" alt="" />
                  <div class="flex flex-col">
                    <span class="truncate text-base font-semibold leading-none">{{ member.first_name }} {{ member.last_name }}</span>
                    <div class="space-x-2">
                      <span class="text-gray-600 leading-none">Tickets: {{ member.tickets_count }}</span>
                      <span v-if="member.tickets_count > 0" class="text-gray-600 leading-none">Response time: {{ member.avg_response_time }}h</span>
                    </div>
                  </div>
                </span>
                <span v-if="member.tickets_count > 0" class="relative col-span-2 inline-flex mr-auto items-center px-2 py-0.5 rounded text-xs font-medium bg-primary-100 text-primary-700 max-w-full">
                  <BookmarkIcon class="flex-shrink-0 w-4 h-4 mr-1" />
                  <span class="truncate">{{ member.most_answered_label.name }}</span>
                </span>
                <p v-if="member.tickets_count > 0" class="col-span-2 px-2 inline-flex ml-auto leading-5 font-medium rounded-full text-primary text-xl items-baseline">
                  <span>{{ parseInt(member.helpfulness) }}%</span>
                  <span class="text-gray-400 text-xs font-normal">/{{ member.amount_of_helpful_comments }}</span>
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

export default {
  name: 'InsightsStaff',
  components: {
    ArrowSmDownIcon,
    ArrowSmUpIcon,
    BookmarkIcon,
    ThumbUpIcon
  },
  data: () => ({
    statsData: [],
    staff: []
  }),
  async mounted () {
    const { inboxId } = this.$route.params

    /* Gettings general statistics. */
    const statsResponse = await axios.get(`/api/inboxes/${inboxId}/statistics/staff`)
    this.statsData = statsResponse.data
  },
  computed: {
    stats () {
      return [
        { name: 'Average time to respond', stat: (this.statsData?.avg_response_time || 0) + 'h', previousStat: '', change: '', changeType: 'increase' },
        { name: 'Average Tickets per staff', stat: this.statsData?.avg_tickets_per_staff || 0, previousStat: '', change: '', changeType: 'increase' }
      ]
    }
  }
}
</script>
