<template>
  <div class="h-screen flex flex-col">
    <page-header :inbox="inbox" />

    <div class="h-full flex overflow-hidden bg-white">

      <inbox-menu ref="menu" :inbox="inbox" v-on:goto="updateInbox" />

      <div class="flex flex-col w-0 flex-1">
        <div class="flex flex-col md:hidden px-4 pt-2">
          <div class="flex justify-between items-center space-x-2">
            <h2 v-if="inbox" class="font-bold leading-6 text-gray-900 text-lg truncate">
              {{ inbox.inbox.name }}
            </h2>
            <div v-else class="h-7 w-full max-w-screen-sm bg-gray-200 rounded" />
          </div>

          <div class="flex space-x-2 mt-1">
            <div class="flex items-center text-xs text-gray-500">
              <!-- Heroicon name: code -->
              <svg
                class="w-4 h-4 mr-1"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"
                ></path>
              </svg>
              <span v-if="inbox">{{ inbox.inbox.code }}</span>
              <div v-else class="h-5 w-24 bg-gray-200 rounded" />
            </div>
            <div class="flex items-center text-xs text-gray-500">
              <!-- Heroicon name: user -->
              <svg
                class="w-4 h-4 mr-1"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                ></path>
              </svg>
              <span class="w-full truncate" v-if="inbox"
                >{{ inbox.inbox.coordinator.first_name }}
                {{ inbox.inbox.coordinator.last_name }}</span
              >
              <div v-else class="h-5 w-24 bg-gray-200 rounded" />
            </div>
          </div>
        </div>

        <hr
          class="md:hidden border-t border-gray-200 mt-2"
          aria-hidden="true"
        />

        <main
          class="flex-1 relative z-0 overflow-y-auto focus:outline-none"
          tabindex="0"
        >

          <slot />
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import {mixin as clickaway} from 'vue-clickaway'

export default {
  name: 'InboxLayout',
  mixins: [clickaway],
  data: () => ({
    inbox: null,
    side: false,
    openSupport: false
  }),
  async mounted() {
    const response = await axios.get(`api/me/inboxes/${this.$route.params.inboxId}`);
    this.inbox = response.data
  },
  computed: {
    user() {
      return this.$store.state.user
    },
    is_staff() {
      if (!this.inbox) {
        return false
      }

      const role = this.inbox.role
      return (this.user && this.user.is_superuser) || (role && (role === 'AGENT' || role === 'MANAGER'))
    }
  },
  methods: {
    isFramed() {
      return window.self !== window.top
    },
    openInTab() {
      if (hasLocalStorage) {
        window.open(window.location.href, '_blank')
      } else {
        const url = new URL(window.location.href)
        url.searchParams.append("token", store.state.token);
        window.open(url.href, '_blank')
      }
    },
    async updateInbox(id) {
      this.$router.push('/inboxes/' + id)
      const response = await axios.get(`api/me/inboxes/${this.$route.params.inboxId}`)
      this.inbox = response.data
    }
  }
};
</script>

<style>
</style>
