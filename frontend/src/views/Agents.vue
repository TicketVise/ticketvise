<template>
  <section class="flex h-full flex-grow dark:bg-gray-800 pt-2">
    <div class="ticket-columns max-w-full flex flex-grow overflow-x-auto pl-4">
      <ticket-column
        v-for="tickets in ticketsPerAssignee"
        :key="tickets[0].assignee.id"
        :title="
          tickets[0].assignee.first_name + ' ' + tickets[0].assignee.last_name
        "
        :ticket-list="tickets"
        :has_next="false"
        :length="tickets.length"
        class="min-w-3/4 sm:min-w-1/2 md:min-w-0 pr-4"
        v-on:refresh="loadTickets"
      />
    </div>
  </section>
</template>

<script>
import axios from "axios";
import _ from "lodash";
import moment from "moment";

import SearchBar from "@/components/searchbar/SearchBar.vue";
import TicketColumn from "@/components/tickets/TicketColumn.vue";
import LabelDropdown from "@/components/dropdown/LabelDropdown.vue";

import { ChevronRightIcon } from "@heroicons/vue/24/solid";
import { GlobeEuropeAfricaIcon } from "@heroicons/vue/24/outline";

export default {
  name: "Agents",
  components: {
    ChevronRightIcon,
    GlobeEuropeAfricaIcon,
    TicketColumn,
    LabelDropdown,
    SearchBar,
  },
  data: () => ({
    ticketsPerAssignee: [],
  }),
  setup() {
    return { moment };
  },
  methods: {
    async loadTickets() {
      const { inboxId } = this.$route.params;
      const response = await axios.get(`/api/inboxes/${inboxId}/tickets`);
      const tickets = _.flatten(response.data.map((column) => column.tickets));
      const ticketsPerAssignee = Object.values(
        _.groupBy(tickets, "assignee.id")
      );
      this.ticketsPerAssignee = ticketsPerAssignee;
    },
  },
  created() {
    this.loadTickets();
  },
};
</script>

<style scoped>
.ticket-columns {
  scroll-snap-type: x mandatory;
  scroll-padding: 16px;
}
</style>
