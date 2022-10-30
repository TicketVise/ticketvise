<template>
  <!-- Pinned tickets -->
  <div v-if="pinnedTickets?.length > 0" class="px-4 mt-6 sm:px-6 lg:px-8">
    <h2
      class="text-gray-500 dark:text-gray-300 text-xs font-medium uppercase tracking-wide"
    >
      Pinned Tickets
    </h2>
    <ul
      class="grid grid-cols-1 gap-4 sm:gap-6 sm:grid-cols-2 xl:grid-cols-4 mt-3"
    >
      <li
        v-for="ticket in pinnedTickets"
        :key="ticket.id"
        class="relative col-span-1 flex shadow-sm rounded-md"
      >
        <div
          class="flex-1 flex items-center justify-between border border-gray-200 bg-white dark:bg-transparent rounded-md truncate"
        >
          <div class="flex-1 px-4 py-2 text-sm truncate">
            <router-link
              :to="`/inboxes/${$route.params.inboxId}/tickets/${ticket.ticket_inbox_id}`"
              class="text-gray-900 dark:text-gray-200 font-medium hover:text-gray-600 dark:hover:text-gray-400"
            >
              {{ ticket.title }}
            </router-link>
            <p class="text-gray-500">{{ ticket.totalResponses }} Responses</p>
          </div>
          <Menu v-if="is_staff" as="div" class="flex-shrink-0 pr-2">
            <MenuButton
              class="w-8 h-8 bg-white dark:bg-transparent inline-flex items-center justify-center text-gray-400 dark:text-gray-300 rounded-full hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
            >
              <span class="sr-only">Open options</span>
              <EllipsisVerticalIcon class="w-5 h-5" aria-hidden="true" />
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
                class="z-10 mx-3 origin-top-right absolute right-10 top-3 w-48 mt-1 rounded-md shadow-lg bg-white dark:bg-gray-900 dark:border ring-1 ring-black ring-opacity-5 divide-y divide-gray-200 focus:outline-none"
              >
                <div class="py-1">
                  <MenuItem v-slot="{ active }">
                    <button
                      @click="swapPinTicket(ticket.ticket_inbox_id)"
                      :class="[
                        active
                          ? 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-300'
                          : 'text-gray-700 dark:text-gray-200',
                        'group flex w-full items-center px-4 py-2 text-sm',
                      ]"
                    >
                      <PinnedIcon
                        v-if="ticket.is_pinned"
                        class="mr-3 h-5 w-5 text-gray-400 group-hover:text-gray-500"
                        aria-hidden="true"
                      />
                      <NotPinnedIcon
                        v-else
                        class="mr-3 h-5 w-5 text-gray-400 group-hover:text-gray-500"
                        aria-hidden="true"
                      />
                      {{ ticket.is_pinned ? "Unpin" : "Pin" }} ticket
                    </button>
                  </MenuItem>
                </div>
                <div class="py-1">
                  <MenuItem v-slot="{ active }">
                    <router-link
                      :to="`/inboxes/${$route.params.inboxId}/tickets/${ticket.ticket_inbox_id}`"
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
                      View ticket
                    </router-link>
                  </MenuItem>
                </div>
              </MenuItems>
            </transition>
          </Menu>
        </div>
      </li>
    </ul>
  </div>

  <div class="p-4 flex flex-col md:flex-row items-start md:items-center space-y-2 md:space-y-0 md:space-x-2">
    <button
      class="inline-flex items-center rounded-full bg-gray-100 py-1 px-3 text-sm font-medium text-gray-700"
    >
      FILTERS
      <span
        class="ml-2 inline-flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-full text-gray-600"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="w-5 h-5"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M6 13.5V3.75m0 9.75a1.5 1.5 0 010 3m0-3a1.5 1.5 0 000 3m0 3.75V16.5m12-3V3.75m0 9.75a1.5 1.5 0 010 3m0-3a1.5 1.5 0 000 3m0 3.75V16.5m-6-9V3.75m0 3.75a1.5 1.5 0 010 3m0-3a1.5 1.5 0 000 3m0 9.75V10.5"
          />
        </svg>
      </span>
    </button>

    <div class="flex flex-1 overflow-x-auto space-x-2">
      <span
        class="flex w-max items-center rounded-full bg-white border py-1 pl-3 pr-1.5 text-xs font-medium text-gray-700"
      >
        YOUR TICKETS
        <button
          type="button"
          class="ml-1 inline-flex h-4 w-4 flex-shrink-0 items-center justify-center rounded-full text-gray-600 hover:bg-gray-200 hover:text-gray-500 focus:bg-gray-500 focus:text-white focus:outline-none"
        >
          <span class="sr-only">Remove large option</span>
          <svg
            class="h-2 w-2"
            stroke="currentColor"
            fill="none"
            viewBox="0 0 8 8"
          >
            <path
              stroke-linecap="round"
              stroke-width="1.5"
              d="M1 1l6 6m0-6L1 7"
            />
          </svg>
        </button>
      </span>
      <span
        class="flex w-max items-center rounded-full bg-white border py-1 pl-3 pr-1.5 text-xs font-medium text-gray-700"
      >
        PRIVATE
        <button
          type="button"
          class="ml-1 inline-flex h-4 w-4 flex-shrink-0 items-center justify-center rounded-full text-gray-600 hover:bg-gray-200 hover:text-gray-500 focus:bg-gray-500 focus:text-white focus:outline-none"
        >
          <span class="sr-only">Remove large option</span>
          <svg
            class="h-2 w-2"
            stroke="currentColor"
            fill="none"
            viewBox="0 0 8 8"
          >
            <path
              stroke-linecap="round"
              stroke-width="1.5"
              d="M1 1l6 6m0-6L1 7"
            />
          </svg>
        </button>
      </span>
      <span
        class="flex w-max items-center rounded-full bg-white border py-1 pl-3 pr-1.5 text-xs font-medium text-gray-700"
      >
        TODAY
        <button
          type="button"
          class="ml-1 inline-flex h-4 w-4 flex-shrink-0 items-center justify-center rounded-full text-gray-600 hover:bg-gray-200 hover:text-gray-500 focus:bg-gray-500 focus:text-white focus:outline-none"
        >
          <span class="sr-only">Remove large option</span>
          <svg
            class="h-2 w-2"
            stroke="currentColor"
            fill="none"
            viewBox="0 0 8 8"
          >
            <path
              stroke-linecap="round"
              stroke-width="1.5"
              d="M1 1l6 6m0-6L1 7"
            />
          </svg>
        </button>
      </span>
    </div>
  </div>

  <!-- Tickets list (only on smallest breakpoint) -->
  <div class="mt-3 sm:hidden h-full overflow-y-auto">
    <div class="px-4 sm:px-6">
      <h2 class="text-gray-500 text-xs font-medium uppercase tracking-wide">
        Tickets
      </h2>
    </div>
    <ul class="mt-3 border-t border-gray-200 divide-y divide-gray-100">
      <li v-for="ticket in ticketsFlattened" :key="ticket.id">
        <router-link
          :to="`/inboxes/${$route.params.inboxId}/tickets/${ticket.ticket_inbox_id}`"
          class="group flex items-center justify-between px-4 py-3 hover:bg-gray-50 sm:px-6"
        >
          <span class="flex items-center truncate space-x-3">
            <span class="font-medium truncate text-sm leading-4">
              {{ ticket.title }}
            </span>
          </span>
          <ChevronRightIcon
            class="ml-4 h-5 w-5 text-gray-400 group-hover:text-gray-500"
            aria-hidden="true"
          />
        </router-link>
      </li>
    </ul>
  </div>

  <!-- Tickets table (small breakpoint and up) -->
  <div class="hidden sm:block h-full overflow-y-auto">
    <div class="align-middle inline-block min-w-full border-b border-gray-200">
      <table class="min-w-full">
        <thead>
          <tr class="border-t border-gray-200">
            <th
              class="px-6 py-3 border-b border-gray-200 bg-gray-50 dark:bg-gray-800 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
            >
              <span class="lg:pl-2">Tickets</span>
            </th>
            <th
              class="px-6 py-3 border-b border-gray-200 bg-gray-50 dark:bg-gray-800 text-center text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
            >
              Status
            </th>
            <th
              class="hidden md:table-cell px-6 py-3 border-b border-gray-200 bg-gray-50 dark:bg-gray-800 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider truncate"
            >
              Last updated
            </th>
            <th
              v-if="is_staff"
              class="pr-6 py-3 border-b border-gray-200 bg-gray-50 dark:bg-gray-800 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
            />
          </tr>
        </thead>
        <tbody class="bg-white dark:bg-transparent divide-y divide-gray-100">
          <tr v-for="ticket in ticketsFlattened" :key="ticket.id">
            <td
              class="px-6 py-3 max-w-0 w-full whitespace-nowrap text-sm font-medium text-gray-900 dark:text-gray-200"
            >
              <div class="flex items-center space-x-3 lg:pl-2">
                <router-link
                  :to="`/inboxes/${$route.params.inboxId}/tickets/${ticket.ticket_inbox_id}`"
                  class="truncate hover:text-gray-600 dark:hover:text-gray-300"
                >
                  <span>
                    {{ ticket.title }}
                  </span>
                </router-link>
              </div>
            </td>
            <td
              class="px-6 py-3 text-sm text-gray-500 font-medium flex justify-center"
            >
              <span
                v-if="ticket.open"
                class="inline-flex items-center px-2.5 py-0.5 rounded-md text-sm font-medium bg-green-100 text-green-800"
              >
                Open
              </span>
              <span
                v-else
                class="inline-flex items-center px-2.5 py-0.5 rounded-md text-sm font-medium bg-red-100 text-red-800"
              >
                Closed
              </span>
            </td>
            <td
              class="hidden md:table-cell px-6 py-3 whitespace-nowrap text-sm text-gray-500 text-right"
            >
              {{ date(ticket.date_latest_update) }}
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
                        <button
                          @click="swapPinTicket(ticket.ticket_inbox_id)"
                          :class="[
                            active
                              ? 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-gray-300'
                              : 'text-gray-700 dark:text-gray-200',
                            'group flex w-full items-center px-4 py-2 text-sm',
                          ]"
                        >
                          <PinnedIcon
                            v-if="ticket.is_pinned"
                            class="mr-3 h-5 w-5 text-gray-400 group-hover:text-gray-500"
                            aria-hidden="true"
                          />
                          <NotPinnedIcon
                            v-else
                            class="mr-3 h-5 w-5 text-gray-400 group-hover:text-gray-500"
                            aria-hidden="true"
                          />
                          {{ ticket.is_pinned ? "Unpin" : "Pin" }} ticket
                        </button>
                      </MenuItem>
                    </div>
                    <div class="py-1">
                      <MenuItem v-slot="{ active }">
                        <router-link
                          :to="`/inboxes/${$route.params.inboxId}/tickets/${ticket.ticket_inbox_id}`"
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
                          View ticket
                        </router-link>
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
import axios from "axios";
import store from "@/store";
import { mapState } from "vuex";
import moment from "moment";

