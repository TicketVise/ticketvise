<template>
  <div>
    <div class="flex-wrap md:flex mb-2">
      <search-bar v-on:input="get_tickets" class="flex-grow px-2"></search-bar>
      <submit-button v-if="!showPersonal" class="bg-orange-400 px-2 m-2 md:m-0" text="My Tickets" @click="showPersonal = !showPersonal; get_tickets()"></submit-button>
      <submit-button v-if="showPersonal" class="bg-orange-500 px-2 m-2 md:m-0" text="My Tickets" @click="showPersonal = !showPersonal; get_tickets()"></submit-button>
    </div>
    <div class="sm:flex-wrap md:flex md:space-x-6 flex-grow min-h-screen">
      <!-- Banner -->

      <!-- Sorteren -->

      <!-- Columns -->
      <ticket-column
          v-for="(column, i) in tickets"
          :key="column.label"
          :title="column.label"
          :color="colors[i]"
          :ticket-list="column.tickets"
          class="m-2 md:m-0"
      />
    </div>
  </div>
</template>

<script>
import SearchBar from "../elements/SearchBar";
import SubmitButton from "../elements/buttons/SubmitButton";
import TicketColumn from "./TicketColumn";

export default {
  components: {TicketColumn, SubmitButton, SearchBar},
  props: ['title'],
  data: () => ({
    colors: ['#e76f51', '#e9c46a', '#2a9d8f', '#264653'],
    tickets: [],
    debounce_search: null,
    showPersonal: false
  }),
  methods: {
    get_tickets(search) {
      console.log("get")
      window.axios.get(`/api${window.location.pathname}`, {
        params: {
          columns: true,
          q: search,
          show_personal: this.showPersonal
        }
      }).then(response => {
        this.tickets = response.data
      })
    },
    search_tickets(search) {
      this.debounce_search(search)
    }
  },
  created() {
    this.get_tickets()
  }
}
</script>
