<template>
  <!-- Column based layout for teachers and assistants -->
  <section v-if="is_staff" class="flex flex-col h-full flex-grow justify-start dark:bg-gray-800">
    <div class="flex flex-col md:grid md:grid-cols-5 md:gap-2 p-4 space-y-2 md:space-y-0">
      <div class="flex space-x-2 md:col-span-2 xl:col-span-3 items-center">
        <search-bar v-model="search" v-on:input="callDebounceSearch"></search-bar>
      </div>

      <div class="flex space-x-2 md:col-span-3 xl:col-span-2 items-center">
        <!--FILTER LABELS-->
        <div class="flex-grow">
          <label-dropdown :selected="labels" :values="inbox_labels" v-model="labels" v-on:input="updateLabels" />
        </div>

        <submit-button
          :class="showPersonal ? `bg-primary-500 text-white` : `bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-300` "
          @click="togglePersonal"
          class="px-4 md:m-0 h-10"
          v-if="is_staff"
        >
          My Tickets
        </submit-button>
      </div>
    </div>

    <!-- Columns -->
    <div class="ticket-columns max-w-full flex flex-grow overflow-x-auto pl-4 b-4">
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
      />
    </div>

    <!-- Floating action button for new ticket -->
    <router-link
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
    </router-link>
  </section>

  <!-- Private questions for students -->
  <section v-else class="flex flex-col h-full flex-grow justify-start dark:bg-gray-800">
    <div class="p-4">
      <h2 class="text-lg leading-6 font-medium text-gray-900">Your tickets</h2>
      <p class="mt-1 text-sm text-gray-500">
        These are your personal tickets.
      </p>
    </div>

    <!-- Tickets list (only on smallest breakpoint) -->
    <div class="mt-2 sm:hidden h-full overflow-y-auto">
      <div class="px-4 sm:px-6">
        <h2 class="text-gray-500 text-xs font-medium uppercase tracking-wide">Tickets</h2>
      </div>
      <ul class="mt-3 border-t border-gray-200 divide-y divide-gray-100">
        <li v-for="ticket in ticketsFlattened" :key="ticket.id">
          <router-link :to="`/inboxes/${$route.params.inboxId}/tickets/${ticket.ticket_inbox_id}`" class="group flex items-center justify-between py-3 px-4 hover:bg-gray-50 sm:px-6">
            <span class="flex items-center truncate space-x-2">
              <span class="font-medium truncate text-sm leading-4">
                {{ ticket.title }}
              </span>
            </span>
            <ChevronRightIcon class="ml-4 h-5 w-5 text-gray-400 group-hover:text-gray-500" aria-hidden="true" />
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
              <th class="px-2 py-3 border-b border-gray-200 bg-gray-50 dark:bg-gray-800 text-center text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
              </th>
              <th class="pl-3 pr-6 py-3 border-b border-gray-200 bg-gray-50 dark:bg-gray-800 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                <span class="lg:pl-2">Tickets</span>
              </th>
              <th class="px-6 py-3 border-b border-gray-200 bg-gray-50 dark:bg-gray-800 text-center text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Status
              </th>
              <!-- truncate is a dirty trick here to make sure the words 'last updated' are on the same row -->
              <th class="hidden md:table-cell truncate px-6 py-3 border-b border-gray-200 bg-gray-50 dark:bg-gray-800 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Last updated
              </th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-transparent divide-y divide-gray-100">
            <tr v-for="ticket in ticketsFlattened" :key="ticket.id">
              <td class="px-2 py-3 max-w-0 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-gray-200">
                <GlobeIcon v-if="ticket.is_public" class="h-5 w-5 text-gray-700" />
              </td>
              <td class="pl-3 pr-6 py-3 max-w-0 w-full whitespace-nowrap text-sm font-medium text-gray-900 dark:text-gray-200">
                <div class="flex items-center space-x-3 lg:pl-2">
                  <router-link :to="`/inboxes/${$route.params.inboxId}/tickets/${ticket.ticket_inbox_id}`" class="truncate hover:text-gray-600 dark:hover:text-gray-300">
                    <span>{{ ticket.title }}</span>
                  </router-link>
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
              <td class="hidden md:table-cell px-6 py-3 whitespace-nowrap text-sm text-gray-500 text-right">
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
import axios from 'axios'
import store from '@/store'
import { mapState } from 'vuex'
import _ from 'lodash'
import moment from 'moment'

