<template>
  <div
    v-if="filter"
    class="rounded-md border select-none"
    :class="open ? 'ring-primary border-primary-400' : 'hover:bg-gray-50 hover:border-gray-300'"
  >
    <div v-if="!open" @click="open = true" class="group py-3 px-4 flex flex-col space-y-1 cursor-pointer rounded">
      <div class="flex space-x-2 items-center justify-between">
        <span v-if="filter.name" class="font-medium">{{ filter.name }}</span>
        <span v-else class="italic">No title for filter</span>
        <!-- <selector-icon class="h-6 w-6 handle text-primary cursor-move" /> -->
      </div>
      <div v-if="filter.name" class="items-center hidden sm:flex">
        <div class="flex space-x-1">
          <template v-for="(condition, index) in filter.conditions" :key="index">
            <chip v-if="condition.field_name === 'title'">{{ conditionNames[condition.field_name] }} = {{ condition.evaluation_value }}</chip>
            <chip v-if="condition.field_name === 'content'">{{ conditionNames[condition.field_name] }} = {{ condition.evaluation_value }}</chip>
            <chip v-if="condition.field_name === 'date_created'">{{ conditionNames[condition.field_name] }} {{ condition.evaluation_func === 'lt' || condition.evaluation_func === 'le' ? 'before' : 'after' }} {{ condition.evaluation_value }}</chip>
            <chip v-if="condition.field_name === 'labels'" :background="labels.find(l => parseInt(l.id) === parseInt(condition.evaluation_value))?.color">{{ labels.find(l => parseInt(l.id) === parseInt(condition.evaluation_value))?.name }}</chip>
            <chip v-if="condition.field_name === 'is_public'">{{ condition.evaluation_value === 'True' ? 'Public' : 'Private' }}</chip>
          </template>
        </div>
        <chevron-right-icon class="h-6 w-6" />
        <chip v-if="filter.action_func === 'add_label'" :background="labels.find(l => parseInt(l.id) === parseInt(filter.action_value))?.color">{{ labels.find(l => parseInt(l.id) === parseInt(filter.action_value))?.name }}</chip>
        <chip v-else-if="filter.action_func === 'assign_to'">
          <img :src="staff.find(s => s.id === parseInt(filter.action_value))?.avatar" class="w-4 h-4 rounded-full mr-1">
          {{ staff.find(s => s.id === parseInt(filter.action_value))?.name }}
        </chip>
      </div>
    </div>
    <div v-else class="py-3 px-4 space-y-2 w-full">
      <div class="flex justify-between w-full">
        <div class="flex space-x-2 items-center w-full">
          <!-- Name -->
          <div class="w-full">
            <label class="block text-xs leading-5 font-medium text-primary">
              Action title:
            </label>
            <div class="mt-1 relative rounded-md">
              <input v-model="filter.name" type="text" id="filterName" class="block w-full focus:outline-none sm:text-sm rounded-md" :class="errors?.name ? 'pr-10 border-red-300 text-red-900 placeholder-red-300 focus:ring-red-500 focus:border-red-500' : 'focus:ring-primary focus:border-primary border-gray-300'" placeholder="Filter name" aria-invalid="true" aria-autocomplete="false" />
              <div v-if="errors?.name" class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                <ExclamationCircleIcon class="h-5 w-5 text-red-500" aria-hidden="true" />
              </div>
            </div>
            <p v-if="errors?.name" class="mt-1 text-sm text-red-600" id="name-error">{{ errors?.name }}</p>
          </div>
        </div>
      </div>
      <div class="space-y-2 w-full">
        <div class="flex w-full items-center space-x-2">
          <div class="h-1 border-b w-1/2"></div>
          <span class="leading-5 font-medium text-primary">Conditions</span>
          <div class="h-1 border-b w-1/2"></div>
        </div>
        <!-- Place for the conditions -->
        <div v-for="(condition, index) in filter.conditions" :key="condition">
          <div class="flex space-x-2 w-full">
            <div class="flex w-22 justify-center items-center rounded px-4 py-2 space-x-2 text-blue-500 focus:outline-none">
              <span>{{ index === 0 ? 'IF' : 'AND' }}</span>
            </div>

            <AutomationCondition :filterId="filter.id" :conditionId="condition.id" />

            <div class="flex items-center">
              <button @click="removeCondition(condition)" class="p-2 focus:outline-none">
                <trash-icon class="h-6 w-6 text-red-600" />
              </button>
            </div>
          </div>
        </div>
        <p v-if="errors?.conditions" class="mt-1 text-sm text-red-600" id="conditions-error">{{ errors?.conditions }}</p>
        <div class="flex space-x-2">
          <div class="relative inline-block w-min-content">
            <button
              @click="filter.conditions.push({ id: nextId(), evaluation_func: '', evaluation_value: '', field_name: '' })"
              class="flex justify-center items-center rounded px-4 py-2 space-x-1 text-blue-500 bg-blue-100 focus:outline-none hover:bg-blue-200"
            >
              <plus-icon class="h6 w-6" />
              <span>Add condition</span>
            </button>
          </div>
        </div>

        <div class="flex w-full items-center space-x-2">
          <div class="h-1 border-b w-1/2"></div>
          <span class="leading-5 font-medium text-primary">Action</span>
          <div class="h-1 border-b w-1/2"></div>
        </div>
        
        <AutomationAction :filterId="filter.id" />
        <p v-if="errors?.action" class="mt-1 text-sm text-red-600" id="action-error">{{ errors?.action }}</p>

        <!-- Divider -->
        <div class="w-full border-b pt-2 mb-2"></div>

        <!-- Buttons -->
        <div class="flex justify-end space-x-2">
          <button
            @click="cancel"
            class="rounded-md border px-4 py-2 text-gray-800 focus:outline-none hover:bg-gray-50"
          >
            Cancel
          </button>
          <button
            v-if="filter.id > 0"
            @click="askRemove"
            class="rounded-md border px-4 py-2 text-red-700 border-red-300 bg-red-100 focus:outline-none hover:bg-red-200"
          >
            Remove
          </button>
          <button
            @click="save"
            class="rounded-md border px-4 py-2 text-green-700 border-green-300 bg-green-100 focus:outline-none hover:bg-green-200"
          >
            {{ filter.id > 0 ? 'Save' : 'Create' }}
          </button>
        </div>
      </div>
    </div>

    <!-- <NotificationAutomation v-if="showNotification" /> -->
    <RemoveDialog :open="showWarning" @cancel="showWarning = false" @submit="remove()" />
  </div>
