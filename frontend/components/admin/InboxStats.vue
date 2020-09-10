<template>
  <div>
    <div class="pl-6 pr-2 py-4 flex justify-between">
      <div class="flex-grow grid sm:grid-cols-2">
        <div class="flex space-x-4">
          <img class="h-12 w-12 rounded-full object-cover" :src="inbox.image">
          <div class="flex flex-col">
            <span class="text-orange-500 break-words">{{ inbox.name }}</span>
            <div class="flex items-center text-sm leading-5 text-gray-500">
              <i class="fa fa-user mr-1"></i>
              {{ inbox.get_coordinator }}
            </div>
          </div>
        </div>
        <div class="hidden sm:flex flex-col">
          <span class="text-gray-800">Started: {{ moment(inbox.date_created).calendar() }}</span>
          <span class="text-gray-800">
            <i class="fa fa-clipboard-list"></i>
            {{ inbox.scheduling_algorithm }}
          </span>
        </div>
      </div>
      <div class="flex sm:items-center hover:bg-gray-100 rounded-full cursor-pointer select-none" @click="open = !open">
        <i class="fa p-4" :class="{ 'fa-chevron-down': !open, 'fa-chevron-up': open }"></i>
      </div>
    </div>
    <div v-if="open" class="border-t py-2 sm:px-6 grid grid-cols-3 divide-x">
      <div class="flex flex-col items-center">
        <span class="text-orange-500 text-2xl">
          {{ inbox.get_number_of_users }}
        </span>
        <span class="text-gray-700">Users</span>
      </div>
      <div class="flex flex-col items-center">
        <span class="text-orange-500 text-2xl">
          {{ inbox.get_number_of_tickets }}
        </span>
        <span class="text-gray-700">Tickets</span>
      </div>
      <div class="flex flex-col items-center">
        <span class="text-orange-500 text-2xl">
          {{ inbox.get_number_of_labels }}
        </span>
        <span class="text-gray-700">Labels</span>
      </div>

      <div class="col-span-3">
        <div id="tickets-chart" :inboxId="inbox.id"></div>
      </div>
    </div>
  </div>
</template>

<script>
const moment = require('moment')

export default {
  data: () => ({
    open: false,
    moment: moment
  }),
  props: {
    inbox: {
      required: true,
      type: Object
    }
  }
}
</script>

<style>

</style>
