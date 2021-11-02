<template>
  <section aria-labelledby="tickets-heading">
    <h2 id="tickets-heading" class="sr-only">General insights</h2>

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
            <ArrowSmUpIcon v-if="item.changeType === 'increase'" class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5 text-green-500" aria-hidden="true" />
            <ArrowSmDownIcon v-else class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5 text-red-500" aria-hidden="true" />
            <span class="sr-only"> {{ item.changeType === 'increase' ? 'Increased' : 'Decreased' }} by </span>
            {{ item.change }}
          </div>
        </dd>
      </div>
    </dl>

    <!-- Some general graphs here -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-4">
      <div class="col-span-2 border rounded-lg p-4 pt-2">
        <h2 class="text-lg font-semibold text-primary-600">Tickets over time</h2>
        <LineChart v-if="ticketsData" :data="ticketsData" :options="ticketsOptions" :height="400" />
      </div>
      <div class="col-span-1 border rounded-lg p-4 pt-2">
        <h2 class="text-lg font-semibold text-primary-600">Label usage</h2>
        <DoughnutChart v-if="labelsData" :data="labelsData" :options="labelsOptions" />
      </div>
      <div class="col-span-1 flex flex-col space-y-4">
        <div class="border rounded-lg px-4 py-3">
          <h2 class="text-base font-normal text-gray-900">Average time before first anwser</h2>
          <div class="flex items-baseline text-2xl font-semibold text-primary-600">5h</div>
        </div>
        <div class="border rounded-lg px-4 py-3">
          <h2 class="text-base font-normal text-gray-900">Average times of ticket is closed</h2>
          <div class="flex items-baseline text-2xl font-semibold text-primary-600">5h</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios'
import { ArrowSmDownIcon, ArrowSmUpIcon } from '@heroicons/vue/solid'

import LineChart from '@/components/insights/LineChart'
import DoughnutChart from '@/components/insights/DoughnutChart'

export default {
  name: 'InsightsGeneral',
  components: {
    ArrowSmDownIcon,
    ArrowSmUpIcon,
    DoughnutChart,
    LineChart
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
