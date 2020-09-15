<template>
  <div v-if="user">
    <!-- Header -->
    <div class="border-b shadow flex justify-center">
      <div class="container px-4 my-4 mt-2 xl:flex xl:items-center xl:justify-between">
        <div class="flex-1 min-w-0">
          <a class="text-xs text-gray-700 hover:underline cursor-pointer" href="/inboxes">
            <i class="fa fa-arrow-left mr-2"></i>
            Dashboard
          </a>
          <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:leading-9 sm:truncate">
            Your profile
          </h2>
        </div>
      </div>
    </div>

    <div class="w-screen max-w-screen-lg mx-auto hidden lg:grid grid-cols-3 gap-8">
      <div class="col-span-1 p-8">
        <img :src="user.avatar_url" class="rounded-full w-full h-auto">
      </div>
      <div class="col-span-2 p-8">
        <div class="flex items-center">
          <h2 class="font-bold text-3xl text-orange-500 mr-2">{{ user.first_name }} {{ user.last_name }}</h2>
          <span class="font-light text-gray-400">@{{ user.username }}</span>
        </div>
        <div class="font-light mb-16 text-gray-700">
          <i class="fa fa-envelope mr-2"></i>
          {{ user.email }}
        </div>

        <!-- Notifications settings -->
        <notification-settings />
      </div>
    </div>

    <div class="container mx-auto flex flex-col space-y-4 lg:hidden">
      <div class="flex space-x-8 p-8 pb-0">
        <img :src="user.avatar_url" class="rounded-full w-16 h-16">
        <div class="flex flex-col justify-center">
          <div class="flex flex-row flex-wrap items-center">
            <h2 class="font-bold text-3xl text-orange-500 mr-4">{{ user.first_name }} {{ user.last_name }}</h2>
            <span class="font-light text-gray-400">@{{ user.username }}</span>
          </div>
          <div class="font-light text-gray-700">
            <i class="fa fa-envelope mr-2"></i>
            {{ user.email }}
          </div>
        </div>
      </div>

      <div class="p-4">
        <!-- Notifications settings -->
        <notification-settings />
      </div>
    </div>
  </div>
</template>

<script>
  import axios from "axios"

  export default {
  data: () => ({
    user: null
  }),
  mounted() {
    axios.get('/api/me').then(response => {
      this.user = response.data
    })
  }
}
</script>
