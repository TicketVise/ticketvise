<template>
  <div class="flex flex-col">
    <div class="flex">
      <div class="w-1/2">
        <tickets-chart/>
      </div>
      <div class="w-1/2">
        <tickets-chart/>
      </div>
    </div>
    <div class="flex">
      <div class="w-1/2">
        <agent-response-time-chart/>
      </div>
      <div class="w-1/2">
        <tickets-chart/>
      </div>
    </div>
  </div>
</template>

<script>
import TicketsChart from "./TicketsChart";
import AgentResponseTimeChart from "./AgentResponseTimeChart";

export default {
  components: {AgentResponseTimeChart, TicketsChart},
}
</script>

<style scoped>

</style>