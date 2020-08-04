<template>
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
</template>

<script>
export default {
  props: ['title'],
  data: () => ({
    colors: ['#e76f51', '#e9c46a', '#2a9d8f', '#264653'],
    tickets: []
  }),
  created() {
    const self = this
    
    window.axios.get(`/api${window.location.pathname}`, {
      params: {
        columns: true
      }
    }).then(response => {
      self.tickets = response.data
    })
  }
}
</script>