import SearchBar from '@/components/searchbar/SearchBar'
import SubmitButton from '@/components/button/SubmitButton'
import TicketColumn from '@/components/tickets/TicketColumn'
import LabelDropdown from '@/components/dropdown/LabelDropdown'

import {
  ChevronRightIcon
} from '@heroicons/vue/solid'
import {
  GlobeIcon
} from '@heroicons/vue/outline'

const UNLABELLED_LABEL = {
  id: 0,
  name: 'Unlabelled',
  color: '#2D3748'
}

export default {
  name: 'Inbox',
  components: {
    ChevronRightIcon,
    GlobeIcon,
    TicketColumn,
    LabelDropdown,
    SubmitButton,
    SearchBar
  },
  data: () => ({
    colors: {
      Pending: '#e76f51',
      Assigned: '#e9c46a',
      'Awaiting response': '#2a9d8f',
      Closed: '#264653'
    },
    search: null,
    showPersonal: false,
    labels: [],
    label: null,
    inbox_labels: [],
    is_staff: false
  }),
  setup () {
    return { moment }
  },
  methods: {
    get_tickets () {
      // Call this function by using callDebounceSearch
      const labelsIds = []
      this.labels.forEach((label) => labelsIds.push(label.id))
      const inboxId = this.$route.params.inboxId

      axios
        .get(`/api/inboxes/${inboxId}/tickets`, {
          params: {
            q: this.search,
            show_personal: this.showPersonal,
            labels: labelsIds
          }
        })
        .then(async (response) => {
          if (!store.getters.inbox(inboxId)) await store.dispatch('update_inboxes')

          store.commit('update_tickets', { inbox: inboxId, tickets: response.data })
        })
    },
    callDebounceSearch: _.debounce(function () {
      this.get_tickets()
    }, 300),
    deleteEvent (index) {
      this.labels.splice(index, 1)

      this.get_tickets()
    },
    updateLabels (items) {
      this.labels = items

      this.get_tickets()
    },
    togglePersonal () {
      this.showPersonal = !this.showPersonal
      this.get_tickets()
    },
    loadStatus (status) {
      const labelsIds = []
      this.labels.forEach((label) => labelsIds.push(label.id))
      let index = 0

      if (status === 'Pending') {
        index = 0
      } else if (status === 'Assigned') {
        index = 1
      } else if (status === 'Awaiting response') {
        index = 2
      } else if (status === 'Closed') {
        index = 3
      }

      axios
        .get(`/api/inboxes/${this.$route.params.inboxId}/tickets`, {
          params: {
            q: this.search,
            show_personal: this.showPersonal,
            labels: labelsIds,
            status: status,
            page: this.tickets[index].page_num + 1
          }
        })
        .then((response) => {
          this.tickets[index].tickets = this.tickets[index].tickets.concat(
            response.data.results
          )

          this.tickets[index].page_num += 1
          this.tickets[index].has_next = response.data.has_next
        })
    }
  },
  created () {
    axios
      .get(`/api/inboxes/${this.$route.params.inboxId}/labels/all`)
      .then((response) => {
        this.inbox_labels = response.data.concat([UNLABELLED_LABEL])
      })

    axios
      .get(`/api/inboxes/${this.$route.params.inboxId}/role`)
      .then((response) => {
        this.is_staff = (response.data.key === 'AGENT' || response.data.key === 'MANAGER')
      })

    this.get_tickets()
  },
  computed: {
    ticketsFlattened () {
      return this.tickets?.flatMap(c => {
        for (let i = 0; i < c.tickets.length; i++) c.tickets[i].open = c.label !== 'Closed'

        return c.tickets
      }).sort((a, b) => a.lastUpdated < b.lastUpdated)
    },
    ...mapState({
      user: state => state.user,
      tickets () {
        return store.getters.inbox(this.$route.params.inboxId)?.tickets
      }
    })
  }
}
</script>

<style scoped>
.ticket-columns {
  scroll-snap-type: x mandatory;
  scroll-padding: 16px;
}
</style>
