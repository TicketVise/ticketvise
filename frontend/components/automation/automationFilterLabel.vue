<template>
  <div class="grid grid-cols-3 gap-2 w-full">
    <tv-select :items="['Label', 'Title', 'Time']" />
    <tv-select :items="['Contains', 'Contains not']" />
    <tv-select multiple :items="labels" />
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data: () => ({
    inbox_id: window.location.pathname.split('/')[2],
    labels: [],
    selected: []
  }),
  mounted() {
    axios.get(`/api/inboxes/${this.inbox_id}`).then(response => {
      this.labels = response.data.labels
    })
  }
}
</script>