<template>
  <div>
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto p-4 pt-2">
        <div class="sm:flex sm:items-center sm:justify-between">
          <div class="flex-1 min-w-0">
            <div class="flex justify-between items-center">
              <a href="/inboxes" class="text-xs text-gray-700 hover:underline cursor-pointer">
                <i class="fa fa-arrow-left mr-2"></i>
                Dashboard
              </a>
            </div>

            <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:leading-9 truncate">
              Admin overview
            </h2>
          </div>
          <div class="mt-2 sm:mt-0 sm:ml-4 space-x-4 flex">
            <span class="shadow-sm rounded-md">
              <a href="/admin/django"
                class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm leading-5 font-medium rounded-md text-gray-700 bg-white hover:text-gray-500 focus:outline-none focus:shadow-outline-blue focus:border-blue-300 active:text-gray-800 active:bg-gray-50 transition duration-150 ease-in-out">
                <i class="fa fa-cog mr-2"></i>
                Django admin
              </a>
            </span>
          </div>
        </div>
      </div>
    </header>

    <div class="container mx-auto py-4 px-2">
      <div class="w-full border rounded-md divide-y">
        <inbox-stats v-for="inbox in inboxes" :key="inbox.id" :inbox="inbox" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data: () => ({
    inboxes: []
  }),
  async mounted() {
    const response = await axios.get(`/api/inboxes`)
    this.inboxes = response.data
  }
}
</script>

<style>

</style>
