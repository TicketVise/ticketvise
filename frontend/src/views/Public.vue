<template>
  <!-- Pinned tickets -->
  <div class="px-4 mt-6 sm:px-6 lg:px-8">
    <h2 class="text-gray-500 dark:text-gray-300 text-xs font-medium uppercase tracking-wide">Pinned Tickets</h2>
    <ul class="grid grid-cols-1 gap-4 sm:gap-6 sm:grid-cols-2 xl:grid-cols-4 mt-3">
      <li v-for="ticket in pinnedTickets" :key="ticket.id" class="relative col-span-1 flex shadow-sm rounded-md">
        <div class="flex-1 flex items-center justify-between border border-gray-200 bg-white dark:bg-transparent rounded-md truncate">
          <div class="flex-1 px-4 py-2 text-sm truncate">
            <a href="#" class="text-gray-900 dark:text-gray-200 font-medium hover:text-gray-600 dark:hover:text-gray-400">
              {{ ticket.title }}
            </a>
            <p class="text-gray-500">{{ ticket.totalResponses }} Responses</p>
          </div>
          <Menu as="div" class="flex-shrink-0 pr-2">
            <MenuButton class="w-8 h-8 bg-white dark:bg-transparent inline-flex items-center justify-center text-gray-400 dark:text-gray-300 rounded-full hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
              <span class="sr-only">Open options</span>
              <DotsVerticalIcon class="w-5 h-5" aria-hidden="true" />
            </MenuButton>
            <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
              <MenuItems class="z-10 mx-3 origin-top-right absolute right-10 top-3 w-48 mt-1 rounded-md shadow-lg bg-white dark:bg-gray-900 dark:border ring-1 ring-black ring-opacity-5 divide-y divide-gray-200 focus:outline-none">
                <div class="py-1">
                  <MenuItem v-slot="{ active }">
                    <a href="#" :class="[active ? 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-300' : 'text-gray-700 dark:text-gray-200', 'block px-4 py-2 text-sm']">View</a>
                  </MenuItem>
                </div>
                <div class="py-1">
                  <MenuItem v-slot="{ active }">
                    <a href="#" :class="[active ? 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-300' : 'text-gray-700 dark:text-gray-200', 'block px-4 py-2 text-sm']">Removed from pinned</a>
                  </MenuItem>
                  <MenuItem v-slot="{ active }">
                    <a href="#" :class="[active ? 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-300' : 'text-gray-700 dark:text-gray-200', 'block px-4 py-2 text-sm']">Share</a>
                  </MenuItem>
                </div>
              </MenuItems>
            </transition>
          </Menu>
        </div>
      </li>
    </ul>
  </div>

  <!-- Tickets list (only on smallest breakpoint) -->
  <div class="mt-10 sm:hidden h-full overflow-y-auto">
    <div class="px-4 sm:px-6">
      <h2 class="text-gray-500 text-xs font-medium uppercase tracking-wide">Tickets</h2>
    </div>
    <ul class="mt-3 border-t border-gray-200 divide-y divide-gray-100">
      <li v-for="ticket in tickets" :key="ticket.id">
        <a href="#" class="group flex items-center justify-between px-4 py-4 hover:bg-gray-50 sm:px-6">
          <span class="flex items-center truncate space-x-3">
            <span class="font-medium truncate text-sm leading-6">
              {{ ticket.title }}
            </span>
          </span>
          <ChevronRightIcon class="ml-4 h-5 w-5 text-gray-400 group-hover:text-gray-500" aria-hidden="true" />
        </a>
      </li>
    </ul>
  </div>

  <!-- Tickets table (small breakpoint and up) -->
  <div class="hidden mt-8 sm:block h-full overflow-y-auto">
    <div class="align-middle inline-block min-w-full border-b border-gray-200">
      <table class="min-w-full">
        <thead>
          <tr class="border-t border-gray-200">
            <th class="px-6 py-3 border-b border-gray-200 bg-gray-50 dark:bg-gray-800 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
              <span class="lg:pl-2">Ticket</span>
            </th>
            <th class="px-6 py-3 border-b border-gray-200 bg-gray-50 dark:bg-gray-800 text-center text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
              Status
            </th>
            <th class="px-6 py-3 border-b border-gray-200 bg-gray-50 dark:bg-gray-800 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
              Responses
            </th>
            <th class="hidden md:table-cell px-6 py-3 border-b border-gray-200 bg-gray-50 dark:bg-gray-800 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
              Last updated
            </th>
            <th class="pr-6 py-3 border-b border-gray-200 bg-gray-50 dark:bg-gray-800 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider" />
          </tr>
        </thead>
        <tbody class="bg-white dark:bg-transparent divide-y divide-gray-100">
          <tr v-for="ticket in tickets" :key="ticket.id">
            <td class="px-6 py-3 max-w-0 w-full whitespace-nowrap text-sm font-medium text-gray-900 dark:text-gray-200">
              <div class="flex items-center space-x-3 lg:pl-2">
                <a href="#" class="truncate hover:text-gray-600 dark:hover:text-gray-300">
                  <span>
                    {{ ticket.title }}
                  </span>
                </a>
              </div>
            </td>
            <td class="px-6 py-3 text-sm text-gray-500 font-medium flex justify-center">
              <span v-if="ticket.open" class="inline-flex items-center px-2.5 py-0.5 rounded-md text-sm font-medium bg-green-100 text-green-800">
                Open
              </span>
              <span v-else class="inline-flex items-center px-2.5 py-0.5 rounded-md text-sm font-medium bg-red-100 text-red-800">
                closed
              </span>
            </td>
            <td class="px-6 py-3 text-sm text-gray-500 font-medium">
              <div class="flex items-center space-x-2">
                <div class="flex flex-shrink-0 -space-x-1">
                  <img v-for="member in ticket.responses" :key="member.handle" class="max-w-none h-6 w-6 rounded-full ring-2 ring-white" :src="member.imageUrl" :alt="member.name" />
                </div>
                <span v-if="ticket.totalResponses > ticket.responses.length" class="flex-shrink-0 text-xs leading-5 font-medium">+{{ ticket.totalResponses - ticket.responses.length }}</span>
              </div>
            </td>
            <td class="hidden md:table-cell px-6 py-3 whitespace-nowrap text-sm text-gray-500 text-right">
              {{ ticket.lastUpdated }}
            </td>
            <td class="pr-6">
              <Menu as="div" class="relative flex justify-end items-center">
                <MenuButton class="w-8 h-8 bg-white dark:bg-transparent inline-flex items-center justify-center text-gray-400 dark:text-gray-300 rounded-full hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                  <span class="sr-only">Open options</span>
                  <DotsVerticalIcon class="w-5 h-5" aria-hidden="true" />
                </MenuButton>
                <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
                  <MenuItems class="mx-3 origin-top-right absolute right-7 top-0 w-48 mt-1 rounded-md shadow-lg z-10 bg-white dark:bg-gray-900 dark:border ring-1 ring-black ring-opacity-5 divide-y divide-gray-200 focus:outline-none">
                    <div class="py-1">
                      <MenuItem v-slot="{ active }">
                        <a href="#" :class="[active ? 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-300' : 'text-gray-700 dark:text-gray-200', 'group flex items-center px-4 py-2 text-sm']">
                          <PencilAltIcon class="mr-3 h-5 w-5 text-gray-400 group-hover:text-gray-500" aria-hidden="true" />
                          Edit
                        </a>
                      </MenuItem>
                      <MenuItem v-slot="{ active }">
                        <a href="#" :class="[active ? 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-300' : 'text-gray-700 dark:text-gray-200', 'group flex items-center px-4 py-2 text-sm']">
                          <DuplicateIcon class="mr-3 h-5 w-5 text-gray-400 group-hover:text-gray-500" aria-hidden="true" />
                          Duplicate
                        </a>
                      </MenuItem>
                      <MenuItem v-slot="{ active }">
                        <a href="#" :class="[active ? 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-300' : 'text-gray-700 dark:text-gray-200', 'group flex items-center px-4 py-2 text-sm']">
                          <UserAddIcon class="mr-3 h-5 w-5 text-gray-400 group-hover:text-gray-500" aria-hidden="true" />
                          Share
                        </a>
                      </MenuItem>
                    </div>
                    <div class="py-1">
                      <MenuItem v-slot="{ active }">
                        <a href="#" :class="[active ? 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-300' : 'text-gray-700 dark:text-gray-200', 'group flex items-center px-4 py-2 text-sm']">
                          <TrashIcon class="mr-3 h-5 w-5 text-gray-400 group-hover:text-gray-500" aria-hidden="true" />
                          Delete
                        </a>
                      </MenuItem>
                    </div>
                  </MenuItems>
                </transition>
              </Menu>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

