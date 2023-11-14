<template>
  <div class="h-screen flex flex-col">
    <!-- TicketVise Header -->
    <header class="bg-gray-800 dark:border-b dark:border-white">
      <div class="w-full">
        <div class="relative flex flex-wrap items-center justify-between">
          <div class="flex items-center">
            <!-- Logo -->
            <div class="left-0 p-4 flex-shrink-0">
              <router-link to="/" class="flex items-center">
                <img class="h-8 w-auto" :src="logo" alt="TicketVise" />
                <span class="font-semibold text-2xl ml-2 text-white">Ticket</span>
                <span class="text-2xl text-primary font-bold">Vise</span>
              </router-link>
            </div>
            <!-- <div class="block ml-4 sm:ml-10">
              <div class="flex space-x-4">
                <router-link
                  to="/dashboard"
                  class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 focus:outline-none focus:text-white focus:bg-gray-700"
                  active-class="text-white bg-gray-900"
                >
                  Dashboard
                </router-link>
                <router-link
                  v-if="user.is_superuser"
                  to="/admin"
                  class="hidden sm:block px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 focus:outline-none focus:text-white focus:bg-gray-700"
                  active-class="text-gray-100 bg-gray-800"
                >
                  Admin
                </router-link>
              </div>
            </div> -->
          </div>

          <!-- <div
            class="flex flex-1 justify-center lg:justify-end mx-auto max-w-2xl"
          >
            <div class="w-full px-2 lg:px-6">
              <label for="search" class="sr-only">Search</label>
              <div class="relative text-gray-200 focus-within:text-gray-400">
                <div
                  class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3"
                >
                  <svg
                    class="h-5 w-5"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </div>
                <button
                  class="block w-full rounded-md border border-transparent bg-gray-400 bg-opacity-25 py-2 pl-10 pr-3 leading-5 text-gray-100 placeholder-gray-200 text-left sm:text-sm"
                  @click="search = true"
                >Search</button>
              </div>
            </div>
          </div> -->

          <!-- Right section on desktop -->
          <div class="flex items-center">
            <button type="button"
                    class="inline-flex items-center justify-center py-1 px-4 border border-transparent rounded-md shadow-sm text-white bg-primary hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 mr-4 space-x-2"
                    aria-label="Fullscreen" @click="openInTab()" v-if="isFramed()">
                    <span>New Tab</span>
                    <ArrowTopRightOnSquareIcon class="h-5 w-5" />
            </button>

            <router-link
              to="/notifications"
              type="button"
              class="flex-shrink-0 p-1 text-gray-200 rounded-full hover:text-white hover:bg-white hover:bg-opacity-10 focus:outline-none focus:ring-2 focus:ring-white"
            >
              <span class="sr-only">View notifications</span>
              <BellIcon class="h-6 w-6" aria-hidden="true"/>
            </router-link>

            <!-- Profile dropdown -->
            <Menu as="div" class="p-4 relative flex-shrink-0">
              <div>
                <MenuButton
                  class="bg-white rounded-full flex text-sm ring-2 ring-white ring-opacity-20 focus:outline-none focus:ring-opacity-100"
                >
                  <span class="sr-only">Open user menu</span>
                  <img
                    class="h-8 w-8 rounded-full"
                    :src="user.avatar_url"
                    alt=""
                  />
                </MenuButton>
              </div>
              <transition
                leave-active-class="transition ease-in duration-75"
                leave-from-class="transform opacity-100 scale-100"
                leave-to-class="transform opacity-0 scale-95"
              >
                <MenuItems
                  class="origin-top-right z-40 absolute right-2 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none"
                >
                  <MenuItem v-slot="{ active }">
                    <router-link
                      to="/account"
                      :class="[
                        active ? 'bg-gray-100' : '',
                        'block px-4 py-2 text-sm text-gray-700',
                      ]"
                      >Your profile
                    </router-link>
                  </MenuItem>
                  <MenuItem v-slot="{ active }">
                    <a
                      href="#"
                      @click="logout()"
                      :class="[
                        active ? 'bg-gray-100' : '',
                        'block px-4 py-2 text-sm text-gray-700',
                      ]"
                      >Sign out</a
                    >
                  </MenuItem>
                </MenuItems>
              </transition>
            </Menu>
          </div>
        </div>
      </div>
    </header>

    <div class="flex overflow-hidden bg-white dark:bg-gray-800 h-full">
      <SideMenu class="hidden md:flex" />

      <!-- Main column -->
      <div class="flex flex-col w-0 flex-1 overflow-y-auto">
        <div class="flex md:hidden flex-col px-4 pb-2 bg-gray-800">
          <div class="flex justify-between items-center space-x-2">
            <router-link
              v-if="inbox"
              :to="{ name: 'Overview', params: { inboxId: inbox.inbox.id } }"
              class="text-gray-200 text-sm truncate flex items-center space-x-1"
            >
              <ChevronLeftIcon class="h-3 w-3" />
              <span>{{ inbox.inbox.name }}</span>
            </router-link>
          </div>
        </div>

        <!-- <hr
          class="md:hidden border-t border-gray-200 mt-2"
          aria-hidden="true"
        /> -->

        <main
          class="flex-1 relative focus:outline-none flex flex-col pb-16 md:pb-0"
        >
          <slot />
        </main>
      </div>

      <!-- Bottom menubar -->
      <MenuBottom class="block md:hidden" />
    </div>
  </div>

  <getting-started
    @update="user.give_introduction = false"
    v-if="onboarding.active && onboarding.popup"
  />
  <develop-panel v-if="development" />

  <SearchPopup :show="search" v-on:close="search = false" />
