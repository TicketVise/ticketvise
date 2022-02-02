<template>
  <div class="grid grid-cols-2 gap-2 w-full">
    <SelectInput v-model="selectedAction" :data="actions" emptyLabel="Choose field" />
    <SelectInput v-if="selectedAction?.input === 'labels'" v-model="selectedValue" :data="labels" :emptyLabel="!selectedAction ? 'First choose action' : 'Choose value'" :disabled="!selectedAction" multiple />
    <SelectInput v-if="selectedAction?.input === 'staff'" v-model="selectedValue" :data="staff" :emptyLabel="!selectedAction ? 'First choose action' : 'Choose value'" :disabled="!selectedAction" multiple />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import axios from 'axios'

import SelectInput from '@/components/inputs/SelectInput'

export default {
  name: 'AutomationAction',
  components: {
    SelectInput
  },
  props: {
    filterId: {
      required: true,
      type: Number
    }
  },
  data: () => ({
    labels: [],
    staff: [],
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
  async mounted () {
    await axios.get(`/api/inboxes/${this.$route.params.inboxId}/labels/all`).then(response => {
      this.labels = response.data
    })
    await axios.get(`/api/inboxes/${this.$route.params.inboxId}/staff`).then(response => {
      this.staff = response.data.map(staff => {
        return {
          id: staff.id,
          name: staff.first_name + ' ' + staff.last_name,
          avatar: staff.avatar_url
        }
      })
    })
  },
  watch: {
    selectedAction: {
      handler (newType, oldType) {
        if (oldType === newType) return

        if (newType.input === 'labels') this.selectedValue = this.labels[0]
        else this.selectedValue = this.staff[0]
      },
      deep: true
    }
  },
  computed: {
    ...mapState('automation', {
      filter (state) {
        return state.filters?.find(filter => parseInt(filter.id) === parseInt(this.filterId))
      }
    }),
    selectedAction: {
      get () {
        return this.actions.find(action => action.value === this.filter.action_func)
      },
      set (value) {
        this.$store.commit('automation/setActionFunc', {
          filterId: this.filterId,
          actionFunc: value.value
        })
      }
    },
    selectedValue: {
      get () {
        if (this.filter.action_func === 'add_label')
          return this.labels.find(label => parseInt(label.id) === parseInt(this.filter.action_value))
        if (this.filter.action_func === 'assign_to')
          return this.staff.find(staff => parseInt(staff.id) === parseInt(this.filter.action_value))
      },
      set (value) {
        this.$store.commit('automation/setActionValue', {
          filterId: this.filterId,
          actionValue: value.id
        })
      }
    }
  }
}
</script>
