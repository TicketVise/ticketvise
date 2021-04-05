<template>
  <div class="lg:flex lg:items-center lg:justify-between border-b p-4">
    <div class="flex-1 min-w-0">
      <h2 v-if="inbox" class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
        {{ inbox.inbox.name }}
      </h2>
      <div v-else class="h-7 w-full max-w-screen-sm bg-gray-200 rounded" />
      <div
        class="mt-1 flex flex-col sm:flex-row sm:flex-wrap sm:mt-0 sm:space-x-6"
      >
        <div class="mt-2 flex items-center text-sm text-gray-500">
          <!-- Heroicon name: code -->
          <svg class="w-6 h-6 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path></svg>
          <span v-if="inbox">{{ inbox.inbox.code }}</span>
          <div v-else class="h-5 w-24 bg-gray-200 rounded" />
        </div>
        <div class="mt-2 flex items-center text-sm text-gray-500">
          <!-- Heroicon name: user -->
          <svg class="w-6 h-6 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
          <span v-if="inbox">{{ inbox.inbox.coordinator.first_name }} {{ inbox.inbox.coordinator.last_name }}</span>
          <div v-else class="h-5 w-24 bg-gray-200 rounded" />
        </div>
      </div>
    </div>
    <div class="mt-5 flex lg:mt-0 lg:ml-4">
      <router-link :to="'/inboxes/' + $route.params.inboxId + '/tickets/new'"
        type="button"
        class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-orange-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
      >
        <!-- Heroicon name: add -->
        <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
        New Ticket
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InboxHeader',
  props: {
    inbox: {
      required: false,
      type: Object
    }
  }
}
</script>

<style>

</style>
