<template>
  <div>
    <div class="flex mb-2">
      <search-bar v-on:input="get_tickets" class="flex-grow"></search-bar>
    </div>
    <div class="flex space-x-6 flex-grow">
      <!-- Banner -->

      <!-- Sorteren -->

      <!-- Columns -->
      <ticket-column
          v-for="(column, i) in tickets"
          :key="column.label"
          :title="column.label"
          :color="colors[i]"
          :ticket-list="column.tickets"
      />
    </div>
  </div>
</template>

<script>
import SearchBar from "../elements/SearchBar";

export default {
  components: {SearchBar},
  props: ['title'],
  data: () => ({
    colors: ['#e76f51', '#e9c46a', '#2a9d8f', '#264653'],
    tickets: [],
    debounce_search: null
  }),
  methods: {
    get_tickets(search) {
      window.axios.get(`/api${window.location.pathname}`, {
        params: {
          columns: true,
          q: search
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
