<template>
  <div v-if="!selected">
    <!-- Labels list (only on smallest breakpoint) -->
    <div class="h-full overflow-y-auto sm:hidden">
      <div>
        <h2 class="text-lg leading-6 font-medium text-gray-900">Labels</h2>
        <p class="mt-1 text-sm text-gray-500">
          These are the labels for this inbox. Feel free to add, edit or remove them. 
        </p>
      </div>
      <ul class="mt-3 divide-y divide-gray-100 border-t border-b border-gray-200">
        <li v-for="label in labels" :key="label.id">
          <router-link :to="`/inboxes/${$route.params.inboxId}/settings/labels/${label.id}`" class="group flex w-full items-center justify-between px-4 py-3 hover:bg-gray-50 sm:px-6">
            <span class="flex items-center space-x-3 truncate">
              <div class="h-2.5 w-2.5 flex-shrink-0 rounded-full" :style="`background-color: ${label.color}`" aria-hidden="true" />
              <span class="truncate text-sm font-medium leading-4">
                {{ label.name }}
              </span>
            </span>
            <ChevronRightIcon class="ml-4 h-5 w-5 text-gray-400 group-hover:text-gray-500" aria-hidden="true" />
          </router-link>
        </li>
      </ul>
    </div>

    <!-- Labels table (small breakpoint and up) -->
    <div class="hidden h-full overflow-y-auto sm:block">
      <div class="inline-block min-w-full border-b border-gray-200 align-middle">
        <table class="min-w-full flex flex-col">
          <div class="border-b pb-2 w-full">
            <h2 class="text-lg leading-6 font-medium text-gray-900">Labels</h2>
            <p class="mt-1 text-sm text-gray-500">
              These are the labels for this inbox. Feel free to add, edit or remove them. 
            </p>
          </div>
          <!-- <thead>
            <tr class="border-t border-gray-200">
              <th class="border-b border-gray-200 bg-gray-50 px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 dark:bg-gray-800 dark:text-gray-300">
                <span class="lg:pl-2">Labels</span>
              </th>
              <th class="border-b border-gray-200 bg-gray-50 px-6 py-3 text-center text-xs font-medium uppercase tracking-wider text-gray-500 dark:bg-gray-800 dark:text-gray-300">Status</th>
              <th class="truncate border-b border-gray-200 bg-gray-50 px-6 py-3 text-center text-xs font-medium uppercase tracking-wider text-gray-500 dark:bg-gray-800 dark:text-gray-300">Visible to students</th>
              <th class="border-b border-gray-200 bg-gray-50 py-3 pr-6 text-right text-xs font-medium uppercase tracking-wider text-gray-500 dark:bg-gray-800 dark:text-gray-300" />
            </tr>
          </thead> -->
          <tbody class="divide-y divide-gray-100 bg-white dark:bg-transparent">
            <tr v-for="label in labels" :key="label.id" class="table-row">
              <td class="w-full max-w-0 whitespace-nowrap py-3 text-sm font-medium text-gray-900 dark:text-gray-200">
                <div class="flex items-center space-x-3 lg:pl-2">
                  <div class="h-2.5 w-2.5 flex-shrink-0 rounded-full" :style="`background-color: ${label.color}`" aria-hidden="true" />
                  <router-link :to="`/inboxes/${$route.params.inboxId}/settings/labels/${label.id}`" class="truncate hover:text-gray-600 dark:hover:text-gray-300">
                    <span>
                      {{ label.name }}
                    </span>
                  </router-link>
                </div>
              </td>
              <td class="px-6 py-3 text-center text-sm font-medium text-gray-500">
                <span v-if="label.is_active" class="inline-flex items-center rounded-md bg-green-100 px-2.5 py-0.5 text-sm font-medium text-green-800"> Active </span>
                <span v-else class="inline-flex items-center truncate rounded-md bg-red-100 px-2.5 py-0.5 text-sm font-medium text-red-800"> In-active </span>
              </td>
              <td class="px-6 flex justify-center py-3 text-sm font-medium text-gray-500">
                <span v-if="label.is_visible_to_guest" class="inline-flex items-center rounded-md bg-green-100 px-2.5 py-0.5 text-sm font-medium text-green-800"> Visible </span>
                <span v-else class="inline-flex items-center rounded-md bg-red-100 px-2.5 py-0.5 text-sm font-medium text-red-800"> Invisible </span>
              </td>
              <td v-if="is_staff" class="pr-6">
                <Menu as="div" class="relative flex items-center justify-end">
                  <MenuButton class="inline-flex h-8 w-8 items-center justify-center rounded-full bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 dark:bg-transparent dark:text-gray-300">
                    <span class="sr-only">Open options</span>
                    <EllipsisVerticalIcon class="h-5 w-5 text-gray-400 group-hover:text-gray-500" aria-hidden="true" />
                  </MenuButton>
                  <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
                    <MenuItems class="absolute right-7 top-0 z-10 mx-3 mt-1 w-48 origin-top-right divide-y divide-gray-200 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none dark:border dark:bg-gray-900">
                      <div class="py-1">
                        <MenuItem v-slot="{ active }">
                          <router-link :to="`/inboxes/${$route.params.inboxId}/settings/labels/${label.id}`" :class="[active ? 'bg-gray-100 text-gray-900 dark:bg-gray-700 dark:text-gray-300' : 'text-gray-700 dark:text-gray-200', 'group flex items-center px-4 py-2 text-sm']">
                            <ArrowTopRightOnSquareIcon class="mr-3 h-5 w-5 text-gray-400 group-hover:text-gray-500" aria-hidden="true" />
                            Edit label
                          </router-link>
                        </MenuItem>
                      </div>
                      <div class="py-1">
                        <MenuItem v-slot="{ active }">
                          <button @click="deleteLabel(label.id)" :class="[active ? 'bg-gray-100 text-gray-900 dark:bg-gray-700 dark:text-gray-300' : 'text-gray-700 dark:text-gray-200', 'group flex w-full items-center px-4 py-2 text-sm']">
                            <TrashIcon class="mr-3 h-5 w-5 text-red-400 group-hover:text-red-500" aria-hidden="true" />
                            Delete label
                          </button>
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

    <div class="flex w-full justify-end py-4">
      <router-link :to="`/inboxes/${$route.params.inboxId}/settings/labels/new`" as="button">
        <button class="rounded-md bg-primary px-4 py-2 text-white shadow-sm hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2">
          <span class="inline-flex items-center">
            <span class="text-base font-medium"> Create new label </span>
          </span>
        </button>
      </router-link>
    </div>
  </div>

  <div v-else>
    <SettingsLabel />
  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'

