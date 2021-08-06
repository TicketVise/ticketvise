<template>
  <user-dropdown :values="labels" :selected="selected" class="max-h-8 w-full" />
</template>

<script>
import axios from 'axios'

export default {
  data: () => ({
    inbox_id: window.location.pathname.split('/')[2],
    labels: [],
    selected: []
  }),
  mounted () {
    axios.get(`/api/inboxes/${this.inbox_id}`).then(response => {
      this.labels = response.data.labels
    })
  }
}
</script>
