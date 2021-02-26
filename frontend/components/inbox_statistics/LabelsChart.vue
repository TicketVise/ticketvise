<template>
  <doughnut-chart
      v-if="data"
      :data="data"
      :options="options"/>
</template>

<script>
import axios from "axios";
import DoughnutChart from "./DoughnutChart";

export default {
  components: {DoughnutChart},
  data: () => ({
    data: null,
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  }),
  async mounted() {
    const inboxId = this.$route.params.inboxId
    const response = await axios.get(`/api/inboxes/${inboxId}/statistics/labels/count`);
    this.data = {
      labels: response.data.map(label => label.name),
      datasets: [
        {
          label: "Labels",
          backgroundColor: response.data.map(label => label.color),
          data: response.data.map(label => label.count)
        }
      ]
    }
  }
}
</script>

<style scoped>

</style>