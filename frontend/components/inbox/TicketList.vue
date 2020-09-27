<template>
  <div v-if="ticketList.length !== 0" class="flex flex-col flex-1 rounded" :id="title">
    <div
      class="py-1 mb-2 text-center bg-white sticky z-0"
      :class="{ 'border-b-2': top, 'border rounded mx-4': !top }"
      :style="`border-color: ${color}; top: 64px;`"
      @scroll.passive="handleScroll"
    >
      <p>{{ title }} (<strong>{{ ticketList.length }}</strong>)</p>

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

    <div class="mx-4 space-y-2 text-center" :id="`${title}-tickets`">
      <ticket-card
        :key="ticket.id"
        :ticket="ticket"
        :assignee_show="title !== 'Pending'"
        class="text-left"
        v-for="ticket in ticketList"/>
    </div>
  </div>
</template>

<script>
  import TicketCard from "./TicketCard";
  export default {
    components: {TicketCard},
    name: "TicketColumn",
    props: ['title', 'color', 'ticketList'],
    data: () => ({
      top: false
    }),
    mounted() {
      const self = this
      if (this.ticketList.length === 0) return

      window.addEventListener('scroll', function() {
        const element = this.document.getElementById(self.title)
        const coords = element.getBoundingClientRect()
        self.top = coords.top < 64
      })
    }
  }
</script>