import {
  Menu,
  MenuButton,
  MenuItem,
  MenuItems
} from '@headlessui/vue'
import {
  ChevronRightIcon,
  DotsVerticalIcon,
  DuplicateIcon,
  PencilAltIcon,
  TrashIcon,
  UserAddIcon
} from '@heroicons/vue/solid'

const tickets = [
  {
    id: 1,
    title: 'When is the next SWEBOK panel?',
    responses: [
      {
        name: 'Dries Vincent',
        handle: 'driesvincent',
        imageUrl:
          'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80'
      },
      {
        name: 'Lindsay Walton',
        handle: 'lindsaywalton',
        imageUrl:
          'https://images.unsplash.com/photo-1517841905240-472988babdf9?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80'
      },
      {
        name: 'Courtney Henry',
        handle: 'courtneyhenry',
        imageUrl:
          'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80'
      },
      {
        name: 'Tom Cook',
        handle: 'tomcook',
        imageUrl:
          'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80'
      }
    ],
    totalResponses: 12,
    lastUpdated: 'March 17, 2020',
    pinned: true,
    open: true
  },
  {
    id: 2,
    title: 'Was eJournal founded during this inbox?',
    responses: [
      {
        name: 'Dries Vincent',
        handle: 'driesvincent',
        imageUrl:
          'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80'
      },
      {
        name: 'Lindsay Walton',
        handle: 'lindsaywalton',
        imageUrl:
          'https://images.unsplash.com/photo-1517841905240-472988babdf9?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80'
      },
      {
        name: 'Courtney Henry',
        handle: 'courtneyhenry',
        imageUrl:
          'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80'
      },
      {
        name: 'Tom Cook',
        handle: 'tomcook',
        imageUrl:
          'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80'
      }
    ],
    totalResponses: 8,
    lastUpdated: 'March 18, 2020',
    pinned: false,
    open: false
  }
]
const pinnedTickets = tickets.filter((ticket) => ticket.pinned)

export default {
  name: 'Public',
  components: {
    ChevronRightIcon,
    DotsVerticalIcon,
    DuplicateIcon,
    PencilAltIcon,
    TrashIcon,
    UserAddIcon,
    Menu,
    MenuButton,
    MenuItem,
    MenuItems
  },
  data: () => ({
    userInbox: null,
    side: false
  }),
  async mounted () {
    const response = await axios.get(`/api/me/inboxes/${this.$route.params.inboxId}`)
    this.userInbox = response.data
  },
  setup () {
    return {
      tickets,
      pinnedTickets
    }
  },
  computed: {
    user () {
      return this.$store.state.user
    },
    is_staff () {
      if (!this.userInbox) {
        return false
      }

      const role = this.userInbox.role
      return (this.user && this.user.is_superuser) || (role && (role === 'AGENT' || role === 'MANAGER'))
    },
    development: () => process.env.NODE_ENV !== 'production'
  }
}
</script>
