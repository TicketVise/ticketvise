<template>
  <div class="flex flex-col min-w-0 flex-1 overflow-hidden">
    <div class="flex-1 relative z-0 flex overflow-hidden">
      <main
        class="flex-1 relative z-0 overflow-y-auto focus:outline-none order-last"
        tabindex="0"
      >
        <!-- Breadcrumb -->
        <nav
          v-show="selected"
          class="flex items-start px-4 py-3 sm:px-6 lg:px-8 lg:hidden"
          aria-label="Breadcrumb"
        >
          <router-link :to="{ name: 'Users', params: { inboxId: $route.params.inboxId }}"
            class="inline-flex items-center space-x-3 text-sm font-medium text-gray-900"
          >
            <!-- Heroicon name: solid/chevron-left -->
            <svg
              class="-ml-2 h-5 w-5 text-gray-400"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
              aria-hidden="true"
            >
              <path
                fill-rule="evenodd"
                d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
                clip-rule="evenodd"
              />
            </svg>
            <span>List of users</span>
          </router-link>
        </nav>

        <article v-if="selected">
          <!-- Profile header -->
          <div>
            <div>
              <img
                class="h-32 w-full object-cover lg:h-48"
                src="https://images.unsplash.com/photo-1523978591478-c753949ff840?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
                alt=""
              />
            </div>
            <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
              <div class="-mt-12 sm:-mt-16 sm:flex sm:items-end sm:space-x-5">
                <div class="flex">
                  <img
                    class="h-24 w-24 rounded-full ring-4 ring-white sm:h-32 sm:w-32"
                    :src="selected.user.avatar_url"
                    alt=""
                  />
                </div>
                <div
                  class="mt-6 sm:flex-1 sm:min-w-0 sm:flex sm:items-center sm:justify-end sm:space-x-6 sm:pb-1"
                >
                  <div class="sm:hidden 2xl:block mt-6 min-w-0 flex-1">
                    <h1 class="text-2xl font-bold text-gray-900 dark:text-white truncate">
                      {{ selected.user.first_name }} {{ selected.user.last_name }}
                    </h1>
                  </div>
                </div>
              </div>
              <div class="hidden sm:block 2xl:hidden mt-6 min-w-0 flex-1">
                <h1 class="text-2xl font-bold text-gray-900 dark:text-white truncate">
                  {{ selected.user.first_name }} {{ selected.user.last_name }}
                </h1>
              </div>
            </div>
          </div>

          <!-- Tabs -->
          <div class="mt-6 sm:mt-2 2xl:mt-5">
            <div class="border-b border-gray-200">
              <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
                <nav class="-mb-px flex space-x-8" aria-label="Tabs">
                  <div
                    @click="tab = 'profile'"
                    class="border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm cursor-pointer"
                    :class="tab == 'profile' ? 'border-primary text-gray-900' : 'hover:border-gray-300'"
                    aria-current="page"
                  >
                    Profile
                  </div>

                  <div
                    @click="tab = 'tickets'"
                    class="border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm cursor-pointer"
                    :class="tab == 'tickets' ? 'border-primary text-gray-900' : 'hover:border-gray-300'"
                  >
                    Tickets
                    <span
                      class="bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-200 dark:border inline-block ml-2 py-0.5 px-2.5 rounded-full text-xs font-medium"
                      :class="tab == 'tickets' ? 'bg-orange-100 dark:bg-orange-100 text-orange-600' : ''"
                    >
                      {{ tickets.length }}
                    </span>
                  </div>

                  <div
                    @click="tab = 'settings'"
                    class="border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm cursor-pointer"
                    :class="tab == 'settings' ? 'border-primary text-gray-900' : 'hover:border-gray-300'"
                  >
                    Settings
                  </div>

                  <!-- <div
                    @click="tab = 'insights'"
                    class="border-transparent text-gray-500 hover:text-gray-700 whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm cursor-pointer"
                    :class="tab == 'insights' ? 'border-primary text-gray-900' : 'hover:border-gray-300'"
                  >
                    Insights
                  </div> -->
                </nav>
              </div>
            </div>
          </div>

          <!-- Description list -->
          <div
            v-show="tab == 'profile'"
            class="mt-6 max-w-5xl mx-auto px-4 sm:px-6 lg:px-8"
          >
            <dl class="grid grid-cols-1 gap-x-4 gap-y-8 sm:grid-cols-2">
              <div class="sm:col-span-1">
                <dt class="text-sm font-medium text-gray-500 dark:text-gray-400">Role</dt>
                <dd class="mt-1 text-sm text-gray-900 dark:text-gray-100">
                  {{ selected.role_label }}
                </dd>
              </div>

              <div class="sm:col-span-1">
                <dt class="text-sm font-medium text-gray-500 dark:text-gray-400">Email</dt>
                <dd class="mt-1 text-sm text-gray-900 dark:text-gray-100">
                  {{ selected.user.email }}
                </dd>
              </div>

              <div class="sm:col-span-1">
                <dt class="text-sm font-medium text-gray-500 dark:text-gray-400">Full Name</dt>
                <dd class="mt-1 text-sm text-gray-900 dark:text-gray-100">
                  {{ selected.user.first_name }} {{ selected.user.last_name }}
                </dd>
              </div>

              <div class="sm:col-span-1">
                <dt class="text-sm font-medium text-gray-500 dark:text-gray-400">Username</dt>
                <dd class="mt-1 text-sm text-gray-900 dark:text-gray-100">
                  {{ selected.user.username }}
                </dd>
              </div>
            </dl>

            <!-- Statistics -->
            <div class="mt-8 pb-4">
              <h2 class="text-sm font-medium text-gray-500 dark:text-gray-400">Statistics</h2>
              <div class="mt-1 grid grid-cols-1 gap-4 sm:grid-cols-3">
                <div
                  class="rounded border flex-grow py-2 px-4 flex md:flex-col-reverse space-x-2 md:space-x-0 items-center md:items-start"
                >
                  <div class="flex items-baseline sm:mt-1">
                    <h2 class="text-2xl font-medium text-primary">{{ tickets.length }}</h2>
                  </div>
                  <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-gray-100">
                    Tickets
                  </h3>
                </div>

                <div
                  class="rounded border flex-grow py-2 px-4 flex md:flex-col-reverse space-x-2 md:space-x-0 items-center md:items-start"
                >
                  <div class="flex items-baseline mt-1">
                    <h2 class="text-2xl font-medium text-primary">{{ publicTickets }}</h2>
                  </div>
                  <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-gray-100">
                    Public tickets
                  </h3>
                </div>

                <div
                  class="rounded border flex-grow py-2 px-4 flex md:flex-col-reverse space-x-2 md:space-x-0 items-center md:items-start"
                >
                  <div class="flex items-baseline sm:mt-1">
                    <h2 class="text-2xl font-medium text-primary">{{ average }}<span class="text-gray-400 text-xs"> / per inbox</span></h2>
                  </div>
                  <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-gray-100">
                    Average tickets
                  </h3>
                </div>
              </div>
            </div>
          </div>

          <!-- Tickets list -->
          <div v-show="tab == 'tickets'" class="mt-6 max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="space-y-2 mb-4" v-if="tickets.length > 0">
              <ticket-card
                :key="ticket.id"
                :ticket="ticket"
                v-for="ticket in tickets" />
            </div>

            <div v-else class="text-center mb-4">
              <img
                :src="BlankCanvas"
                alt="Nothing here"
                class="w-1/2 md:w-1/3 mx-auto py-8"
              />
              <span class="text-gray-600 text-lg md:text-xl">
                This user doesn't have any tickets yet
              </span>
            </div>
          </div>

          <!-- User inbox settings -->
          <div v-show="tab == 'settings'" class="mt-6 max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col space-y-8">
            <div v-if="selected.role !== 'GUEST'" class="space-y-2 mb-4">
              <SwitchGroup as="div" class="flex items-center justify-between">
                <span class="flex-grow flex flex-col">
                  <SwitchLabel as="span" class="text-sm font-medium text-gray-900" passive>Assignable</SwitchLabel>
                  <SwitchDescription as="span" class="text-sm text-gray-500">This user is assignable using the automatic scheduler.</SwitchDescription>
                </span>
                <Switch v-if="selected" :change="save()" v-model="selected.is_assignable" :class="[selected.is_assignable ? 'bg-primary-600' : 'bg-gray-200', 'relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary']">
                  <span aria-hidden="true" :class="[selected.is_assignable ? 'translate-x-5' : 'translate-x-0', 'pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']" />
                </Switch>
              </SwitchGroup>
            </div>

            <div>
              <div class="border border-red-600 overflow-hidden rounded p-4 mt-2 mb-4">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  Remove user
                </h3>
                <p class="mt-1 max-w-2xl text-sm leading-5 text-gray-500">
                  The user will lose access to the inbox and will be unable to create new tickets or answer tickets.
                </p>
                <button type="button" @click="onDelete()"
                        class="w-full sm:w-auto mt-4 inline-flex justify-center items-center rounded-md border border-transparent px-4 py-2 bg-red-200 text-red-600 co text-base leading-6 font-medium shadow-sm hover:bg-red-100 focus:outline-none focus:border-red-700 focus:ring-red transition ease-in-out duration-150 sm:text-sm sm:leading-5">
                  <TrashIcon class="h-5 w-5 text-red-600 mr-2" />
                  Remove
                </button>
              </div>
            </div>
          </div>
        </article>
      </main>

      <!-- Users list -->
      <aside
        class="w-full lg:w-96 lg:border-r order-first flex flex-col border-gray-200"
        :class="{ 'hidden lg:flex lg:flex-col flex-shrink-0': selected}"
      >
        <div class="p-4">
          <h2 class="text-lg font-medium text-gray-900 dark:text-gray-200">Inbox Users</h2>
          <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">
            Search users of {{ users ? users.length : "" }} total
          </p>
          <div class="mt-6 flex space-x-4 items-center">
            <search-bar small v-model="query" v-on:input="search" class="flex-grow my-2"/>

            <Menu as="div" class="relative inline-block text-left">
              <div>
                <MenuButton class="inline-flex justify-center w-full rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white dark:bg-gray-800 text-sm font-medium text-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-100 dark:focus:ring-offset-gray-800 focus:ring-primary">
                  <svg
                    class="h-5 w-5 text-gray-400"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M3 3a1 1 0 011-1h12a1 1 0 011 1v3a1 1 0 01-.293.707L12 11.414V15a1 1 0 01-.293.707l-2 2A1 1 0 018 17v-5.586L3.293 6.707A1 1 0 013 6V3z"
                      clip-rule="evenodd"
                    />
                  </svg>
                </MenuButton>
              </div>

              <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
                <MenuItems class="origin-top-right absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white dark:bg-gray-900 dark:border ring-1 ring-black ring-opacity-5 focus:outline-none z-20">
                  <div class="py-1">
                    <MenuItem v-slot="{ active }">
                      <a @click="filter = 'name'; performSearch()" :class="[active ? 'bg-gray-100 text-gray-900 dark:bg-transparent dark:text-gray-100' : 'text-gray-700 dark:text-gray-300', 'block px-4 py-2 text-sm cursor-pointer']">Name</a>
                    </MenuItem>
                    <MenuItem v-slot="{ active }">
                      <a @click="filter = 'function'; performSearch()" :class="[active ? 'bg-gray-100 text-gray-900 dark:bg-transparent dark:text-gray-100' : 'text-gray-700 dark:text-gray-300', 'block px-4 py-2 text-sm cursor-pointer']">Function</a>
                    </MenuItem>
                  </div>
                </MenuItems>
              </transition>
            </Menu>
          </div>
        </div>

        <!-- Users list -->
        <nav class="flex-1 min-h-0 overflow-y-auto" aria-label="Users">
          <div v-if="Object.keys(sorted).length == 0" class="text-center">
            <img
              :src="Empty"
              alt="Nothing here"
              class="w-3/5 mx-auto py-8"
            />
            <span class="text-gray-600 text-lg">
              We couldn't find any users
            </span>
          </div>
          <div class="relative" v-for="(list, letter) in sorted" :key="letter">
            <div
              class="z-10 sticky top-0 border-t border-b border-gray-200 bg-gray-50 dark:bg-gray-700 px-6 py-1 text-sm font-medium text-gray-500 dark:text-gray-300"
            >
              <h3>{{ letter }}</h3>
            </div>
            <ul class="relative z-0 divide-y divide-gray-200">
              <li v-for="user in list" :key="user.user.id">
                <div
                  class="relative px-6 py-5 flex items-center space-x-3 hover:bg-gray-50 dark:hover:bg-gray-700 focus-within:ring-2 focus-within:ring-inset focus-within:ring-primary"
                >
                  <div class="flex-shrink-0">
                    <img
                      class="h-10 w-10 rounded-full"
                      :src="user.user.avatar_url"
                      alt=""
                    />
                  </div>
                  <div class="flex-1 min-w-0">
                    <router-link :to="{ name: 'User', params: { inboxId: $route.params.inboxId, userId: user.user.id }}"
                      class="cursor-pointer focus:outline-none"
                    >
                      <!-- Extend touch target to entire panel -->
                      <span class="absolute inset-0" aria-hidden="true"></span>
                      <p class="text-sm font-medium text-gray-900 dark:text-gray-200">
                        {{ user.user.first_name }} {{ user.user.last_name }}
                      </p>
                      <p class="text-sm text-gray-500 truncate">
                        {{ user.role_label }}
                      </p>
                    </router-link>
                  </div>
                </div>
              </li>
            </ul>

          </div>
        </nav>
      </aside>
    </div>
  </div>
