<template>
  <!-- Labels list (only on smallest breakpoint) -->
  <div class="mt-3 sm:hidden h-full overflow-y-auto">
    <div class="px-4 sm:px-6">
      <h2 class="text-gray-500 text-xs font-medium uppercase tracking-wide">
        Labels
      </h2>
    </div>
    <ul class="mt-3 border-t border-gray-200 divide-y divide-gray-100 border-b">
      <li v-for="label in labels" :key="label.id">
        <router-link
          :to="`/inboxes/${$route.params.inboxId}/labels/${label.id}`"
          class="group flex items-center justify-between px-4 py-3 hover:bg-gray-50 sm:px-6"
        >
          <span class="flex items-center truncate space-x-3">
            <div
              class="flex-shrink-0 w-2.5 h-2.5 rounded-full"
              :style="`background-color: ${label.color}`"
              aria-hidden="true"
            />
            <span class="font-medium truncate text-sm leading-4">
              {{ label.name }}
            </span>
          </span>
          <ChevronRightIcon
            class="ml-4 h-5 w-5 text-gray-400 group-hover:text-gray-500"
            aria-hidden="true"
          />
        </router-link>
      </li>
    </ul>

    <div class="w-full flex justify-end p-4">
      <router-link
        :to="`/inboxes/${$route.params.inboxId}/labels/new`"
        as="button"
      >
        <button
          class="bg-primary hover:bg-primary-600 text-white px-4 py-2 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
        >
          <span class="inline-flex items-center">
            <span class="text-base font-medium"> Create new label </span>
          </span>
        </button>
      </router-link>
    </div>
  </div>

  <!-- Labels table (small breakpoint and up) -->
  <div class="hidden sm:block h-full overflow-y-auto">
    <div class="align-middle inline-block min-w-full border-b border-gray-200">
      <table class="min-w-full">
        <thead>
          <tr class="border-t border-gray-200">
            <th
              class="px-6 py-3 border-b border-gray-200 bg-gray-50 dark:bg-gray-800 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
            >
              <span class="lg:pl-2">Labels</span>
            </th>
            <th
              class="px-6 py-3 border-b border-gray-200 bg-gray-50 dark:bg-gray-800 text-center text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
            >
              Status
            </th>
            <th
              class="px-6 py-3 border-b border-gray-200 bg-gray-50 dark:bg-gray-800 text-center text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider truncate"
            >
              Visible to students
            </th>
            <th
              class="pr-6 py-3 border-b border-gray-200 bg-gray-50 dark:bg-gray-800 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
            />
          </tr>
        </thead>
        <tbody class="bg-white dark:bg-transparent divide-y divide-gray-100">
          <tr v-for="label in labels" :key="label.id" class="table-row">
            <td
              class="px-6 py-3 max-w-0 w-full whitespace-nowrap text-sm font-medium text-gray-900 dark:text-gray-200"
            >
              <div class="flex items-center space-x-3 lg:pl-2">
                <div
                  class="flex-shrink-0 w-2.5 h-2.5 rounded-full"
                  :style="`background-color: ${label.color}`"
                  aria-hidden="true"
                />
                <router-link
                  :to="`/inboxes/${$route.params.inboxId}/labels/${label.id}`"
                  class="truncate hover:text-gray-600 dark:hover:text-gray-300"
                >
                  <span>
                    {{ label.name }}
                  </span>
                </router-link>
              </div>
            </td>
            <td class="px-6 py-3 text-sm text-gray-500 font-medium text-center">
              <span
                v-if="label.is_active"
                class="inline-flex items-center px-2.5 py-0.5 rounded-md text-sm font-medium bg-green-100 text-green-800"
              >
                Active
              </span>
              <span
                v-else
                class="inline-flex items-center px-2.5 py-0.5 rounded-md text-sm font-medium bg-red-100 text-red-800 truncate"
              >
                In-active
              </span>
            </td>
            <td
              class="px-6 py-3 text-sm text-gray-500 font-medium flex justify-center"
            >
              <span
                v-if="label.is_visible_to_guest"
                class="inline-flex items-center px-2.5 py-0.5 rounded-md text-sm font-medium bg-green-100 text-green-800"
              >
                Visible
              </span>
              <span
                v-else
                class="inline-flex items-center px-2.5 py-0.5 rounded-md text-sm font-medium bg-red-100 text-red-800"
              >
                Invisible
              </span>
            </td>
            <td v-if="is_staff" class="pr-6">
              <Menu as="div" class="relative flex justify-end items-center">
                <MenuButton
                  class="w-8 h-8 bg-white dark:bg-transparent inline-flex items-center justify-center text-gray-400 dark:text-gray-300 rounded-full hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
                >
                  <span class="sr-only">Open options</span>
                  <EllipsisVerticalIcon
                    class="h-5 w-5 text-gray-400 group-hover:text-gray-500"
                    aria-hidden="true"
                  />
                </MenuButton>
                <transition
                  enter-active-class="transition ease-out duration-100"
                  enter-from-class="transform opacity-0 scale-95"
                  enter-to-class="transform opacity-100 scale-100"
                  leave-active-class="transition ease-in duration-75"
                  leave-from-class="transform opacity-100 scale-100"
                  leave-to-class="transform opacity-0 scale-95"
                >
                  <MenuItems
                    class="mx-3 origin-top-right absolute right-7 top-0 w-48 mt-1 rounded-md shadow-lg z-10 bg-white dark:bg-gray-900 dark:border ring-1 ring-black ring-opacity-5 divide-y divide-gray-200 focus:outline-none"
                  >
                    <div class="py-1">
                      <MenuItem v-slot="{ active }">
                        <router-link
                          :to="`/inboxes/${$route.params.inboxId}/labels/${label.id}`"
                          :class="[
                            active
                              ? 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-300'
                              : 'text-gray-700 dark:text-gray-200',
                            'group flex items-center px-4 py-2 text-sm',
                          ]"
                        >
                          <ArrowTopRightOnSquareIcon
                            class="mr-3 h-5 w-5 text-gray-400 group-hover:text-gray-500"
                            aria-hidden="true"
                          />
                          Edit label
                        </router-link>
                      </MenuItem>
                    </div>
                    <div class="py-1">
                      <MenuItem v-slot="{ active }">
                        <button
                          @click="deleteLabel(label.id)"
                          :class="[
                            active
                              ? 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-300'
                              : 'text-gray-700 dark:text-gray-200',
                            'group flex items-center px-4 py-2 text-sm w-full',
                          ]"
                        >
                          <TrashIcon
                            class="mr-3 h-5 w-5 text-red-400 group-hover:text-red-500"
                            aria-hidden="true"
                          />
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

    <div class="w-full flex justify-end p-4">
      <router-link
        :to="`/inboxes/${$route.params.inboxId}/labels/new`"
        as="button"
      >
        <button
          class="bg-primary hover:bg-primary-600 text-white px-4 py-2 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
        >
          <span class="inline-flex items-center">
            <span class="text-base font-medium"> Create new label </span>
          </span>
        </button>
      </router-link>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapState } from "vuex";