</template>

<script>
import store from '@/store'
import axios from 'axios'
import { mapState, mapMutations } from 'vuex'

import Chip from '@/components/chip/Chip'
import AutomationAction from '@/components/automation/AutomationAction'
import AutomationCondition from '@/components/automation/AutomationCondition'
import NotificationAutomation from '@/components/notifications/NotificationAutomation'
import RemoveDialog from '@/components/automation/RemoveDialog'

import {
  TrashIcon,
  SelectorIcon
} from '@heroicons/vue/outline'
import {
  PlusIcon,
  ChevronRightIcon,
  ExclamationCircleIcon
} from '@heroicons/vue/solid'

export default {
  components: {
    AutomationAction,
    AutomationCondition,
    PlusIcon,
    ChevronRightIcon,
    TrashIcon,
    SelectorIcon,
    Chip,
    NotificationAutomation,
    RemoveDialog,
    ExclamationCircleIcon
  },
  data: () => ({
    open: false,
    showWarning: false,
    title: '',
    labels: [],
    staff: [],
    errors: {},
    conditionNames: {
      'title': 'Title',
      'content': 'Content',
      'date_created': 'Created'
    },
    showNotification: false,
    removeConditions: []
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
    
    if (this.filter?.open) {
      this.open = true
      this.filter.open = false
    }
  },
  props: {
    filterId: {
      type: Number,
      required: false,
      default: 1
    }
  },
  methods: {
    ...mapMutations('automation', ['removeFilterCondition']),
    cancel () {
      this.open = false
      this.$emit('update')
    },
    nextId () {
      const new_conditions = this.filter.conditions.filter(condition => condition.id < 0).sort((a, b) => a.id - b.id)
      if (new_conditions.length > 0) return new_conditions[0].id - 1
      return -1
    },
    removeCondition (condition) {
      if (!condition.id) return
      this.removeConditions.push(condition.id)
      this.removeFilterCondition({
        filterId: this.filter.id,
        conditionId: condition.id
      })
    },
    askRemove () {
      this.showWarning = true
    },
    remove () {
      const { inboxId } = this.$route.params
      axios.delete(`/api/inboxes/${inboxId}/automation/${this.filter.id}`).then(response => {
        this.open = false
        this.$emit('update')
      })
    },
    async save () {
      const { inboxId } = this.$route.params

      /* Make sure elements for a filter are present. */
      if (!this.filter.name) this.errors.name = 'You need to give this filter a name.'
      else delete this.errors.name
      if (this.filter.conditions.length === 0) this.errors.conditions = 'You need to add at least one condition.'
      else delete this.errors.conditions
      if (!this.filter.action_value || this.filter.action_value === '') this.errors.action = 'You need to add an action.'
      else delete this.errors.action

      /* Check each condition for validity. */
      for (const condition of this.filter.conditions) {
        if (!condition.evaluation_value)
          this.errors.conditions = 'You need to add a value for each condition.'
        if (!condition.evaluation_func)
          this.errors.conditions = 'You need to add an operator for each condition.'
        if (!condition.field_name)
          this.errors.conditions = 'You need to choose a field for each condition.'
      }
      if (Object.keys(this.errors).length > 0) return

      
      if (this.filter.id < 0) {
        await axios.post(`/api/inboxes/${inboxId}/automation/create`, {
          ...this.filter
        }).then(response => {
          const createConditions = this.filter.conditions.map((condition) => {
            return axios.post(`/api/inboxes/${inboxId}/automation/${response.data.id}/condition/create`, {
              ...condition
            })
          })
          Promise.all([createConditions]).then(() => {
            this.showNotification = true
            this.open = false
            this.$emit('update')
            setTimeout(() => {
              this.showNotification = false
            }, 3000)
          })
        })
      } else {
        const updateAutomation = axios.put(`/api/inboxes/${inboxId}/automation/${this.filter.id}`, {
          ...this.filter
        })
        const updateConditions = this.filter.conditions.map((condition) => {
          if (condition.id > 0) return axios.put(`/api/inboxes/${inboxId}/automation/${this.filter.id}/condition/${condition.id}`, {
            ...condition
          })
          else return axios.post(`/api/inboxes/${inboxId}/automation/${this.filter.id}/condition/create`, {
            ...condition
          })
        })
        const removeConditions = this.removeConditions.map((condition) => {
          if (condition < 0) return
          return axios.delete(`/api/inboxes/${inboxId}/automation/${this.filter.id}/condition/${condition}`)
        })
        Promise.all([updateAutomation, updateConditions, removeConditions]).then(() => {
          this.showNotification = true
          this.open = false
          this.$emit('update')
          setTimeout(() => {
            this.showNotification = false
          }, 3000)
        })
      }
      
    }
  },
  computed: {
    ...mapState('automation', {
      filter (state) {
        const filter = state.filters?.find(filter => parseInt(filter.id) === parseInt(this.filterId))

        return filter
      }
    })
  }
}
</script>
