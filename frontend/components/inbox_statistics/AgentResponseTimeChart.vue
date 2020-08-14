<template>
  <bar-chart
      v-if="data"
      :data="data"
      :options="options"/>
</template>

<script>
import LineChart from "./LineChart";
import axios from "axios";
import BarChart from "./BarChart";
import moment from "moment";

export default {
  components: {BarChart},
  data: () => ({
    data: null,
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  }),
  async mounted() {
    const response = await axios.get("/api" + window.location.pathname + "/agent/response/avg");
    this.data = {
      labels: response.data.map(item => item.first_name ),
      datasets: [
        {
          fill: false,
          label: "Tickets",
          backgroundColor: '#f87979',
          data: response.data.map(item => moment.duration(item.avg_response_time).minutes())
        }
      ]
    }
  }
}
</script>

<style scoped>

</style>