</template>

<script>
import TicketCard from '@/components/tickets/TicketCard.vue'
import SearchBar from '@/components/searchbar/SearchBar.vue'
import axios from 'axios'
import { debounce } from 'lodash'
import { Menu, MenuButton, MenuItem, MenuItems, Switch, SwitchDescription, SwitchGroup, SwitchLabel } from '@headlessui/vue'
import {
  TrashIcon
} from '@heroicons/vue/outline'

import Empty from '@/assets/img/svg/empty.svg'
import BlankCanvas from '@/assets/img/svg/blank_canvas.svg'

export default {
  name: 'Users',
  components: {
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    Switch,
    SwitchDescription,
    SwitchGroup,
    SwitchLabel,
    TrashIcon,
    SearchBar,
    TicketCard
  },
  data () {
    return {
      query: '',
      users: [],
      sorted: [],
      tab: 'profile',
      tickets: [],
      average: 0,
      filter_menu: false,
      filter: 'name',
      user: null
    }
  },
  setup () {
    return { Empty, BlankCanvas }
  },
  async mounted () {
    const { inboxId } = this.$route.params
    await axios.get(`/api/inboxes/${inboxId}/users`).then((response) => {
      this.users = response.data
    })

    this.performSearch()
  },
  methods: {
    away () {
      this.filter_menu = false
    },
    save () {
      const { inboxId, userId } = this.$route.params

      axios.put(`/api/inboxes/${inboxId}/users/${userId}`, this.selected)
    },
    onDelete () {
      if (confirm('Are you sure you want to delete this user?')) {
        const { inboxId, userId } = this.$route.params
        axios.delete(`/api/inboxes/${inboxId}/users/${userId}`).then(() => this.$route.push('Users'))
      }
    },
    performSearch () {
      const inboxId = this.$route.params.inboxId
      axios
        .get(`/api/inboxes/${inboxId}/users`, {
          params: {
            q: this.query
          }
        })
        .then((response) => {
          /* Group users by letter. */
          const grouped = {}
          for (const user of response.data) {
            if (this.filter === 'name') {
              if (!grouped[user.user.first_name[0]]) {
                grouped[user.user.first_name[0]] = [user]
              } else {
                grouped[user.user.first_name[0]].push(user)
              }
            } else if (this.filter === 'function') {
              if (!grouped[user.role_label]) {
                grouped[user.role_label] = [user]
              } else {
                grouped[user.role_label].push(user)
              }
            }
          }

          let keys = Object.keys(grouped).sort()
          if (this.filter === 'function') {
            keys = Object.keys(grouped).sort((a, b) => grouped[a].length - grouped[b].length)
          }

          const sorted = {}
          keys.forEach((v) => {
            sorted[v] = grouped[v]
          })

          this.sorted = sorted
        })
    },
    search: debounce(function () {
      this.performSearch()
    }, 250)
  },
  watch: {
    selected () {
      const { inboxId, userId } = this.$route.params

      if (!userId) return

      this.tab = 'profile'

      axios.get(`/api/inboxes/${inboxId}/users/${userId}/tickets`).then((response) => {
        this.tickets = response.data
      })

      axios.get(`/api/inboxes/${inboxId}/users/${userId}/tickets/average`).then((response) => {
        this.average = response.data.average
      })
    }
  },
  computed: {
    publicTickets () {
      return this.tickets.filter(ticket => ticket.is_public).length
    },
    selected () {
      return this.users?.find((user) => user.user.id === parseInt(this.$route.params.userId))
    }
  }
}
</script>
