<template>
  <div class="flex flex-col mb-3 space-y-4">
    <div class="flex space-x-4">
      <card outlined class="w-1/2 p-3">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Number of tickets per day
        </h3>
        <tickets-chart/>
      </card>
      <card outlined class="w-1/2 p-3">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Number of tickets per hour
        </h3>
        <tickets-chart type="hour"/>
      </card>
    </div>
    <div class="flex space-x-4">
      <card outlined class="w-1/2 p-3">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Average response time
        </h3>
        <agent-response-time-chart/>
      </card>
      <card outlined class="w-1/2 p-3">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Label usage
        </h3>
        <labels-chart/>
      </card>
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