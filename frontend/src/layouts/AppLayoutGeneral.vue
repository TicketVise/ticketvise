<template>
  <div class="min-h-screen bg-gray-100">
    <header class="pb-24 bg-gradient-to-r from-gray-800 to-gray-700">
      <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:max-w-7xl lg:px-8">
        <div class="relative flex flex-wrap items-center justify-between">
          <div class="flex items-center">
            <!-- Logo -->
            <div class="left-0 py-5 flex-shrink-0 static">
              <router-link to="/" class="flex items-center">
                <img class="h-8 w-auto" :src="logo" alt="TicketVise" />
                <span class="text-2xl ml-2 font-semibold text-white">Ticket</span
                ><span class="text-2xl text-primary font-bold">Vise</span>
              </router-link>
            </div>
            <div class="block ml-4 sm:ml-10">
              <div class="flex space-x-4">
                <!-- <router-link
                  to="/dashboard"
                  class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 focus:outline-none focus:text-white focus:bg-gray-700"
                  active-class="text-gray-100 bg-gray-800"
                >
                  Dashboard
                </router-link> -->
                <router-link
                  v-if="user.is_superuser"
                  to="/admin"
                  class="hidden sm:block px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 focus:outline-none focus:text-white focus:bg-gray-700"
                  active-class="text-gray-100 bg-gray-800"
                >
                  Admin
                </router-link>
              </div>
            </div>
          </div>

          <!-- Right section on desktop -->
          <div class="flex lg:ml-4 lg:items-center lg:py-5 lg:pr-0.5">
            <button
              type="button"
              class="inline-flex items-center justify-center py-1 px-4 border border-transparent rounded-md shadow-sm text-white bg-primary hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 mr-4 space-x-2"
              aria-label="Fullscreen"
              @click="openInTab()"
              v-if="isFramed()"
            >
              <span>New Tab</span>
              <ArrowTopRightOnSquareIcon class="h-5 w-5" />
            </button>

            <router-link
              to="/notifications"
              type="button"
              class="flex-shrink-0 p-1 text-gray-200 rounded-full hover:text-white hover:bg-white hover:bg-opacity-10 focus:outline-none focus:ring-2 focus:ring-white"
            >
              <span class="sr-only">View notifications</span>
              <BellIcon class="h-6 w-6" aria-hidden="true" />
            </router-link>

            <!-- Profile dropdown -->
            <Menu as="div" class="ml-4 relative flex-shrink-0">
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
                  class="origin-top-right z-40 absolute -right-2 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none"
                >
                  <MenuItem v-slot="{ active }">
                    <router-link
                      to="/account"
                      :class="[
                        active ? 'bg-gray-100' : '',
                        'block px-4 py-2 text-sm text-gray-700',
                      ]"
                      >Your profile</router-link
                    >
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
    <main class="-mt-24 pb-8">
      <slot />
    </main>
    <footer>
      <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 lg:max-w-7xl">
        <div
          class="border-t border-gray-200 py-8 text-sm text-gray-500 text-center sm:text-left"
        >
          <span class="block sm:inline"
            >&copy; {{ new Date().getFullYear() }} TicketVise.</span
          >
          {{ " " }}
          <span class="block sm:inline">All rights reserved.</span>
        </div>
      </div>
    </footer>
  </div>

  <develop-panel v-if="development" />
</template>

<script>
import { mapState } from "vuex";

import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
import { BellIcon, ArrowTopRightOnSquareIcon } from "@heroicons/vue/24/outline";

import DevelopPanel from "@/components/devpanel/DevelopPanel.vue";

import logo from "@/assets/logo/logo.svg";

export default {
  name: "AppLayoutGeneral",
  components: {
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    ArrowTopRightOnSquareIcon,
    BellIcon,
    DevelopPanel,
  },
  setup() {
    return {
      logo,
    };
  },
  computed: {
    ...mapState({
      user: (state) => state.user,
    }),
    development: () => import.meta.env.DEV,
  },
  methods: {
    logout() {
      this.$store.dispatch("logout");
    },
    isFramed() {
      return window.self !== window.top;
    },
    openInTab() {
      const url = new URL(window.location.href);
      url.searchParams.append("token", this.$store.state.token);
      window.open(url.href, "_blank");
    },
  },
};
</script>
