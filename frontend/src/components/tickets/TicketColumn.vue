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
          :assignee_show="title !== 'Pending'"
          v-for="ticket in ticketList"
          v-on:refresh="$emit('refresh')" />

        <div v-if="!ticketList" class="space-y-2">
          <div v-for="i of length" :key="i" class="h-24 w-full bg-gray-200 rounded"/>
        </div>

        <div v-if="has_next" class="flex justify-center py-4">
          <button @click="$emit('input')" class="text-primary font-semibold text-sm">
            Load More
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import TicketCard from '@/components/tickets/TicketCard.vue'
  // import SubmitButton from '../elements/buttons/SubmitButton'

  export default {
    components: { TicketCard },
    name: 'TicketColumn',
    props: ['title', 'color', 'ticketList', 'has_next', 'length']
  }
</script>

<style>
  .ticket-column {
    min-width: calc(100vw - 64px - 32px) !important;
    /* height: calc((100vh - 216px) - 3rem); */
    scroll-snap-align: start;
  }

  @media screen and (min-width: 500px) {
    .ticket-column {
      min-width: 300px !important;
    }
  }

  @media screen and (min-width: 768px) {
    .ticket-column {
      /* height: calc((100vh - 92px - 16px) - 3rem); */
    }
  }
</style>
