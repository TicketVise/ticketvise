<template>
  <div class="flex flex-col h-screen">
    <nav class="bg-gray-800 sticky top-0 z-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <router-link to="/" class="flex items-center">
                <img class="h-8 w-8" src="/static/img/logo/logo.svg" alt="Logo">
                <span class="text-2xl ml-2 text-white">Ticket</span><span
                  class="text-2xl text-primary font-bold">Vise</span>
              </router-link>
            </div>
            <div class="hidden md:block">
              <div class="ml-10 flex items-baseline space-x-4">
                <router-link to="/inboxes"
                             class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700
                 focus:outline-none focus:text-white focus:bg-gray-700"
                             active-class="text-white bg-gray-900">Inboxes
                </router-link>
                <router-link v-if="user.is_superuser" to="/admin"
                             class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700
                 focus:outline-none focus:text-white focus:bg-gray-700"
                             active-class="ext-white bg-gray-900">Admin
                </router-link>
              </div>
            </div>
          </div>
          <div v-on-clickaway="away">
            <div class="hidden md:block">
            <div class="ml-4 flex items-center md:ml-6">
              <div class="relative flex">
                <button type="button"
                        class="relative cursor-pointer px-2 py-1 border-2 border-transparent text-gray-400 rounded-full
                      hover:text-white focus:outline-none focus:text-white focus:bg-gray-700"
                        aria-label="Fullscreen" @click="openInTab()" v-show="isFramed()" style="display: none">
                  <i class="fa fa-arrows-alt text-lg" aria-hidden="true"></i>
                </button>

                <div>
                  <button
                      class="relative cursor-pointer px-2 py-1 border-2 border-transparent text-gray-400 rounded-full
                    hover:text-white focus:outline-none focus:text-white focus:bg-gray-700"
                      aria-label="Support" aria-haspopup="true" @click="toggleSupport()">
                    <i class="fa fa-question-circle text-xl" aria-hidden="true"></i>
                  </button>
                  <div class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg"
                       v-show="openSupport" @click="toggleSupport()">
                    <div class="py-1 rounded-md bg-white ring-1 ring-black ring-opacity-5" role="menu" aria-orientation="vertical"
                         aria-labelledby="user-menu">
                      <a href="https://ticketvise.com/getting-started/" target="_blank"
                                   class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                                   role="menuitem">Getting started
                      </a>
                      <a href="mailto:info@ticketvise.com?subject=Feedback&body=Hi%20TicketVise,"
                         target="_blank"
                         rel="noopener noreferrer"
                         class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                         role="menuitem">Send feedback
                      </a>
                    </div>
                  </div>
                </div>
              </div>

              <router-link to="/notifications"
                           class="relative cursor-pointer p-1 border-2 border-transparent text-gray-400 rounded-full
               hover:text-white focus:outline-none focus:text-white focus:bg-gray-700"
                           aria-label="Notifications">
                <svg class="h-6 w-6" stroke="currentColor" fill="none" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4
                      0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
                </svg>
                <!--              {% number_of_unread_notifications user as count %}-->
                <!--              {% if count > 0 %}-->
                <!--              <div-->
                <!--                  class="flex justify-center items-center absolute top-0 transform translate-x-4 h-4 min-w-4 w-auto bg-primary rounded-full p-0.5">-->
                <!--                <span class="rounded-full text-white text-center text-2xs">{{ count }}</span>-->
                <!--              </div>-->
                <!--              {% endif %}-->
              </router-link>

              <!-- Profile dropdown -->
              <div class="ml-3 relative">
                <div>
                  <button
                      class="max-w-xs flex items-center text-sm rounded-full text-white focus:outline-none focus:shadow-solid"
                      id="user-menu" aria-label="User menu" aria-haspopup="true"
                      @click="toggleProfile()">
                    <img class="h-8 w-8 rounded-full"
                         :src="user.avatar_url"
                         alt="User profile">
                  </button>

                </div>
                <div class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg"
                     v-show="openProfile" @click="toggleProfile()">
                  <div class="py-1 rounded-md bg-white ring-1 ring-black ring-opacity-5" role="menu" aria-orientation="vertical"
                       aria-labelledby="user-menu">
                    <router-link to="/account" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                                 role="menuitem">Account
                    </router-link>
                    <a href="#" @click="logout()" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                                 role="menuitem">Sign out
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="flex items-center md:hidden">
            <!-- Mobile menu button-->
            <button
                class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-white
              hover:bg-gray-700 focus:outline-none focus:bg-gray-700 focus:text-white transition duration-150
              ease-in-out" @click="toggleMobile()">
              <!-- Icon when menu is closed. -->
              <!-- Menu open: "hidden", Menu closed: "block" -->
              <svg class="block h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M4 6h16M4 12h16M4 18h16"/>
              </svg>
              <!-- Icon when menu is open. -->
              <!-- Menu open: "block", Menu closed: "hidden" -->
              <svg class="hidden h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
          </div>
        </div>
      </div>

      <div v-show="openMobile" @click="toggleMobile()">
        <div class="px-2 pt-2 pb-3 sm:px-3 space-y-1">
          <router-link to="/inboxes"
                       class="block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-white hover:bg-gray-700
           focus:outline-none focus:text-white focus:bg-gray-700"
                       active-class="text-white bg-gray-900">Inboxes
          </router-link>
          <router-link to="/notifications"
                       class="flex flex-row items-center px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-white
           hover:bg-gray-700 focus:outline-none focus:text-white focus:bg-gray-700"
                       active-class="text-white bg-gray-900">
            Notifications

            <!--          {% number_of_unread_notifications user as count %}-->
            <!--          {% if count > 0 %}-->
            <!--          <div class="flex justify-center items-center h-4 min-w-4 bg-primary rounded-full ml-2">-->
            <!--            <span class="rounded-full text-white text-center text-2xs">{{ count }}</span>-->
            <!--          </div>-->
            <!--          {% endif %}-->

          </router-link>
          <router-link v-if="user.is_superuser" to="/admin"
                       class="block px-3 py-2 rounded-md text-base font-medium text-gray-300 hover:text-white hover:bg-gray-700
           focus:outline-none focus:text-white focus:bg-gray-700"
                       active-class="text-white bg-gray-900">Admin
          </router-link>
        </div>
        <div class="pt-4 pb-3 border-t border-gray-700">
          <div class="flex items-center px-5">
            <div class="flex-shrink-0">
              <img class="h-10 w-10 rounded-full" :src="user.avatar_url" alt="Profile image">
            </div>
            <div class="ml-3">
              <div class="text-base font-medium leading-none text-white">{{ user.full_name }}</div>
              <div class="mt-1 text-sm font-medium leading-none text-gray-400">{{ user.email }}</div>
            </div>
          </div>
          <div class="mt-3 px-2 space=y-1">
            <router-link to="/account"
                         class="block px-3 py-2 rounded-md text-base font-medium text-gray-400 hover:text-white hover:bg-gray-700
             focus:outline-none focus:text-white focus:bg-gray-700">Your
              Account
            </router-link>
                    <a href="#" @click="logout()"
                         class="block px-3 py-2 rounded-md text-base font-medium text-gray-400 hover:text-white hover:bg-gray-700
             focus:outline-none focus:text-white focus:bg-gray-700">Sign
              out
            </a>
          </div>
        </div>
      </div>
    </nav>

    <div class="h-full overflow-y-auto">
      <slot />
    </div>
  </div>
</template>

<script>
import {mixin as clickaway} from 'vue-clickaway'
import {hasLocalStorage} from "../utils";
import store from "../store";

export default {
  name: "Navigation",
  mixins: [clickaway],
  data: () => ({
    openProfile: false,
    openSupport: false,
    openMobile: false
  }),
  methods: {
    away() {
      this.openProfile = false
      this.openSupport = false
      this.openMobile = false
    },
    toggleProfile() {
      this.openSupport = false
      this.openMobile = false
      this.openProfile = !this.openProfile
    },
    toggleSupport() {
      this.openSupport = !this.openSupport
      this.openMobile = false
      this.openProfile = false
    },
    toggleMobile() {
      this.openSupport = false
      this.openMobile = !this.openMobile
      this.openProfile = false
    },
    isFramed() {
      return window.self !== window.top
    },
    logout() {
      this.$store.dispatch("logout")
    },
    openInTab() {
      if (hasLocalStorage) {
        window.open(window.location.href, '_blank')
      } else {
        const url = new URL(window.location.href)
        url.searchParams.append("token", store.state.token);

        window.open(url.href, '_blank')
      }
    }
  },
  computed: {
    user() {
      return this.$store.state.user
    }
  }
}
</script>
