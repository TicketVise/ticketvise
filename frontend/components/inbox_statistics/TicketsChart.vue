<template>
  <line-chart
      v-if="data"
      :data="data"
      :options="options"/>
</template>

<script>
import LineChart from "./LineChart";
import axios from "axios";
import moment from "moment";

export default {
  components: {LineChart},
  props: {
    type: {
      type: String,
      default: "date"
    }
  },
  data: () => ({
    data: null,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      tooltips: {
        mode: 'nearest',
        intersect: false,
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
            labelString: 'Minutes'
          }
        }],
      }
    }
  }),
  async mounted() {
    const response = await axios.get("/api" + window.location.pathname + "/tickets/count", {
      params: {
        "date_type": this.type
      }
    });
    this.data = {
      labels: response.data.map(item => {
        if (this.type === "hour"){
          return moment(item.date).hour()
        }

        return item.date
      }),
      datasets: [
        {
          fill: false,
          label: "Tickets",
          backgroundColor: '#ed8936',
          borderColor: '#fbd38d',
          data: response.data.map(item => item.total)
        }
      ]
    }
  },
}
</script>

<style scoped>

</style>