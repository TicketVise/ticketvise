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
    <div class="max-w-7xl mx-auto sm:py-6 sm:px-6 lg:px-8">
      <div v-if="userInboxes" class="px-4 py-6 sm:px-0 grid md:grid-cols-3 gap-4">
        <div v-for="userInbox in userInboxes" class="bg-white relative">
          <a :href="userInbox.inbox.id" class="" aria-label="more options">
              <div class="h-64 w-full rounded hover:shadow-lg transition-shadow ease-in-out duration-100"
                   :style="{'background-color': userInbox.inbox.color}">
                <img class="h-64 w-full rounded object-cover opacity-75" :src="userInbox.inbox.image"
                     :alt="userInbox.inbox.name">
              </div>
          </a>

          <div
              class="absolute bottom-0 bg-gray-800 bg-opacity-50 w-full text-white flex py-2 px-4 space-x-2 rounded-br rounded-bl shadow-lg"
              style="overflow: hidden; text-overflow: ellipsis;">
              <button type="button" @click="onBookmarkClick()" class="pl-0">
                <i v-if="userInbox.is_bookmarked" class="fa fa-bookmark"></i>
                <i v-else class="fa fa-bookmark-o"></i>
              </button>

            <a :href="userInbox.inbox.id">
              {{ userInbox.inbox.name }}
            </a>
          </div>
        </div>
      </div>
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
    userInboxes: [],
  }),
  async mounted() {
    const response = await axios.get("/api/me" + window.location.pathname);
    this.userInboxes = response.data
  },
  methods: {
    onBookmarkClick: function () {

    }
  }
}
</script>

<style scoped>

</style>