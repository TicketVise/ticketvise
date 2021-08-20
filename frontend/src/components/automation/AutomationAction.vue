<template>
  <div class="grid grid-cols-2 gap-2 w-full">
    <select-input :data="types" :init="types[0]" />
    <select-input :data="users" :init="users[0]" />
  </div>
</template>

<script>
import axios from 'axios'
import SelectInput from '@/components/inputs/SelectInput'

const types = [
  { name: 'Assign to' },
  { name: 'Add label' },
  { name: 'Change status' },
  { name: 'Make urgent' }
]

export default {
  components: { SelectInput },
  setup () {
    return { types }
  },
  data: () => ({
    inbox_id: window.location.pathname.split('/')[2],
    users: [],
    selected: []
  }),
  mounted () {
    axios.get(`/api/inboxes/${this.inbox_id}/staff`).then(response => {
      this.users = response.data
      this.users.forEach(c => {
        c.name = c.first_name + ' ' + c.last_name
        c.avatar = c.avatar_url
      })
    })
  }
}
</script>
