<template>
  <div class="flex flex-col flex-1 rounded ticket-column" :id="title">
    <div class="pb-1 border-b-2 bg-white rounded-tl rounded-tr" :style="`border-color: ${color};`">
      <span class="text-lg font-medium">{{ title }}</span>
      <span v-if="title != 'Closed'" class="text-xs">({{ length }})</span>
    </div>

    <div class="flex-grow overflow-y-auto">
      <div class="pt-2 space-y-2" :id="`${title}-tickets`">
        <ticket-card
          :key="ticket.id"
          :ticket="ticket"
          :assignee_show="title !== 'Pending'"
          v-for="ticket in ticketList"/>

        <div v-if="!ticketList" class="space-y-2">
          <div v-for="i of length" :key="i" class="h-24 w-full bg-gray-200 rounded"/>
        </div>

        <div v-if="has_next" class="flex justify-center">
          <submit-button @click="$emit('input')" class="bg-white">
            Load More
          </submit-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import TicketCard from "./TicketCard";
  import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'
  import SubmitButton from "../elements/buttons/SubmitButton";

  export default {
    components: {SubmitButton, TicketCard, FontAwesomeIcon},
    name: "TicketColumn",
    props: ['title', 'color', 'ticketList', "has_next", "length"]
  }
</script>

<style>
  .ticket-column {
    min-width: calc(100vw - 64px - 16px) !important;
    height: calc((100vh - 218px) - 3rem);
  }

  @media screen and (min-width: 500px) {
    .ticket-column {
      min-width: 300px !important;
    }
  }

  @media screen and (min-width: 768px) {
    .ticket-column {
      height: calc((100vh - 106px) - 3rem);
    }
  }
</style>