import SettingsLabel from '@/components/settings/SettingsLabel.vue'

import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { ChevronRightIcon, EllipsisVerticalIcon, ArrowTopRightOnSquareIcon } from '@heroicons/vue/24/solid'
import { TrashIcon } from '@heroicons/vue/24/outline'

export default {
  name: 'Labels',
  components: {
    ChevronRightIcon,
    EllipsisVerticalIcon,
    ArrowTopRightOnSquareIcon,
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    TrashIcon,
    SettingsLabel
  },
  data: () => ({
    is_staff: false,
    labels: [],
    selected: null
  }),
  created() {
    if (this.$route.params.itemId) {
      this.selected = this.$route.params.itemId
    }
  },
  mounted() {
    const { inboxId } = this.$route.params

    axios.get(`/api/inboxes/${inboxId}/role`).then((response) => {
      this.is_staff = response.data.key === 'AGENT' || response.data.key === 'MANAGER'
    })

    axios.get(`/api/inboxes/${inboxId}/labels`).then(async (response) => {
      this.labels = response.data.results
    })
  },
  methods: {
    deleteLabel(label) {
      const { inboxId } = this.$route.params

      if (confirm('Are you sure you want to delete this label?')) {
        axios.delete(`/api/inboxes/${inboxId}/labels/${label}`).then(() => {
          this.labels = this.labels.filter((l) => l.id !== label)
        })
      }
    }
  },
  computed: {
    ...mapState({
      user: (state) => state.user
    })
  }
}
</script>
