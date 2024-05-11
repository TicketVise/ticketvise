<template>
  <div class="p-4">
    <div class="flex justify-between items-center mb-1">
      <h2 class="text-lg font-semibold text-primary-600">Tickets</h2>
    </div>
    <VerticalBarChart v-if="data" :data="data" :options="options" :height="400" />
  </div>
</template>

<script>
import VerticalBarChart from '@/components/insights/VerticalBarChart.vue'

export default {
  name: 'UsersPerYear',
  components: { VerticalBarChart },
  props: {
    data: {
      type: Object,
      required: true
    }
  },
  data: () => ({
    options: {
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
  })
}
</script>
