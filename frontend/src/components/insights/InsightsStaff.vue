<template>
  <section aria-labelledby="staff-heading" class="mx-auto flex max-w-3xl flex-col space-y-4 overflow-y-auto">
    <!-- Some basic stats -->
    <div class="grid w-full grid-cols-2 gap-4">
      <div class="flex items-center overflow-hidden rounded-lg border bg-white p-2 px-4">
        <div class="hidden flex-shrink-0 sm:flex">
          <InboxStackIcon class="h-6 w-6 text-gray-400" />
        </div>
        <dl class="w-0 flex-1 sm:ml-5">
          <dt class="truncate text-sm font-medium text-gray-500">Helpfulness</dt>
          <dd class="flex items-center justify-between">
            <div class="text-xl font-medium text-primary">
              {{ Math.round(statsData?.staff?.filter(s => s.amount_of_helpful_comments > 0).reduce((acc, cur) => acc + cur.helpfulness, 0) / statsData?.staff?.filter(s => s.amount_of_helpful_comments > 0).length) }}%
            </div>
          </dd>
        </dl>
      </div>

      <div class="flex items-center overflow-hidden rounded-lg border bg-white p-2 px-4">
        <div class="hidden flex-shrink-0 sm:flex">
          <ChatBubbleLeftRightIcon class="h-6 w-6 text-gray-400" />
        </div>
        <div class="w-0 flex-1 sm:ml-5">
          <dl>
            <dt class="truncate text-sm font-medium text-gray-500">Avg response time</dt>
            <dd class="flex items-center justify-between">
              <div class="text-xl font-medium text-primary">
                {{ statsData?.avg_response_time }}h
              </div>
            </dd>
          </dl>
        </div>
      </div>
    </div>

    <!-- <div class="rounded-md bg-yellow-50 p-4">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-yellow-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd" d="M8.485 3.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.17 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 3.495zM10 6a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0v-3.5A.75.75 0 0110 6zm0 9a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <h3 class="text-sm font-medium text-yellow-800">Response time is high</h3>
          <div class="mt-1 text-sm text-yellow-700 text-justify">
            <p>The response time on tickets is <strong>high</strong> for more than half of your staff. Try to encourage your staff to check their page more often to reduce the response time.</p>
            <p class="mt-1">You can check the <router-link :to="{ name: 'Insights', params: { inboxId: this.$route.params.inboxId, tab: 'tickets' } }" class="text-medium underline">ticket insights</router-link> to see what some good times are when students often ask questions.</p>
          </div>
        </div>
      </div>
    </div> -->

    <!-- Imformation about the staff. -->
    <div>
      <h2 class="text-lg font-semibold text-primary-600">Staff overview</h2>
      <ul role="list" class="divide-y divide-gray-200">
        <li v-for="member in statsData.staff?.sort((a, b) => b.tickets_count - a.tickets_count)" :key="member">
          <div class="py-3 flex space-x-1">
            <img class="mr-2 inline-block h-8 w-8 rounded-full" :src="member.avatar_url" alt="" />

            <div>
              <h3 class="text-gray-800 truncate text-base font-semibold leading-none">
                {{ member.first_name }} {{ member.last_name }}
              </h3>
              <div class="flex flex-wrap mt-2">
                <span class="flex space-x-1 items-center rounded-full bg-white border py-1 px-3 text-xs font-medium text-gray-900 mb-2 mr-2">
                  <TicketIcon class="h-4 w-4 flex-shrink-0 mr-1.5 text-gray-400" />
                  {{ member.tickets_count }}
                </span>
                <span v-if="member.tickets_count > 0" class="flex space-x-1 items-center rounded-full bg-white border py-1 pl-2 pr-3 text-xs font-medium text-gray-900 mb-2 mr-2">
                  <ClockIcon class="h-4 w-4 flex-shrink-0 mr-1.5 text-gray-400" />
                  {{ member.avg_response_time }}h
                </span>
                <span v-if="member.most_answered_label.name" class="flex space-x-1 items-center rounded-full bg-white border py-1 pl-2 pr-3 text-xs font-medium text-gray-900 mb-2 mr-2">
                  <TagIcon class="h-4 w-4 flex-shrink-0 mr-1.5 text-gray-400" />
                  {{ member.most_answered_label.name }}
                </span>
                <span v-if="member.tickets_count > 0 && member.amount_of_helpful_comments > 0" class="flex space-x-1 items-center rounded-full bg-white border py-1 px-3 text-xs font-medium text-gray-900 mb-2 mr-2">
                  <HandThumbUpIcon class="h-4 w-4 flex-shrink-0 mr-1.5 text-primary" />
                  {{ parseInt(member.helpfulness) }}%
                </span>
              </div>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </section>
</template>

<script>
import axios from 'axios'
import { InboxStackIcon, ChatBubbleLeftRightIcon } from '@heroicons/vue/24/outline'
import { ArrowSmallDownIcon, ArrowSmallUpIcon, BookmarkIcon } from '@heroicons/vue/24/solid'
import { ClockIcon, TagIcon, TicketIcon, HandThumbUpIcon } from '@heroicons/vue/20/solid'

export default {
  name: 'InsightsStaff',
  components: {
    ArrowSmallDownIcon,
    ArrowSmallUpIcon,
    BookmarkIcon,
    HandThumbUpIcon,
    InboxStackIcon,
    ChatBubbleLeftRightIcon,
    TicketIcon,
    ClockIcon,
    TagIcon
},
  data: () => ({
    statsData: [],
    staff: []
  }),
  async mounted() {
    const { inboxId } = this.$route.params

    /* Gettings general statistics. */
    const statsResponse = await axios.get(`/api/inboxes/${inboxId}/statistics/staff`)
    this.statsData = statsResponse.data
  }
}
</script>
