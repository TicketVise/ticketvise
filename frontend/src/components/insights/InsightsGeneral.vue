<template>
  <section aria-labelledby="tickets-heading">
    <h2 id="tickets-heading" class="sr-only">General insights</h2>

    <!-- Some basic stats first -->
    <!-- <dl class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
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
            <ArrowSmallUpIcon v-if="item.changeType === 'increase'" class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5 text-green-500" aria-hidden="true" />
            <ArrowSmallDownIcon v-else class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5 text-red-500" aria-hidden="true" />
            <span class="sr-only"> {{ item.changeType === 'increase' ? 'Increased' : 'Decreased' }} by </span>
            {{ item.change }}
          </div>
        </dd>
      </div>
    </dl> -->

    <!-- Some general graphs here -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 w-full">
      <div class="overflow-hidden rounded-lg border bg-white">
        <div class="p-2 px-4">
          <div class="flex items-center">
            <div class="hidden flex-shrink-0 sm:flex">
              <StarIcon class="h-6 w-6 text-gray-400" />
            </div>
            <div class="w-0 flex-1 sm:ml-5">
              <dl>
                <dt class="truncate text-sm font-medium text-gray-500">Helpfulness</dt>
                <dd class="flex items-center justify-between">
                  <div class="text-xl font-medium text-primary">
                    85%
                    <span class="ml-1 hidden text-sm font-medium text-gray-500 lg:inline"> from 71% last week </span>
                  </div>

                  <div :class="['increase' === 'increase' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800', 'inline-flex items-baseline rounded-full px-2.5 py-0.5 text-sm font-medium md:mt-2 lg:mt-0']">
                    <ArrowSmallUpIcon v-if="'up' === 'up'" class="-ml-1 mr-0.5 h-5 w-5 flex-shrink-0 self-center" :class="['increase' === 'increase' ? 'text-green-500' : 'text-red-500']" aria-hidden="true" />
                    <ArrowSmallDownIcon v-else class="-ml-1 mr-0.5 h-5 w-5 flex-shrink-0 self-center" :class="['increase' === 'increase' ? 'text-green-500' : 'text-red-500']" aria-hidden="true" />
                    <span class="sr-only"> {{ 'increase' === 'increase' ? 'Increased' : 'Decreased' }} by </span>
                    33%
                  </div>
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
      <div class="overflow-hidden rounded-lg border bg-white">
        <div class="p-2 px-4">
          <div class="flex items-center">
            <div class="hidden flex-shrink-0 sm:flex">
              <ChatBubbleLeftRightIcon class="h-6 w-6 text-gray-400" />
            </div>
            <div class="w-0 flex-1 sm:ml-5">
              <dl>
                <dt class="truncate text-sm font-medium text-gray-500">Average response time</dt>
                <dd class="flex items-center justify-between">
                  <div class="text-xl font-medium text-primary">
                    7.9h
                    <span class="ml-1 hidden text-sm font-medium text-gray-500 lg:inline"> from 6.2h last week </span>
                  </div>

                  <div :class="['decrease' === 'increase' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800', 'inline-flex items-baseline px-2.5 py-0.5 rounded-full text-sm font-medium md:mt-2 lg:mt-0']">
                    <ArrowSmallUpIcon v-if="'up' === 'up'" class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5" :class="['decrease' === 'increase' ? 'text-green-500' : 'text-red-500']" aria-hidden="true" />
                    <ArrowSmallDownIcon v-else class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5" :class="['increase' === 'increase' ? 'text-green-500' : 'text-red-500']" aria-hidden="true" />
                    <span class="sr-only"> {{ 'increase' === 'increase' ? 'Increased' : 'Decreased' }} by </span>
                    27%
                  </div>
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
      <div class="col-span-2 sm:col-span-1 overflow-hidden rounded-lg border bg-white">
        <div class="p-2 px-4">
          <div class="flex items-center">
            <div class="hidden flex-shrink-0 sm:flex">
              <HashtagIcon class="h-6 w-6 text-gray-400" />
            </div>
            <div class="w-0 flex-1 sm:ml-5">
              <dl>
                <dt class="truncate text-sm font-medium text-gray-500">Frequent terms</dt>
                <dd class="flex items-center justify-between">
                  <div class="text-lg font-medium text-primary">
                    Swebok, Demo, Individual report
                  </div>
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
      <div class="hidden sm:block overflow-hidden rounded-lg border bg-white">
        <div class="p-2 px-4">
          <div class="flex items-center">
            <div class="hidden flex-shrink-0 sm:flex">
              <DocumentTextIcon class="h-6 w-6 text-gray-400" />
            </div>
            <div class="w-0 flex-1 sm:ml-5">
              <dl>
                <dt class="truncate text-sm font-medium text-gray-500">Number of tickets</dt>
                <dd class="flex items-center justify-between">
                  <div class="text-xl font-medium text-primary">
                    214
                  </div>
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="col-span-2 border rounded-lg p-4 pt-2">
        <h2 class="text-lg font-semibold text-primary-600">Tickets over time</h2>
        <LineChart v-if="ticketsData" :data="ticketsData" :options="ticketsOptions" :height="250" />
      </div>
      <div class="col-span-2 sm:col-span-1 border rounded-lg p-4 pt-2">
        <h2 class="text-lg font-semibold text-primary-600">Label usage</h2>
        <DoughnutChart class="h-full" v-if="labelsData" :data="labelsData" :options="labelsOptions" />
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios'
import { StarIcon, HashtagIcon, ChatBubbleLeftRightIcon, DocumentTextIcon } from '@heroicons/vue/24/outline'
import { ArrowSmallDownIcon, ArrowSmallUpIcon } from '@heroicons/vue/24/solid'

