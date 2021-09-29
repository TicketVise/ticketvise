<template>
  <VerticalBarChart
    v-if="data"
    :data="data"
    :options="options"
    :height="this.height ? this.height : 400" />
</template>

<script>
  import VerticalBarChart from './VerticalBarChart'
  import axios from 'axios'

  export default {
    components: { VerticalBarChart },
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
    data () {
      return {
        data: null
      }
    },
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
    },
    computed: {
      options () {
        return {
          legend: {
            display: this.data?.datasets?.length > 1 || false
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
      }
    }
  }
</script>
