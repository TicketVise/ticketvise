<template>
  <HorizontalBarChart
    v-if="data"
    :data="data"
    :options="options" />
</template>

<script>
import axios from 'axios'
import HorizontalBarChart from './HorizontalBarChart'
import moment from 'moment'

export default {
  components: { HorizontalBarChart },
  data: () => ({
    data: null,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      tooltips: {
        mode: 'index',
        intersect: false
      },
      hover: {
        mode: 'nearest',
        intersect: true
      },
      scales: {
        xAxes: [{
          display: true,
          scaleLabel: {
            display: true,
            labelString: 'Hours'
          },
          ticks: {
            suggestedMin: 0
          }
        }]
      }
    }
  }),
  async mounted () {
    const inboxId = this.$route.params.inboxId
    const response = await axios.get(`/api/inboxes/${inboxId}/statistics/agent/response/avg`)
    this.data = {
      labels: response.data.map(item => item.first_name + ' ' + item.last_name),
      datasets: [
        {
          fill: false,
          label: 'Response time',
          backgroundColor: '#ed8936',
          data: response.data.map(item => moment.duration(item.avg_response_time).asHours().toFixed(2))
        }
      ]
    }
  }
}
</script>
