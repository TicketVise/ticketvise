<template>
  <div class="rounded-md border select-none" :class="{ 'shadow-outline-orange border-orange-400': open }">
    <div v-if="!open" @click="open = true" class="group py-3 px-4 flex flex-col space-y-1 cursor-pointer rounded">
      <div class="flex space-x-2 items-center justify-between">
        <span class="font-medium">{{ title }}</span>
        <font-awesome-icon @click.stop class="handle text-orange-500 cursor-move" :icon="['fas', 'grip-vertical']"/>
      </div>
      <div class="flex space-x-2 items-center">
        <chip background="#FF0000" :rounded="false" outlined>Grades</chip>
        <i class="fa fa-arrow-right text-gray-800"></i>
        <chip :rounded="false" outlined>Ana Coordinator</chip>
      </div>
    </div>
    <div v-else class="py-3 px-4 space-y-2">
      <div class="flex justify-between w-full">
        <div class="flex space-x-2 items-center w-3/4">
          <!-- Name -->
          <div class="w-full">
            <label class="block text-xs leading-5 font-medium text-orange-500">
              Filter title:
            </label>
            <input
              v-model="title"
              type="text"
              id="text"
              placeholder="Filter name"
              class="h-8 text-sm w-full rounded-md border border-gray-300 bg-white pl-3 pr-10 py-2 text-left focus:outline-none"
            >
          </div>
        </div>
      </div>
      <div class="space-y-2 w-full">
        <div class="flex w-full items-center space-x-2">
          <div class="h-1 border-b w-1/2"></div>
          <span class="leading-5 font-medium text-orange-500">Conditions</span>
          <div class="h-1 border-b w-1/2"></div>
        </div>
        <!-- Place for the IF filters -->
        <div v-for="(filter, index) in ifs" :key="index" class="flex space-x-2">
          <div class="flex w-22 justify-center items-center rounded px-4 py-2 space-x-2 text-blue-500 focus:outline-none">
            <span>{{ index === 0 ? 'IF' : 'AND' }}</span>
          </div>

          <component :is="filter" />

          <button @click="remove(index)" class="flex items-center px-2 focus:outline-none">
            <font-awesome-icon class="text-red-600" icon="trash"/>
          </button>
        </div>
        <div class="flex space-x-2">
          <div class="relative inline-block w-min-content">
            <button  @click="ifs.push('automationFilterLabel')" class="flex justify-center items-center rounded px-4 py-2 space-x-2 text-blue-500 bg-blue-100 focus:outline-none hover:bg-blue-200">
              <i class="fa fa-plus"></i>
              <span>Add</span>
            </button>
            <!-- <div v-if="addIf" v-on-clickaway="awayAddIf" class="origin-top-left absolute left-0 mt-2 w-56 rounded-md shadow-lg z-10">
              <div class="rounded-md bg-white shadow-xs">
                <div class="py-1" role="menu" aria-orientation="vertical" aria-labelledby="options-menu">
                  <button @click="ifs.push('automationFilterLabel')" class="flex w-full px-2 py-2 text-sm leading-5 space-x-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900 focus:outline-none focus:bg-gray-100 focus:text-gray-900" role="menuitem">
                    <div class="flex justify-center items-center w-8">
                      <font-awesome-icon class="text-orange-500" icon="tags"/>
                    </div>
                    <span>Label</span>
                  </button>
                  <button @click="ifs.push('automationFilterText')" class="flex px-2 py-2 text-sm leading-5 space-x-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900 focus:outline-none focus:bg-gray-100 focus:text-gray-900" role="menuitem">
                    <div class="flex justify-center items-center w-8">
                      <font-awesome-icon class="text-orange-500" icon="i-cursor"/>
                    </div>
                    <span>Title</span>
                  </button>
                  <a href="#" class="flex px-2 py-2 text-sm leading-5 space-x-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900 focus:outline-none focus:bg-gray-100 focus:text-gray-900" role="menuitem">
                    <div class="flex justify-center items-center w-8">
                      <font-awesome-icon class="text-orange-500" icon="clock"/>
                    </div>
                    <span>Time</span>
                  </a>
                </div>
              </div>
            </div> -->
          </div>
        </div>

        <div class="flex w-full items-center space-x-2">
          <div class="h-1 border-b w-1/2"></div>
          <span class="leading-5 font-medium text-orange-500">Actions</span>
          <div class="h-1 border-b w-1/2"></div>
        </div>
        <div v-if="thens.length" class="grid grid-cols-2 gap-2">
          <!-- Place for the thens actions -->
        </div>
        <div class="flex space-x-2">
          <div class="relative inline-block w-min-content">
            <button @click="addThen = !addThen" class="flex justify-center items-center rounded px-4 py-2 space-x-2 text-blue-500 bg-blue-100 focus:outline-none hover:bg-blue-200">
              <i class="fa fa-plus"></i>
              <span>Add</span>
            </button>
            <div v-if="addThen" v-on-clickaway="awayAddThen" class="origin-top-left absolute left-0 mt-2 w-56 rounded-md shadow-lg z-10">
              <div class="rounded-md bg-white shadow-xs">
                <div class="py-1" role="menu" aria-orientation="vertical" aria-labelledby="options-menu">
                  <a href="#" class="flex px-2 py-2 text-sm leading-5 space-x-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900 focus:outline-none focus:bg-gray-100 focus:text-gray-900" role="menuitem">
                    <div class="flex justify-center items-center w-8">
                      <font-awesome-icon class="text-orange-500" icon="user"/>
                    </div>
                    <span>Assign</span>
                  </a>
                  <a href="#" class="flex px-2 py-2 text-sm leading-5 space-x-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900 focus:outline-none focus:bg-gray-100 focus:text-gray-900" role="menuitem">
                    <div class="flex justify-center items-center w-8">
                      <font-awesome-icon class="text-orange-500" icon="bell"/>
                    </div>
                    <span>Notify</span>
                  </a>
                  <a href="#" class="flex px-2 py-2 text-sm leading-5 space-x-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900 focus:outline-none focus:bg-gray-100 focus:text-gray-900" role="menuitem">
                    <div class="flex justify-center items-center w-8">
                      <font-awesome-icon class="text-orange-500" icon="tags"/>
                    </div>
                    <span>Label</span>
                  </a>
                  <a href="#" disabled class="flex px-2 py-2 text-sm leading-5 space-x-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900 focus:outline-none focus:bg-gray-100 focus:text-gray-900" role="menuitem">
                    <div class="flex justify-center items-center w-8">
                      <font-awesome-icon class="text-orange-500" icon="columns"/>
                    </div>
                    <span>Status</span>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Divider -->
        <div class="w-full border-b pt-2 mb-2"></div>

        <!-- Buttons -->
        <div class="flex justify-end space-x-2">
          <button @click="cancel" class="rounded border px-4 py-2 text-gray-800 focus:outline-none hover:bg-gray-100">
            Cancel
          </button>
          <button @click="cancel" class="rounded border px-4 py-2 text-red-600 border-red-400 bg-red-300 focus:outline-none hover:bg-red-200">
            Remove
          </button>
          <button @click="cancel" class="rounded border px-4 py-2 text-green-600 border-green-400 bg-green-300 focus:outline-none hover:bg-green-200">
            Save
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mixin as clickaway } from 'vue-clickaway'
import axios from "axios";

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faGripVertical, faClock, faICursor, faTags, faUser, faBell, faColumns, faTrash } from '@fortawesome/free-solid-svg-icons'

library.add([faGripVertical, faClock, faICursor, faTags, faUser, faBell, faColumns, faTrash])

export default {
  components: {FontAwesomeIcon},
  mixins: [ clickaway ],
  data: () => ({
    open: true,
    colorPicker: false,
    title: 'Important ticket to teacher',
    inbox_id: window.location.pathname.split('/')[2],
    addIf: false,
    addThen: false,
    ifs: [],
    thens: []
  }),
  methods: {
    cancel() {
      this.open = false
    },
    awayAddIf() {
      this.addIf = false
    },
    awayAddThen() {
      this.addThen = false
    },
    remove(index) {
      console.log(index)
      this.ifs.splice(index, 1)
    }
  }
}
</script>

<style lang="scss">
  .moving-card {
    @apply opacity-50 bg-gray-100 border border-orange-500;
  }
</style>