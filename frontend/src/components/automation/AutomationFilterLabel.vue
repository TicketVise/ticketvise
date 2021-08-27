<template>
  <div class="grid grid-cols-3 gap-2 w-full">
    <select-input :data="types" :init="types[0]" />
    <select-input :data="options" :init="options[0]" />
    <select-input :data="labels" :init="labels[0]" />
  </div>
</template>

<script>
import axios from 'axios'
import SelectInput from '@/components/inputs/SelectInput'

const types = [
  { name: 'Labels' },
  { name: 'Title' },
  { name: 'Time' }
]

const options = [
  { name: 'Contains' },
  { name: 'Contains not' }
]

export default {
  components: { SelectInput },
  setup () {
    return { types, options }
  },
  data: () => ({
    inbox_id: window.location.pathname.split('/')[2],
    labels: [],
    selected: []
  }),
  mounted () {
    axios.get(`/api/inboxes/${this.inbox_id}/labels/all`).then(response => {
      this.labels = response.data
    })
  }
}
</script>
