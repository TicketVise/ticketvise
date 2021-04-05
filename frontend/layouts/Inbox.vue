<template>
  <div class="h-screen flex flex-col">
    <page-header :inbox="inbox" />

    <div class="h-full flex overflow-hidden bg-white">

      <inbox-menu ref="menu" :inbox="inbox" v-on:goto="updateInbox" />

      <div class="flex flex-col w-0 h-full flex-1">
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

        <slot />
      </div>

      <div v-show="user.is_superuser && showAlert" class="absolute top-8 flex justify-center w-full">
        <div class="mx-auto shadow-xl rounded-md bg-yellow-50 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <!-- Heroicon name: solid/exclamation -->
              <svg class="h-5 w-5 text-yellow-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-yellow-800">
                Pay attention!
              </h3>
              <div class="mt-2 text-sm text-yellow-700">
                <p>
                  You are visiting this inbox page as an admin of the platform. Go back if you don't have anything to do here because you are working with real data.
                </p>
              </div>
            </div>
            <div class="ml-auto pl-3">
              <div class="-mx-1.5 -my-1.5">
                <button @click="showAlert = false" type="button" class="inline-flex bg-yellow-50 rounded-md p-1.5 text-yellow-500 hover:bg-yellow-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-yellow-50 focus:ring-yellow-600">
                  <span class="sr-only">Dismiss</span>
                  <!-- Heroicon name: solid/x -->
                  <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
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
    openSupport: false,
    showAlert: true
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