import LineChart from '@/components/insights/LineChart.vue'
import DoughnutChart from '@/components/insights/DoughnutChart.vue'

export default {
  name: 'InsightsGeneral',
  components: {
    ArrowSmallDownIcon,
    ArrowSmallUpIcon,
    DoughnutChart,
    LineChart,
    StarIcon,
    HashtagIcon,
    ChatBubbleLeftRightIcon,
    DocumentTextIcon
  },
  data: () => ({
    statsData: null,
    ticketsData: null,
    ticketsOptions: {
      legend: {
        display: true
      },
      responsive: true,
      aspectRatio: 6,
      maintainAspectRatio: false,
      tooltips: {
        mode: 'nearest',
        intersect: false
      },
      hover: {
        mode: 'nearest',
        intersect: true
      },
      scales: {
        yAxes: [{
          display: true,
          ticks: {
            stepSize: 1
          }
        }]
      }
    },
    labelsData: null,
    labelsOptions: {
      responsive: true,
      maintainAspectRatio: false
    }
  }),
  async mounted () {
    const { inboxId } = this.$route.params

    /* Gettings general statistics. */
    const statsResponse = await axios.get(`/api/inboxes/${inboxId}/statistics`)
    this.statsData = statsResponse.data

    /* Getting the tickets data. */
    const ticketResponse = await axios.get(`/api/inboxes/${inboxId}/statistics/tickets/count`, {
      params: {
        date_type: 'date'
      }
    })
    this.ticketsData = {
      labels: ticketResponse.data.map(item => item.date),
      datasets: [
        {
          fill: false,
          label: 'Private Tickets',
          backgroundColor: '#ed8936',
          borderColor: '#fbd38d',
          data: ticketResponse.data.map(item => item.total)
        },
        {
          fill: false,
          label: 'Public Tickets',
          backgroundColor: '#38b01c',
          borderColor: '#126e13',
          data: ticketResponse.data.map(item => item.public)
        }
      ]
    }

    /* Getting the labels data. */
    const labelResponse = await axios.get(`/api/inboxes/${inboxId}/statistics/labels/count`)
    this.labelsData = {
      labels: labelResponse.data.map(label => label.name),
      datasets: [
        {
          label: 'Labels',
          backgroundColor: labelResponse.data.map(label => label.color),
          data: labelResponse.data.map(label => label.count)
        }
      ]
    }
  },
  computed: {
    stats () {
      return [
        { name: 'Total Tickets', stat: this.statsData?.total_tickets || 0, previousStat: '', change: '', changeType: 'increase' },
        { name: 'Students', stat: this.statsData?.total_guests || 0, previousStat: '', change: '', changeType: 'increase' },
        { name: 'Staff members', stat: this.statsData?.users - this.statsData?.total_guests || 0, previousStat: '', change: '', changeType: 'decrease' },
        { name: 'Average Tickets per user', stat: this.statsData?.avg_ticket_per_student || 0, previousStat: '', change: '', changeType: 'decrease' }
      ]
    }
  }
}
</script>
