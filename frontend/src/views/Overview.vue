<template>
  <div>
    <div class="block">
      <div class="border-b border-gray-200 px-4">
        <nav class="-mb-px flex space-x-8 max-w-3xl mx-auto" aria-label="Tabs">
          <a v-for="tab in tabs" :key="tab.name" href="#" :class="[tab.current ? 'border-primary text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-200', 'whitespace-nowrap flex py-3 md:py-4 px-1 border-b-2 font-medium text-sm']" :aria-current="tab.current ? 'page' : undefined">
            {{ tab.name }}
            <span v-if="tab.count" :class="[tab.current ? 'bg-primary-100 text-primary-600' : 'bg-gray-100 text-gray-900', 'hidden ml-3 py-0.5 px-2.5 rounded-full text-xs font-medium md:inline-block']">{{ tab.count }}</span>
          </a>
        </nav>
      </div>
    </div>

    <div class="p-4">
      <div class="max-w-3xl mx-auto flex flex-col space-y-4">
        <router-link :to="`/inboxes/1/tickets/1`" class="group border rounded-lg flex flex-col p-3">
          <div class="flex justify-between">
            <div class="flex space-x-2 text-red-600">
              <ExclamationCircleIcon class="w-5 h-5" />
              <span class="font-medium text-sm">HIGH</span>
            </div>
            <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">Created</span>
          </div>

          <h2 class="font-semibold text-lg group-hover:underline mt-1 leading-6">Should we write the individual report in the passive form?</h2>

          <div class="flex justify-between items-center">
            <h3 class="text-xs text-gray-500 dark:text-gray-400">
              <span class="font-medium">Ivan de Wolf</span>・Today at 00:35
            </h3>
          </div>

          <div class="flex mt-2">
            <chip background="#FF0000">Assignment</chip>
          </div>
        </router-link>

        <router-link :to="`/inboxes/1/tickets/1`" class="group border rounded-lg flex flex-col p-3">
          <div class="flex justify-between">
            <div class="flex space-x-2 text-yellow-600">
              <BellIcon class="w-5 h-5" />
              <span class="font-medium text-sm">MEDIUM</span>
            </div>
            <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-yellow-100 text-yellow-800">Reaction</span>
          </div>

          <h2 class="font-semibold text-lg group-hover:underline mt-1 leading-6">Is there a lecture on the day of the demo?</h2>

          <div class="flex justify-between items-center">
            <h3 class="text-xs text-gray-500 dark:text-gray-400">
              <span class="font-medium">Jurre Brandsen</span>・Yesterday 17:36
            </h3>
          </div>

          <div class="flex mt-2">
            <chip background="#0000FF">Lectures</chip>
          </div>
        </router-link>

        <!-- <div class="flex flex-col space-y-4 items-center">
          <img
            :src="HighFive"
            alt="Nothing here"
            class="w-64 h-64"
          />
          <span class="text-gray-800 text-lg md:text-xl font-semibold">
            Concrats you are all up to date, nothing you need to do now!
          </span>
        </div> -->
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import store from '@/store'
import { mapState } from 'vuex'

import Chip from '@/components/chip/Chip.vue'

import {
  BellIcon,
  ExclamationCircleIcon
} from '@heroicons/vue/outline'

// const HighFive = require('@/assets/img/svg/highfive.svg')

const tabs = [
  { name: 'Urgent', href: '#', count: '2', current: true },
  { name: 'Others', href: '#', count: '0', current: false }
]

export default {
  name: 'Overview',
  components: {
    BellIcon,
    Chip,
    ExclamationCircleIcon
  },
  setup() {
    return {
      // HighFive,
      tabs
    }
  },
  computed: {
    ...mapState({
      user: state => state.user,
      tickets () {
        return store.getters.inbox(this.$route.params.inboxId)?.tickets
      }
    })
  }
}
</script>
