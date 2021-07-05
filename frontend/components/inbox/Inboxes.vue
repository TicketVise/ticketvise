<template>
  <div class="overflow-y-auto">
    <div class="py-5">
      <div class="flex justify-between items-center">
        <h1 class="text-3xl font-bold text-white">
          Your Inboxes
        </h1>
        <nav class="flex space-x-4">
          <button
            v-if="showAll"
            @click="showAll = false"
            class="text-white text-sm font-medium rounded-md bg-white bg-opacity-0 px-3 py-2 hover:bg-opacity-10"
            aria-current="page"
          >
            See only bookmarked
          </button>

          <button
            v-if="!showAll"
            @click="showAll = true"
            class="text-white text-sm font-medium rounded-md bg-white bg-opacity-0 px-3 py-2 hover:bg-opacity-10"
            aria-current="false"
          >
            See all inboxes
          </button>
        </nav>
      </div>
    </div>
    <inboxes-grid v-if="!showAll" :inboxes="bookmarked" />
    <inboxes-grid v-if="showAll && userInboxes" :inboxes="userInboxes" />
    <div v-if="(!showAll && !bookmarked.length)" class="flex flex-col items-center w-full">
      <img
        src="/static/img/svg/undraw_empty_street_sfxm.svg"
        alt="Nothing here"
        class="w-1/2 md:w-1/3 mx-auto py-8"
      />
      <span class="text-gray-600 text-lg md:text-xl">
        {{ showAll ? 'You have no inboxes' : 'Bookmarking inboxes makes them appear here' }}
      </span>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Inboxes",
  data: () => ({
    userInboxes: [],
    showAll: false
  }),
  computed: {
    bookmarked() {
      return this.userInboxes.filter((inbox) => inbox.is_bookmarked);
    },
  },
  async mounted() {
    const response = await axios.get("/api/me/inboxes");
    this.userInboxes = response.data;

    if (this.bookmarked.length == 0) this.showAll = true
  },
};
</script>
