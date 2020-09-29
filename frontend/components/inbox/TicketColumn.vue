<template>
  <div
    class="flex flex-col flex-1 border rounded border-gray-700 border-opacity-50 border-t-0 bg-gray-100 ticket-column"
    :id="title"
  >
    <div class="py-1 text-center border-t-2 bg-white rounded-tl rounded-tr" :style="`border-color: ${color};`">
      <p v-if="title === 'Closed'">{{ title }}</p>
      <p v-else>{{ title }} (<strong>{{ ticketList.length }}</strong>)</p>

      <div class="is-marginless pretty p-icon p-round select-column" style="display: none;">
        <input
          :id="`select-column-${title}`"
          :value="title"
          autocomplete="off"
          class="select-column-checkbox"
          name="select-column-checkbox"
          type="checkbox"/>
        <div class="state">
          <i class="icon fa fa-check"></i>
          <label></label>
        </div>
      </div>
    </div>

    <div class="flex-grow border-t border-gray-700 border-opacity-50 overflow-y-auto">
      <div class="p-2 space-y-2" :id="`${title}-tickets`">
        <ticket-card
          :key="ticket.id"
          :ticket="ticket"
          :assignee_show="title !== 'Pending'"
          v-for="ticket in ticketList"/>
      </div>
    </div>
  </div>
</template>

<script>
  import TicketCard from "./TicketCard";
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
  export default {
    components: {TicketCard, FontAwesomeIcon},
    name: "TicketColumn",
    props: ['title', 'color', 'ticketList']
  }
</script>

<style>
.ticket-column {
  height: calc((100vh - 255px) - 3rem);
}
@media screen and (min-width: 640px) {
  .ticket-column {
    height: calc((100vh - 263px) - 3rem);
  }
}
@media screen and (min-width: 1024px) {
  .ticket-column {
    height: calc((100vh - 214px) - 3rem);
  }
}
</style>
