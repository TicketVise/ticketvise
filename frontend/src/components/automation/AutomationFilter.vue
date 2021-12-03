<template>
  <div
    class="rounded-md border select-none"
    :class="open ? 'ring-primary border-primary-400' : 'hover:bg-gray-100'"
  >
    <div v-if="!open" @click="open = true" class="group py-3 px-4 flex flex-col space-y-1 cursor-pointer rounded">
      <div class="flex space-x-2 items-center justify-between">
        <span class="font-medium">{{ item.name }}</span>
        <selector-icon class="h-6 w-6 handle text-primary cursor-move" />
      </div>
      <div class="flex items-center">
        <chip background="#FF0000">Grades</chip>
        <i class="fa fa-arrow-right text-gray-800"></i>
        <chevron-right-icon class="h-6 w-6" />
        <chip>Ana Coordinator</chip>
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
            <input
              v-model="item.name"
              type="text"
              id="text"
              placeholder="Filter name"
              class="h-8 text-sm w-full rounded-md border border-gray-300 bg-white pl-3 pr-10 py-2 text-left focus:outline-none"
            />
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
        <div v-for="(filter, index) in item.conditions" :key="index" class="flex space-x-2">
          <div
            class="flex w-22 justify-center items-center rounded px-4 py-2 space-x-2 text-blue-500 focus:outline-none"
          >
            <span>{{ index === 0 ? 'IF' : 'AND' }}</span>
          </div>

          <component :is="filter" />

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
              @click="ifs.push('automationFilterLabel')"
              class="flex justify-center items-center rounded px-4 py-2 space-x-1 text-blue-500 bg-blue-100 focus:outline-none hover:bg-blue-200"
            >
              <plus-icon class="h6 w-6" />
              <span>Add condition</span>
            </button>
          </div>
        </div>

        <div class="flex w-full items-center space-x-2">
          <div class="h-1 border-b w-1/2"></div>
          <span class="leading-5 font-medium text-primary">Actions</span>
          <div class="h-1 border-b w-1/2"></div>
        </div>
        <!-- Place for the thens actions -->
        <div v-for="(filter, index) in thens" :key="index" class="flex space-x-2">
          <component :is="filter" />

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
              @click="thens.push('automationAction')"
              class="flex justify-center items-center rounded px-4 py-2 space-x-1 text-blue-500 bg-blue-100 focus:outline-none hover:bg-blue-200"
            >
              <plus-icon class="h6 w-6" />
              <span>Add action</span>
            </button>
          </div>
        </div>

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
import AutomationFilterLabel from '@/components/automation/AutomationFilterLabel'
import AutomationFilterText from '@/components/automation/AutomationFilterText'
import AutomationAction from '@/components/automation/AutomationAction'
import Chip from '@/components/chip/Chip'

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
    PlusIcon,
    ChevronRightIcon,
    TrashIcon,
    SelectorIcon,
    AutomationFilterLabel,
    AutomationFilterText,
    AutomationAction,
    Chip
  },
  data: () => ({
    open: false,
    title: 'Lecture tickets to teacher',
    addIf: false,
    addThen: false,
    ifs: [],
    thens: []
  }),
  props: {
    item: {
      required: true
    }
  },
  methods: {
    cancel () {
      this.open = false
    },
    remove (index) {
      this.ifs.splice(index, 1)
    }
  }
}
</script>
