<template>
  <div class="flex flex-col flex-1 rounded" :id="title">
    <div
            class="py-1 mb-2 text-center bg-white sticky z-0"
            :class="{ 'border-b-2': top, 'border rounded mx-4': !top }"
            :style="`border-color: ${color}; top: 0px;`"
            @scroll.passive="handleScroll"
    >
      <p v-if="title === 'Closed'">{{ title }}</p>
      <p v-else>{{ title }} (<strong>{{ ticketList.length }}</strong>)</p>
    </div>


    <div class="mx-4 space-y-2 text-center" :id="`${title}-tickets`">
      <ticket-card
              :key="ticket.id"
              :ticket="ticket"
              :assignee_show="title !== 'Pending'"
              class="text-left"
              v-for="ticket in ticketList"/>

      <span v-if="ticketList.length === 0">No tickets in this status</span>
    </div>
  </div>
</template>

<script>
  import TicketCard from "./TicketCard";

  export default {
    components: {TicketCard},
    name: "TicketList",
    props: ['title', 'color', 'ticketList'],
    data: () => ({
      top: false
    }),
    created() {
      if (document.getElementById('scrollable-content')) {
        document.getElementById('scrollable-content').addEventListener('scroll', this.handleScroll);
      }
    },
    destroyed() {
      if (document.getElementById('scrollable-content')) {
        document.getElementById('scrollable-content').removeEventListener('scroll', this.handleScroll);
      }
    },
    methods: {
      handleScroll() {
        const element = document.getElementById(this.title);
        const coords = element.getBoundingClientRect();
        this.top = coords.top <= 64
      }
    }
  }
</script>
