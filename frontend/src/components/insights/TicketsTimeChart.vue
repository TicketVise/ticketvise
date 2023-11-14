<template>
  <VerticalBarChart
    v-if="chartData"
    :data="chartData"
    :options="options"
    :height="this.height ? this.height : 400" />
</template>

<script>
  import VerticalBarChart from './VerticalBarChart.vue'
  import axios from 'axios'

  export default {
    components: { VerticalBarChart },
    props: {
      type: {
        type: String,
        default: 'hour'
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
        chartData: null
      }
    },
    async mounted () {
      this.get_data(this.type)
    },
    methods: {
      async get_data(type) {
        const url = this.inboxId
          ? `/api/inboxes/${this.inboxId}/statistics/tickets/count`
          : '/api/admin/statistics/tickets/count'

        const response = await axios.get(url, {
          params: {
            date_type: type
          }
        })

        let labels = response.data.map(item => item.date)

        if (type == 'week_day')
          labels = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

        this.chartData = {
          labels: labels,
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
    },
    watch: {
      type () {
        this.chartData = null
        this.get_data(this.type)
      }
    },
    computed: {
      options () {
        return {
          legend: {
            display: this.chartData?.datasets?.length > 1 || false
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
