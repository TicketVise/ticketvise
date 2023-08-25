<template>
  <section aria-labelledby="tickets-heading">
    <h2 id="tickets-heading" class="sr-only">Label insights</h2>

    <!-- Some basic stats first -->
    <div class="grid w-full grid-cols-2 sm:grid-cols-4 gap-4 mb-4">
      <div class="flex items-center overflow-hidden rounded-lg border bg-white p-2 px-4">
        <div class="hidden flex-shrink-0 sm:flex">
          <TagIcon class="h-6 w-6 text-gray-400" />
        </div>
        <dl class="w-0 flex-1 sm:ml-5">
          <dt class="truncate text-sm font-medium text-gray-500">Most used label</dt>
          <dd class="flex items-center justify-between">
            <div class="text-xl font-medium text-primary truncate">
              {{ this.labels[0]?.name || '' }}
            </div>
          </dd>
        </dl>
      </div>

      <div class="flex items-center overflow-hidden rounded-lg border bg-white p-2 px-4">
        <div class="hidden flex-shrink-0 sm:flex">
          <TicketIcon class="h-6 w-6 text-gray-400" />
        </div>
        <dl class="w-0 flex-1 sm:ml-5">
          <dt class="truncate text-sm font-medium text-gray-500">Tickets without a label</dt>
          <dd class="flex items-center justify-between">
            <div class="text-xl font-medium text-primary truncate">
              {{ 12 }}
            </div>
          </dd>
        </dl>
      </div>

      <div class="flex items-center overflow-hidden rounded-lg border bg-white p-2 px-4">
        <div class="hidden flex-shrink-0 sm:flex">
          <ExclamationTriangleIcon class="h-6 w-6 text-gray-400" />
        </div>
        <dl class="w-0 flex-1 sm:ml-5">
          <dt class="truncate text-sm font-medium text-gray-500">Unused labels</dt>
          <dd class="flex items-center justify-between">
            <div class="text-xl font-medium text-primary truncate">
              {{ this.labels?.filter(l => l.count === 0)?.length || 0 }}
            </div>
          </dd>
        </dl>
      </div>

      <div class="flex items-center overflow-hidden rounded-lg border bg-white p-2 px-4">
        <div class="hidden flex-shrink-0 sm:flex">
          <HashtagIcon class="h-6 w-6 text-gray-400" />
        </div>
        <dl class="w-0 flex-1 sm:ml-5">
          <dt class="truncate text-sm font-medium text-gray-500">Number of labels</dt>
          <dd class="flex items-center justify-between">
            <div class="text-xl font-medium text-primary truncate">
              {{ labels?.length || 0 }}
            </div>
          </dd>
        </dl>
      </div>
    </div>

    <!-- Some basic stats first -->
    <!-- <dl class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <div v-for="item in stats" :key="item.name" class="px-4 py-3 rounded-lg border">
        <dt class="text-base font-normal text-gray-900">
          {{ item.name }}
        </dt>
        <dd class="flex justify-between items-baseline md:block lg:flex">
          <div class="flex items-baseline text-2xl font-semibold text-primary-600 w-full">
            <span class="truncate">{{ item.stat }}</span>
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
    </dl> -->

    <!-- Some general graphs here -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-4">
      <div class="col-span-1 border rounded p-4 pt-2 h-auto">
        <h2 class="text-lg font-semibold text-primary-600">Top 5 most used labels</h2>
        <ul role="list" class="divide-y divide-gray-200">
          <li v-for="label in labels.slice(0, 5)" :key="label.id">
            <div class="p-3">
              <div class="flex items-center justify-between">
                <span class="inline-flex items-center px-2 py-0.5 rounded-full text-sm font-medium text-gray-800 truncate">
                  <svg class="-ml-1 mr-1.5 h-4 w-4" :style="`color: ${label.color}`" fill="currentColor" viewBox="0 0 8 8">
                    <circle cx="4" cy="4" r="3" />
                  </svg>
                  <span class="truncate">{{ label.name }}</span>
                </span>
                <div class="ml-2 flex-shrink-0 flex">
                  <p class="px-2 inline-flex leading-5 font-semibold rounded-full text-gray-800">
                    {{ label.count }}
                  </p>
                </div>
              </div>
            </div>
          </li>
        </ul>
      </div>

      <div class="col-span-2 border rounded p-4 pt-2">
        <h2 class="text-lg font-semibold text-primary-600">Tickets per label</h2>
        <LineChart v-if="labelData" :data="labelData" :options="labelOptions" :height="300" />
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios'
import { ExclamationTriangleIcon, HashtagIcon, TagIcon, TicketIcon } from '@heroicons/vue/24/outline'
import { ArrowSmallDownIcon, ArrowSmallUpIcon } from '@heroicons/vue/24/solid'

import LineChart from '@/components/insights/LineChart.vue'

export default {
  name: 'InsightsLabels',
  components: {
    ArrowSmallDownIcon,
    ArrowSmallUpIcon,
    LineChart,
    TicketIcon,
    TagIcon,
    ExclamationTriangleIcon,
    HashtagIcon
},
  data: () => ({
    labels: [],
    labelData: null,
    labelOptions: {
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
    }
  }),
  async mounted () {
    const { inboxId } = this.$route.params
    /* Getting the labels data. */
    const labelResponse = await axios.get(`/api/inboxes/${inboxId}/statistics/labels/count`)
    this.labels = labelResponse.data

    /* Getting the tickets per label data. */
    const labelsResponse = await axios.get(`/api/inboxes/${inboxId}/statistics/tickets/count`, {
      params: {
        date_type: 'labels'
      }
    })

    const base = labelsResponse.data.labels.map(label => ({
      date: label,
      total: 0
    }))
    this.labelData = {
      labels: labelsResponse.data.labels,
      datasets: labelsResponse.data?.datasets?.map(item => ({
        fill: false,
        label: item.label.name,
        backgroundColor: item.label.color,
        borderColor: item.label.color,
        data: base.map(b => item.data.find(d => d.date === b.date)?.total || 0)
      }))
    }
  },
  computed: {
    stats () {
      return [
        { name: 'Number of labels', stat: this.labels?.length || 0, previousStat: '', change: '', changeDirection: '', changeType: 'increase' },
        { name: 'Most used label', stat: this.labels[0]?.name || '', previousStat: '', change: '', changeDirection: '', changeType: 'increase' },
        { name: 'Tickets without a label', stat: '12', previousStat: '11', change: '9.15%', changeDirection: 'up', changeType: 'decrease' },
        { name: 'Unused labels', stat: this.labels?.filter(l => l.count === 0)?.length || 0, previousStat: '', change: '', changeDirection: '', changeType: 'decrease' }
      ]
    }
  }
}
</script>
