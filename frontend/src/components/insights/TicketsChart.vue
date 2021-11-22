<template>
  <line-chart
    v-if="data"
    :data="data"
    :options="options"
    :height="this.height ? this.height : 400" />
</template>

<script>
  import LineChart from './LineChart'
  import axios from 'axios'

  export default {
    components: { LineChart },
    props: {
      type: {
        type: String,
        default: 'date'
      },
      inboxId: {
        required: false,
        default: null
      },
      height: {
        type: Number,
        required: false
      }
    },
    data: () => ({
      data: null,
      options: {
        legend: {
          display: false
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
      const url = this.inboxId
          ? `/api/inboxes/${this.inboxId}/statistics/tickets/count`
          : '/api/admin/statistics/tickets/count'

      const response = await axios.get(url, {
        params: {
          date_type: this.type
        }
      })
      this.data = {
        labels: response.data.map(item => item.date),
        datasets: [
          {
            fill: false,
            label: 'Tickets',
            backgroundColor: '#ed8936',
            borderColor: '#fbd38d',
            data: response.data.map(item => item.total)
          }
        ]
      }
    }
  }
</script>
