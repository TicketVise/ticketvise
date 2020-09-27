<template>
  <div>
    <h3 class="text-lg leading-6 font-medium text-gray-900 px-4 pb-1 pt-4">
      Graphs
    </h3>

    <div class="grid grid-cols-1 sm:grid-cols-2 mb-2 gap-4">
      <div class="shadow p-3">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Number of tickets per day
        </h3>
        <tickets-chart />
      </div>
      <div class="shadow p-3">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Number of tickets per hour
        </h3>
        <tickets-chart type="hour" />
      </div>
      <div class="shadow p-3">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Average response time
        </h3>
        <agent-response-time-chart/>
      </div>
      <div class="shadow p-3">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Label usage
        </h3>
        <labels-chart/>
      </div>
    </div>
  </div>
</template>

<script>
  import TicketsChart from "./TicketsChart";
  import AgentResponseTimeChart from "./AgentResponseTimeChart";
  import LabelsChart from "./LabelsChart";
  import Card from "../elements/card/Card";

  export default {
    components: {Card, LabelsChart, AgentResponseTimeChart, TicketsChart},
  }
</script>

<style scoped>

</style>
