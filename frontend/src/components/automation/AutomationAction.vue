<template>
  <div class="grid grid-cols-2 gap-2 w-full">
    <SelectInput v-model="selectedAction" :data="actions" emptyLabel="Choose field" />
    <SelectInput v-if="selectedAction?.input === 'labels'" v-model="selectedLabel" :data="labels" :emptyLabel="!selectedAction ? 'First choose action' : 'Choose value'" :disabled="!selectedAction" />
    <SelectInput v-if="selectedAction?.input === 'staff'" v-model="selectedStaff" :data="staff" :emptyLabel="!selectedStaff ? 'First choose action' : 'Choose value'" :disabled="!selectedAction" />
  </div>
</template>

<script>
import axios from 'axios'

import SelectInput from '@/components/inputs/SelectInput'

export default {
  name: 'AutomationAction',
  components: {
    SelectInput
  },
  props: {
    item: {
      required: true
    }
  },
  data: () => ({
    labels: [],
    staff: [],
    selectedAction: null,
    selectedLabel: null,
    selectedStaff: null,
    actions: [
      {
        name: 'Add label',
        value: 'add_label',
        input: 'labels'
      },
      {
        name: 'Assign to',
        value: 'assign_to',
        input: 'staff'
      }
    ]
  }),
  mounted () {
    axios.get(`/api/inboxes/${this.$route.params.inboxId}/labels/all`).then(response => {
      this.labels = response.data
    })
    axios.get(`/api/inboxes/${this.$route.params.inboxId}/staff`).then(response => {
      this.staff = response.data
    })
    
    this.selectedAction = this.actions.find(type => type.value === this.item.action_func)

    if (this.selectedAction.value === 'add_label')
      this.selectedLabel = this.labels.find(label => label.id === this.item.action_value)
    else if (this.selectedAction.value === 'assign_to')
      this.selectedStaff = this.staff.find(staff => staff.id === this.item.action_value)
  },
  watch: {
    selectedAction: {
      handler (value) {
        this.selectedAction = value
      },
      immediate: true
    }
  }
}
</script>