</template>

<script>
import axios from "axios"
import store from "@/store"
import { mapState } from "vuex"

import GettingStarted from "@/components/onboarding/GettingStarted.vue"
import DevelopPanel from "@/components/devpanel/DevelopPanel.vue"
import SideMenu from "@/layouts/elements/SideMenu.vue"
import MenuBottom from "@/layouts/elements/MenuBottom.vue"
import SearchPopup from "@/layouts/elements/SearchPopup.vue"

import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue"
import { BellIcon, ArrowTopRightOnSquareIcon, ChevronLeftIcon } from "@heroicons/vue/24/outline"

import logo from "@/assets/logo/logo.svg"

export default {
  components: {
    BellIcon,
    ChevronLeftIcon,
    SideMenu,
    MenuBottom,
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    ArrowTopRightOnSquareIcon,
    GettingStarted,
    DevelopPanel,
    SearchPopup
  },
  setup() {
    return {
      logo,
    }
  },
  data: () => ({
    inboxes: [],
    inbox: null,
    side: false,
    search: false
  }),
  async mounted() {
    const response = await axios.get(
      `/api/me/inboxes/${this.$route.params.inboxId}`
    )
    this.inbox = response.data
  },
  methods: {
    async goto(index) {
      this.$router.push("/inboxes/" + index + "/tickets")
      const response = await axios.get(`/api/me/inboxes/${index}`)
      this.inbox = response.data
    },
    logout() {
      this.$store.dispatch("logout")
    },
    isFramed() {
      return window.self !== window.top
    },
    openInTab() {
      const url = new URL(window.location.href)
      url.searchParams.append("token", store.state.token)
      window.open(url.href, "_blank")
    },
  },
  computed: {
    ...mapState({
      user: (state) => state.user,
    }),
    ...mapState('onboarding', {
      onboarding: (state) => state.status
    }),
    is_staff() {
      if (!this.inbox) {
        return false
      }

      const role = this.inbox.role
      return (
        (this.user && this.user.is_superuser) ||
        (role && (role === "AGENT" || role === "MANAGER"))
      )
    },
    development: () => import.meta.env.DEV,
  },
  watch: {
    inbox: async function (newVal) {
      const response = await axios.get("/api/me/inboxes")
      this.inboxes = []
      for (const inbox of response.data) {
        if (inbox.inbox.id === newVal.inbox.id) continue
        this.inboxes.push(inbox)
      }
    },
    $route: async function () {
      this.menu = false
    },
  },
}
</script>
