<template>
  <line-chart
      v-if="data"
      :data="data"
      :options="options"/>
</template>

<script>
import LineChart from "./LineChart";
import axios from "axios";

export default {
  components: {LineChart},
  props: {
    type: {
      type: String,
      default: "day"
    }
  },
  data: () => ({
    data: null,
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  }),
  async mounted() {
    const response = await axios.get("/api" + window.location.pathname + "/tickets/count", {
      params: {        "date_type": this.type
      }
    });
    this.data = {
      labels: response.data.map(item => item.date),
      datasets: [
        {
          fill: false,
          label: "Tickets",
          backgroundColor: '#f87979',
          data: response.data.map(item => item.total)
        }
      ]
    }
  }
}
</script>

<style scoped>

</style>