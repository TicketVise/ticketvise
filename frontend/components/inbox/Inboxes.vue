<template>
  <div>
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold leading-tight text-gray-900">
          Your inboxes
        </h1>
      </div>
    </header>
    <main>
      <div class="max-w-7xl mx-auto sm:py-6 px-6 lg:px-8">
        <div v-if="bookmarked.length" class="mb-8">
          <h2 class="text-xl mb-2 font-bold leading-tight text-gray-900">
            Bookmarked
          </h2>
          <inboxes-grid :inboxes="bookmarked" />
        </div>
        <h2 class="text-xl mb-2 font-bold leading-tight text-gray-900">
          All inboxes
        </h2>
        <inboxes-grid v-if="userInboxes" :inboxes="userInboxes" />
        <div v-else class="flex flex-col items-center w-full">
          <img src="/static/img/svg/undraw_empty_street_sfxm.svg" alt="Nothing here" class="w-1/2 md:w-1/3 mx-auto py-8">
          <span class="text-gray-600 text-lg md:text-xl">You have no inboxes</span>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Inboxes",
  data: () => ({
    userInboxes: []
  }),
  computed: {
    bookmarked() {
      return this.userInboxes.filter((inbox) => {
        return inbox.is_bookmarked
      })
    }
  },
  async mounted() {
    const response = await axios.get('/api/me/inboxes');
    this.userInboxes = response.data
  }
}
</script>

<style scoped>

</style>