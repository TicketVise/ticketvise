<template>
  <div class="flex flex-col flex-1 rounded ticket-column" :id="title">
    <div class="pb-1 border-b-2 bg-white dark:bg-transparent dark:text-white rounded-tl rounded-tr" :style="`border-color: ${color};`">
      <span class="text-lg font-medium">{{ title }}</span>
      <span>{{ ' ' }}</span>
      <span v-if="title != 'Closed'" class="text-xs">({{ length }})</span>
    </div>

    <div class="flex-grow overflow-y-auto">
      <div class="pt-2 space-y-2 pb-2" :id="`${title}-tickets`">
        <ticket-card
          :key="ticket.id"
          :ticket="ticket"
          :assignee_show="true"
          v-for="ticket in ticketList"
          v-on:refresh="$emit('refresh')" />

        <div v-if="!ticketList" class="space-y-2">
          <div v-for="i of length" :key="i" class="h-24 w-full bg-gray-200 rounded"/>
        </div>

        <div v-if="has_next" class="flex justify-center py-4">
          <button @click="$emit('input')" class="flex items-center text-primary font-semibold text-sm">
            <ChevronDownIcon class="w-4 h-4 inline-block mr-1" />
            Load More
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import TicketCard from '@/components/tickets/TicketCard.vue'
  import { ChevronDownIcon } from '@heroicons/vue/24/outline';
  // import SubmitButton from '../elements/buttons/SubmitButton'

  export default {
    components: { TicketCard, ChevronDownIcon },
    name: 'TicketColumn',
    props: ['title', 'color', 'ticketList', 'has_next', 'length']
  }
</script>

<style>
  .ticket-column {
    min-width: calc(100vw - 32px) !important;
    scroll-snap-align: start;
  }

  @media screen and (min-width: 500px) {
    .ticket-column {
      min-width: 300px !important;
    }
  }
</style>
