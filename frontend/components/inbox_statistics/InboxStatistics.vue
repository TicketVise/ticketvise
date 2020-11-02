<template>
  <div class="container mx-auto pt-4 sm:px-2 lg:px-4">
    <h3 class="text-lg leading-6 font-medium text-gray-900 px-4 pb-1" v-if="statistics">
      Last week
    </h3>

    <div class="sm:rounded shadow grid grid-cols-2 lg:grid-cols-4 mb-4" v-if="statistics">

      <div class="flex-grow border-r border-b lg:border-b-0 p-4">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Pending
        </h3>
        <div class="flex items-baseline mt-1">
          <h2 class="text-2xl font-medium text-orange-500">{{ statistics.current_week_pending }}</h2>
          <span class="ml-2 text-sm flex-grow text-gray-600">from {{ statistics.last_week_pending }} last week</span>
          <increase-label :a="statistics.current_week_pending" :b="statistics.last_week_pending" />
        </div>
      </div>
      <div class="flex-grow border-b lg:border-b-0 lg:border-r p-4">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Assigned
        </h3>
        <div class="flex items-baseline mt-1">
          <h2 class="text-2xl font-medium text-orange-500">{{ statistics.current_week_assigned }}</h2>
          <span class="ml-2 text-sm flex-grow text-gray-600">from {{ statistics.last_week_assigned }} last week</span>
          <increase-label :a="statistics.current_week_assigned" :b="statistics.last_week_assigned" />
        </div>
      </div>
      <div class="flex-grow p-4 border-r">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Answered
        </h3>
        <div class="flex items-baseline mt-1">
          <h2 class="text-2xl font-medium text-orange-500">{{ statistics.current_week_answered }}</h2>
          <span class="ml-2 text-sm flex-grow text-gray-600">from {{ statistics.last_week_answered }} last week</span>
          <increase-label :a="statistics.current_week_answered" :b="statistics.last_week_answered" />
        </div>
      </div>
      <div class="flex-grow p-4">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Closed
        </h3>
        <div class="flex items-baseline mt-1">
          <h2 class="text-2xl font-medium text-orange-500">{{ statistics.current_week_closed }}</h2>
          <span class="ml-2 text-sm flex-grow text-gray-600">from {{ statistics.last_week_closed }} last week</span>
          <increase-label :a="statistics.current_week_closed" :b="statistics.last_week_closed" />
        </div>
      </div>
    </div>

    <h3 class="text-lg leading-6 font-medium text-gray-900 px-4 pb-1 pt-4" v-if="statistics">
      Summary
    </h3>

    <div class="flex flex-col md:grid md:grid-cols-3 divide-y md:divide-y-0 md:divide-x shadow mb-4 sm:rounded" v-if="statistics">
      <div class="flex flex-wrap">
        <div class="grow p-4">
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            Total tickets
          </h3>
          <div class="flex items-baseline mt-1">
            <h2 class="text-2xl font-medium text-orange-500">{{ statistics.total_tickets }}</h2>
            <span class="ml-2 text-sm flex-grow text-gray-600">from {{ statistics.last_week_total_tickets }} last week</span>
          </div>
        </div>
      </div>

      <div class="flex-grow p-4">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Average response time
        </h3>
        <div class="flex items-baseline mt-1">
          <h2 class="text-2xl font-medium text-orange-500">{{ statistics.avg_response_time }} <span
              class="text-gray-600 text-sm font-normal">hours</span></h2>
        </div>
      </div>

      <div class="flex-grow p-4">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Active students
        </h3>
        <div class="flex items-baseline mt-1">
          <h2 class="text-2xl font-medium text-orange-500">{{ statistics.total_guests }}</h2>
        </div>
      </div>
    </div>

    <h3 class="text-lg leading-6 font-medium text-gray-900 px-4 pb-1 pt-4">
      Graphs
    </h3>

    <div class="grid grid-cols-1 sm:grid-cols-2 mb-2 gap-4">
      <div class="shadow p-3">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Number of tickets per day
        </h3>
        <tickets-chart/>
      </div>
      <div class="shadow p-3">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Number of tickets per hour
        </h3>
        <tickets-chart type="hour"/>
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
import axios from "axios";
import IncreaseLabel from "./IncreaseLabel";

export default {
  components: {IncreaseLabel, Card, LabelsChart, AgentResponseTimeChart, TicketsChart},
  data: () => ({
    statistics: null,
  }),
  async mounted() {
    const response = await axios.get("/api" + window.location.pathname);
    this.statistics = response.data
  }
}
</script>

<style scoped>

</style>
