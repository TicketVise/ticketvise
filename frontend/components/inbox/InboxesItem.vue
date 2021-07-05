<template>
  <div class="bg-white relative rounded">
    <router-link :to="`/inboxes/${inbox.inbox.id}/tickets`" class="" aria-label="more options">
      <div class="h-64 w-full rounded hover:shadow-2xl transition-shadow ease-in-out duration-100"
          :style="{'background-color': inbox.inbox.color}">
        <img class="h-64 w-full rounded object-cover opacity-75" :src="inbox.inbox.image"
            :alt="inbox.inbox.name">
      </div>
    </router-link>

    <div class="absolute bottom-0 bg-gray-800 bg-opacity-50 w-full text-white flex py-2 px-4 space-x-2 rounded-br rounded-bl shadow-lg"
        style="overflow: hidden; text-overflow: ellipsis;">
      <button type="button" @click="onBookmarkClick(inbox)" class="pl-0 focus:outline-none self-start">
        <i v-if="inbox.is_bookmarked" class="fa fa-bookmark"></i>
        <i v-else class="fa fa-bookmark-o"></i>
      </button>

      <router-link :to="`/inboxes/${inbox.inbox.id}/tickets`" class="font-bold">{{ inbox.inbox.name }}</router-link>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    inbox: {
      required: true,
      type: Object
    }
  },
  methods: {
    onBookmarkClick: function (inbox) {
      inbox.is_bookmarked = !inbox.is_bookmarked

      axios.post('/api/me/inboxes', {"inbox_id": inbox.inbox.id})
    }
  }
}
</script>
