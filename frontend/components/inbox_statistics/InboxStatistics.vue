<template>
  <div class="flex flex-col">
    <div class="flex">
      <div class="w-1/2">
        <tickets-chart/>
      </div>
      <div class="w-1/2">
        <tickets-chart type="hour"/>
      </div>
    </div>
    <div class="flex">
      <div class="w-1/2">
        <agent-response-time-chart/>
      </div>
      <div class="w-1/2">
        <labels-chart/>
      </div>
    </div>
  </div>
</template>

<script>
import TicketsChart from "./TicketsChart";
import AgentResponseTimeChart from "./AgentResponseTimeChart";
import LabelsChart from "./LabelsChart";

export default {
  components: {LabelsChart, AgentResponseTimeChart, TicketsChart},
}
</script>

<style scoped>

</style>