import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
import {
  ChevronRightIcon,
  EllipsisVerticalIcon,
  ArrowTopRightOnSquareIcon,
} from "@heroicons/vue/24/solid";
import { TrashIcon } from "@heroicons/vue/24/outline";

export default {
  name: "Labels",
  components: {
    ChevronRightIcon,
    EllipsisVerticalIcon,
    ArrowTopRightOnSquareIcon,
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    TrashIcon,
  },
  data: () => ({
    is_staff: false,
    labels: [],
  }),
  mounted() {
    const { inboxId } = this.$route.params;

    axios.get(`/api/inboxes/${inboxId}/role`).then((response) => {
      this.is_staff =
        response.data.key === "AGENT" || response.data.key === "MANAGER";
    });

    axios.get(`/api/inboxes/${inboxId}/labels`).then(async (response) => {
      this.labels = response.data.results;
    });
  },
  methods: {
    deleteLabel(label) {
      const { inboxId } = this.$route.params;

      if (confirm("Are you sure you want to delete this label?")) {
        axios.delete(`/api/inboxes/${inboxId}/labels/${label}`).then(() => {
          this.labels = this.labels.filter((l) => l.id !== label);
        });
      }
    },
  },
  computed: {
    ...mapState({
      user: (state) => state.user,
    }),
  },
};
</script>
