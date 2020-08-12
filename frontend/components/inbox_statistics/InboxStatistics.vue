<template>
  <div>
    <div class="flex">
      <div class="w-1/2">
        <tickets-chart/>
      </div>

      <div class="w-1/2">
        <tickets-chart/>
      </div>
    </div>
  </div>
</template>

<script>
import TicketsChart from "./TicketsChart";

export default {
  components: {TicketsChart},
}
</script>

<style scoped>

</style>