import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
import {
  ChevronRightIcon,
  EllipsisVerticalIcon,
  ArrowTopRightOnSquareIcon,
  MapPinIcon as PinnedIcon,
} from "@heroicons/vue/24/solid";
import { MapPinIcon as NotPinnedIcon } from "@heroicons/vue/24/outline";

export default {
  name: "Public",
  components: {
    ChevronRightIcon,
    EllipsisVerticalIcon,
    ArrowTopRightOnSquareIcon,
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    PinnedIcon,
    NotPinnedIcon,
  },
  data: () => ({
    is_staff: false,
  }),
  created() {
    axios
      .get(`/api/inboxes/${this.$route.params.inboxId}/role`)
      .then((response) => {
        this.is_staff =
          response.data.key === "AGENT" || response.data.key === "MANAGER";
      });

    this.getTickets();
  },
  methods: {
    getTickets() {
      const { inboxId } = this.$route.params;

      axios
        .get(`/api/inboxes/${inboxId}/tickets`, {
          params: {
            public: true,
          },
        })
        .then(async (response) => {
          if (!store.getters.inbox(inboxId))
            await store.dispatch("update_inboxes");

          store.commit("update_public_tickets", {
            inbox: inboxId,
            public_tickets: response.data,
          });
        });
    },
    swapPinTicket(ticketId) {
      const { inboxId } = this.$route.params;
      axios.put(`/api/inboxes/${inboxId}/tickets/${ticketId}/pin`);

      this.getTickets();
    },
    date(date) {
      return moment.parseZone(date).calendar(null, {
        lastDay: "[Yesterday at] HH:mm",
        sameDay: "[Today at] HH:mm",
        nextDay: "[Tomorrow at] HH:mm",
        lastWeek: "[Last] dddd [at] HH:mm",
        nextWeek: "dddd [at] HH:mm",
        sameElse: "L [at] HH:mm",
      });
    },
  },
  computed: {
    ticketsFlattened() {
      return this.tickets
        ?.flatMap((c) => {
          for (let i = 0; i < c.tickets.length; i++)
            c.tickets[i].open = c.label !== "Closed";

          return c.tickets;
        })
        .sort((a, b) => a.date_latest_update < b.date_latest_update);
    },
    pinnedTickets() {
      return this.ticketsFlattened?.filter((ticket) => ticket.is_pinned);
    },
    ...mapState({
      user: (state) => state.user,
      tickets() {
        return store.getters.inbox(this.$route.params.inboxId)?.public_tickets;
      },
    }),
  },
};
</script>
