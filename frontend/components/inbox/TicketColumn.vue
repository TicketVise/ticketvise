<template>
  <div
    class="flex flex-col flex-1 border rounded border-gray-700 border-opacity-50 border-t-0 bg-gray-100 ticket-column"
    :id="title"
  >
    <div class="py-1 text-center border-t-2 bg-white rounded-tl rounded-tr" :style="`border-color: ${color};`">
      <p v-if="title === 'Closed'">{{ title }}</p>
      <p v-else>{{ title }} (<strong>{{ length }}</strong>)</p>
    </div>

    <div class="flex-grow border-t border-gray-700 border-opacity-50 overflow-y-auto">
      <div class="p-2 space-y-2" :id="`${title}-tickets`">
        <ticket-card
          :key="ticket.id"
          :ticket="ticket"
          :assignee_show="title !== 'Pending'"
          v-for="ticket in ticketList"/>

        <submit-button v-if="has_next" @click="$emit('input')">Load More</submit-button>
      </div>
    </div>
  </div>
</template>

<script>
  import TicketCard from "./TicketCard";
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
  import SubmitButton from "../elements/buttons/SubmitButton";
  export default {
    components: {SubmitButton, TicketCard, FontAwesomeIcon},
    name: "TicketColumn",
    props: ['title', 'color', 'ticketList', "has_next", "length"]
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
@media screen and (min-width: 768px) {
  .ticket-column {
    height: calc((100vh - 213px) - 3rem);
  }
}
</style>
