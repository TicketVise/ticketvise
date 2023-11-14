<template>
  <!-- Column based layout for teachers and assistants -->
  <section
    v-if="is_staff"
    class="flex flex-col h-full flex-grow justify-start dark:bg-gray-800"
  >
    <div class="flex flex-col md:grid md:grid-cols-5 md:gap-2 p-4 space-y-2 md:space-y-0">
      <div class="flex space-x-2 md:col-span-2 xl:col-span-3 items-center">
        <SearchBar v-model="search" v-on:input="callDebounceGetTickets" />
      </div>

      <div class="flex space-x-2 md:col-span-3 xl:col-span-2 items-center">
        <div class="flex-grow">
          <label-dropdown :selected="labels" :values="inbox_labels" v-model="labels" v-on:input="updateLabels" />
        </div>

        <button
          :class="showPersonal ? `bg-primary-500 text-white px-4 py-2 border border-gray-300 text-sm leading-5 font-medium rounded-md focus:outline-none transition duration-150 ease-in-out` : `bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-300 px-4 py-2 border border-gray-300 text-sm leading-5 font-medium rounded-md focus:outline-none transition duration-150 ease-in-out` "
          @click="togglePersonal"
          class="px-4 md:m-0 h-10"
          v-if="is_staff"
        >
          My Tickets
        </button>
      </div>
    </div>
    <!-- <div class="flex justify-between w-full items-center">
      <div class="p-4 flex flex-col items-start space-y-2 w-full">
        <div class="flex justify-between items-center w-full">
          <Popover class="relative">
            <PopoverButton class="inline-flex items-center rounded-full bg-gray-100 py-1 px-3 text-sm font-medium text-gray-700">
              <span>FILTERS</span>
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
            </PopoverButton>

            <PopoverPanel class="absolute z-10 bg-white shadow-lg p-4 rounded-md">
              <h3 class="font-medium text-gray-600">Filters</h3>

              <div class="flex flex-col w-max text-gray-800">
                <div class="py-1 flex space-x-2 items-center">
                  <UserIcon class="h-4 w-4" />
                  <span class="">Your tickets</span>
                </div>
                <hr />
                <div class="py-1 flex space-x-2 items-center">
                  <UserIcon class="h-4 w-4" />
                  <span class="">Public</span>
                </div>
                <div class="py-1 flex space-x-2 items-center">
                  <UserIcon class="h-4 w-4" />
                  <span class="">Private</span>
                </div>
                <hr />
                <div class="py-1 flex space-x-2 items-center">
                  <UserIcon class="h-4 w-4" />
                  <span class="">Today</span>
                </div>
              </div>
            </PopoverPanel>
          </Popover>

          <div class="flex md:hidden items-center rounded-lg bg-gray-100 p-0.5">
            <button type="button" class="rounded-md p-1.5 text-gray-400 hover:bg-white hover:shadow-sm focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500">
              <Bars4Icon class="h-5 w-5" aria-hidden="true" />
              <span class="sr-only">Use list view</span>
            </button>
            <button type="button" class="ml-0.5 rounded-md bg-white p-1.5 text-gray-400 shadow-sm focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500">
              <ViewColumnsIcon class="h-5 w-5" aria-hidden="true" />
              <span class="sr-only">Use grid view</span>
            </button>
          </div>
        </div>
  
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

      <div class="mr-4 hidden md:flex items-center rounded-lg bg-gray-100 p-0.5">
        <button type="button" class="rounded-md p-1.5 text-gray-400 hover:bg-white hover:shadow-sm focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500">
          <Bars4Icon class="h-5 w-5" aria-hidden="true" />
          <span class="sr-only">Use list view</span>
        </button>
        <button type="button" class="ml-0.5 rounded-md bg-white p-1.5 text-gray-400 shadow-sm focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500">
          <ViewColumnsIcon class="h-5 w-5" aria-hidden="true" />
          <span class="sr-only">Use grid view</span>
        </button>
      </div>
    </div> -->

    <div v-if="onboarding.active" class="mx-4 border border-primary rounded-lg flex px-4 py-3 max-w-lg">
      <div class="flex flex-col text-gray-800">
        <h2 class="font-bold text-primary text-xl">The tickets</h2>
        <p class="text-sm mt-1 text-justify">This is the <strong>tickets page</strong>. Here you will find every ticket in the inbox. They are organized by their status.</p>
        <div class="flex justify-end text-sm mt-2">
          <button @click="nextStep()">
            <span class="text-primary uppercase font-medium">Got it!</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Columns -->
    <div
      class="ticket-columns max-w-full flex flex-grow overflow-x-auto pl-4 b-4"
    >
      <ticket-column
        v-for="(column, i) in tickets"
        :key="i"
        :color="colors[column.label]"
        :title="column.label"
        :ticket-list="column.tickets"
        :has_next="column.has_next"
        :length="column.total"
        @input="loadStatus(column.label)"
        class="min-w-3/4 sm:min-w-1/2 md:min-w-0 pr-4"
        v-on:refresh="get_tickets"
      />
    </div>

    <!-- Floating action button for new ticket -->
    <!-- <router-link
      :to="'/inboxes/' + $route.params.inboxId + '/tickets/new'"
      exact
      type="button"
      class="md:hidden fixed right-4 bottom-4 inline-flex items-center px-3.5 py-2 border border-transparent text-sm leading-4 font-medium rounded-full shadow text-white bg-primary hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 z-10"
    >
      <svg
        class="-ml-0.5 mr-2 h-6 w-6"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M12 6v6m0 0v6m0-6h6m-6 0H6"
        ></path>
      </svg>
      New Ticket
    </router-link> -->
  </section>

  <!-- Private questions for students -->
  <section
    v-else
    class="flex flex-col h-full flex-grow justify-start dark:bg-gray-800"
  >
    <div class="p-4">
      <h2 class="text-lg leading-6 font-medium text-gray-900">Your tickets</h2>
      <p class="mt-1 text-sm text-gray-500">These are your personal tickets.</p>
    </div>

    <!-- Tickets list (only on smallest breakpoint) -->
    <div class="mt-2 sm:hidden h-full overflow-y-auto">
      <div class="px-4 sm:px-6">
        <h2 class="text-gray-500 text-xs font-medium uppercase tracking-wide">
          Tickets
        </h2>
      </div>
      <ul class="mt-3 border-t border-gray-200 divide-y divide-gray-100">
        <li v-for="ticket in ticketsFlattened" :key="ticket.id">
          <router-link
            :to="`/inboxes/${$route.params.inboxId}/tickets/${ticket.ticket_inbox_id}`"
            class="group flex items-center justify-between py-3 px-4 hover:bg-gray-50 sm:px-6"
          >
            <span class="flex items-center truncate space-x-2">
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
      <div
        class="align-middle inline-block min-w-full border-b border-gray-200"
      >
        <table class="min-w-full">
          <thead>
            <tr class="border-t border-gray-200">
              <th
                class="px-3 py-3 border-b border-gray-200 bg-gray-50 dark:bg-gray-800 text-center text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
              ></th>
              <th
                class="pl-3 pr-6 py-3 border-b border-gray-200 bg-gray-50 dark:bg-gray-800 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
              >
                <span class="lg:pl-2">Tickets</span>
              </th>
              <th
                class="px-6 py-3 border-b border-gray-200 bg-gray-50 dark:bg-gray-800 text-center text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
              >
                Status
              </th>
              <!-- truncate is a dirty trick here to make sure the words 'last updated' are on the same row -->
              <th
                class="hidden md:table-cell truncate px-6 py-3 border-b border-gray-200 bg-gray-50 dark:bg-gray-800 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
              >
                Last updated
              </th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-transparent divide-y divide-gray-100">
            <tr v-for="ticket in ticketsFlattened" :key="ticket.id">
              <td
                class="px-3 py-3 max-w-0 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-gray-200"
              >
                <GlobeEuropeAfricaIcon
                  v-if="ticket.is_public"
                  class="h-5 w-5 text-gray-700"
                />
              </td>
              <td
                class="pl-3 pr-6 py-3 max-w-0 w-full whitespace-nowrap text-sm font-medium text-gray-900 dark:text-gray-200"
              >
                <div class="flex items-center space-x-3 lg:pl-2">
                  <router-link
                    :to="`/inboxes/${$route.params.inboxId}/tickets/${ticket.ticket_inbox_id}`"
                    class="truncate hover:text-gray-600 dark:hover:text-gray-300"
                  >
                    <span>{{ ticket.title }}</span>
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
                  closed
                </span>
              </td>
              <td
                class="hidden md:table-cell px-6 py-3 whitespace-nowrap text-sm text-gray-500 text-right"
              >
                {{ ticket.lastUpdated || moment().calendar() }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "axios";
import store from "@/store";
import { mapState, mapActions } from "vuex";
import _ from "lodash";
import moment from "moment";

import SearchBar from "@/components/searchbar/SearchBar.vue";
import TicketColumn from "@/components/tickets/TicketColumn.vue";
import LabelDropdown from "@/components/dropdown/LabelDropdown.vue";

import { ChevronRightIcon, UserIcon } from "@heroicons/vue/24/solid";
import { GlobeEuropeAfricaIcon, Bars4Icon, ViewColumnsIcon } from "@heroicons/vue/24/outline";
import { Popover, PopoverButton, PopoverPanel } from "@headlessui/vue";

const UNLABELLED_LABEL = {
  id: 0,
  name: "Unlabelled",
  color: "#2D3748",
};

export default {
  name: "Inbox",
  components: {
    Bars4Icon,
    ChevronRightIcon,
    GlobeEuropeAfricaIcon,
    TicketColumn,
    LabelDropdown,
    SearchBar,
    ViewColumnsIcon,
    Popover,
    PopoverButton,
    PopoverPanel,
    UserIcon
  },
  data: () => ({
    colors: {
      Pending: "#e76f51",
      Assigned: "#e9c46a",
      "Awaiting response": "#2a9d8f",
      Closed: "#264653",
    },
    search: null,
    showPersonal: false,
    labels: [],
    inbox_labels: [],
    is_staff: false,
  }),
  setup() {
    return { moment };
  },
  methods: {
    ...mapActions('onboarding', {
      nextStep: 'next',
      prevStep: 'prev'
    }),
    get_tickets() {
      // Call this function by using callDebounceGetTickets
      const labelsIds = [];
      this.labels.forEach((label) => labelsIds.push(label.id));
      const { inboxId } = this.$route.params;

      axios
        .get(`/api/inboxes/${inboxId}/tickets`, {
          params: {
            q: this.search,
            show_personal: this.showPersonal,
            labels: labelsIds,
          },
        })
        .then(async (response) => {
          if (!store.getters.inbox(inboxId))
            await store.dispatch("update_inboxes");

          store.commit("update_tickets", {
            inbox: inboxId,
            tickets: response.data,
          });
        });
    },
    callDebounceGetTickets: _.debounce(function () {
      this.get_tickets();
    }, 300),
    deleteEvent(index) {
      this.labels.splice(index, 1);

      this.get_tickets();
    },
    updateLabels(items) {
      this.labels = items;

      this.get_tickets();
    },
    togglePersonal() {
      this.showPersonal = !this.showPersonal;
      this.get_tickets();
    },
    loadStatus(status) {
      const labelsIds = [];
      this.labels.forEach((label) => labelsIds.push(label.id));
      let index = 0;

      if (status === "Pending") {
        index = 0;
      } else if (status === "Assigned") {
        index = 1;
      } else if (status === "Awaiting response") {
        index = 2;
      } else if (status === "Closed") {
        index = 3;
      }

      axios
        .get(`/api/inboxes/${this.$route.params.inboxId}/tickets`, {
          params: {
            q: this.search,
            show_personal: this.showPersonal,
            labels: labelsIds,
            status: status,
            page: this.tickets[index].page_num + 1,
          },
        })
        .then((response) => {
          this.tickets[index].tickets = this.tickets[index].tickets.concat(
            response.data.results
          );

          this.tickets[index].page_num += 1;
          this.tickets[index].has_next = response.data.has_next;
        });
    },
  },
  created() {
    axios
      .get(`/api/inboxes/${this.$route.params.inboxId}/labels/all`)
      .then((response) => {
        this.inbox_labels = response.data.concat([UNLABELLED_LABEL]);
      });

    axios
      .get(`/api/inboxes/${this.$route.params.inboxId}/role`)
      .then((response) => {
        this.is_staff =
          response.data.key === "AGENT" ||
          response.data.key === "MANAGER" ||
          this.user.is_superuser;
      });

    this.get_tickets();
  },
  computed: {
    ticketsFlattened() {
      return this.tickets
        ?.flatMap((c) => {
          for (let i = 0; i < c.tickets.length; i++)
            c.tickets[i].open = c.label !== "Closed";

          return c.tickets;
        })
        .sort((a, b) => a.lastUpdated < b.lastUpdated);
    },
    ...mapState({
      user: (state) => state.user,
      tickets() {
        return store.getters.inbox(this.$route.params.inboxId)?.tickets;
      },
    }),
    ...mapState('onboarding', {
      onboarding: (state) => state.status
    })
  },
  watch: {
    $route: async function () {
      this.get_tickets();
    },
  },
};
</script>

<style scoped>
.ticket-columns {
  scroll-snap-type: x mandatory;
  scroll-padding: 16px;
}
</style>
