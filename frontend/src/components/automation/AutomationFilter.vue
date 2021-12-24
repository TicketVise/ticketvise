<template>
  <div
    class="rounded-md border select-none"
    :class="open ? 'ring-primary border-primary-400' : 'hover:bg-gray-100'"
  >
    <div v-if="!open" @click="open = true" class="group py-3 px-4 flex flex-col space-y-1 cursor-pointer rounded">
      <div class="flex space-x-2 items-center justify-between">
        <span class="font-medium">{{ item.name }}</span>
        <!-- <selector-icon class="h-6 w-6 handle text-primary cursor-move" /> -->
      </div>
      <div class="flex items-center">
        <div class="flex space-x-1">
          <template v-for="(condition, index) in item.conditions" :key="index">
            <chip v-if="condition.field_name === 'title'">{{ conditionNames[condition.field_name] }} = {{ condition.evaluation_value }}</chip>
            <chip v-if="condition.field_name === 'date_created'">{{ conditionNames[condition.field_name] }} {{ condition.evaluation_func === 'lt' || condition.evaluation_func === 'le' ? 'before' : 'after' }} {{ condition.evaluation_value }}</chip>
          </template>
        </div>
        <chevron-right-icon class="h-6 w-6" />
        <chip v-if="item.action_func === 'add_label'" :background="labels.find(l => l.id === parseInt(item.action_value))?.color">{{ labels.find(l => l.id === parseInt(item.action_value))?.name }}</chip>
        <chip v-else-if="item.action_func === 'assign_to'">
          Assign to
        </chip>
      </div>
    </div>
    <div v-else class="py-3 px-4 space-y-2">
      <div class="flex justify-between w-full">
        <div class="flex space-x-2 items-center w-full">
          <!-- Name -->
          <div class="w-full">
            <label class="block text-xs leading-5 font-medium text-primary">
              Action title:
            </label>
            <input v-model="item.name" type="text" id="text" placeholder="Filter name" class="h-8 text-sm w-full rounded-md border border-gray-300 bg-white pl-3 pr-10 py-2 text-left focus:outline-none" />
          </div>
        </div>
      </div>
      <div class="space-y-2 w-full">
        <div class="flex w-full items-center space-x-2">
          <div class="h-1 border-b w-1/2"></div>
          <span class="leading-5 font-medium text-primary">Conditions</span>
          <div class="h-1 border-b w-1/2"></div>
        </div>
        <!-- Place for the IF filters -->
        <div v-for="(condition, index) in item.conditions" :key="index" class="flex space-x-2">
          <div class="flex w-22 justify-center items-center rounded px-4 py-2 space-x-2 text-blue-500 focus:outline-none">
            <span>{{ index === 0 ? 'IF' : 'AND' }}</span>
          </div>

          <AutomationCondition :condition="condition" />

          <button
            @click="remove(index)"
            class="flex items-center px-2 focus:outline-none"
          >
            <trash-icon class="h-6 w-6 text-red-600" />
          </button>
        </div>
        <div class="flex space-x-2">
          <div class="relative inline-block w-min-content">
            <button
              @click="item.conditions.push({ evaluation_func: '', evaluation_value: '', field_name: '' })"
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
        
        <AutomationAction :item="item" />

        <!-- Divider -->
        <div class="w-full border-b pt-2 mb-2"></div>

        <!-- Buttons -->
        <div class="flex justify-end space-x-2">
          <button
            @click="cancel"
            class="rounded border px-4 py-2 text-gray-800 focus:outline-none hover:bg-gray-100"
          >
            Cancel
          </button>
          <button
            @click="cancel"
            class="rounded border px-4 py-2 text-red-600 border-red-400 bg-red-300 focus:outline-none hover:bg-red-200"
          >
            Remove
          </button>
          <button
            @click="cancel"
            class="rounded border px-4 py-2 text-green-600 border-green-400 bg-green-300 focus:outline-none hover:bg-green-200"
          >
            Save
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

import Chip from '@/components/chip/Chip'
import AutomationAction from '@/components/automation/AutomationAction'
import AutomationCondition from '@/components/automation/AutomationCondition'

import {
  TrashIcon,
  SelectorIcon
} from '@heroicons/vue/outline'
import {
  PlusIcon,
  ChevronRightIcon
} from '@heroicons/vue/solid'

export default {
  components: {
    AutomationAction,
    AutomationCondition,
    PlusIcon,
    ChevronRightIcon,
    TrashIcon,
    SelectorIcon,
    Chip
  },
  data: () => ({
    open: false,
    title: '',
    labels: [],
    conditionNames: {
      'title': 'Title',
      'date_created': 'Created'
    },
  }),
  mounted () {
    axios.get(`/api/inboxes/${this.$route.params.inboxId}/labels/all`).then(response => {
      this.labels = response.data
    })
  },
  props: {
    item: {
      required: true
    }
  },
  methods: {
    cancel () {
      this.open = false
    },
    remove (index) {}
  }
}
</script>
