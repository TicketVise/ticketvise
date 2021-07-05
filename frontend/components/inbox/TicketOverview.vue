<template>
  <section class="flex flex-col h-full flex-grow justify-start">
    <div class="flex flex-col md:grid md:grid-cols-5 md:gap-2 p-4 space-y-2 md:space-y-0">
      <div class="flex space-x-2 md:col-span-2 xl:col-span-3 items-center">
        <search-bar v-model="search" v-on:input="callDebounceSearch"></search-bar>
      </div>

      <div class="flex space-x-2 md:col-span-3 xl:col-span-2 items-center">
        <!--FILTER LABELS-->
        <div class="flex-grow">
          <label-dropdown :selected="labels" :values="inbox_labels" v-model="labels" v-on:input="updateLabels"/>
        </div>

        <submit-button
          :class="showPersonal ? `bg-orange-500 text-white` : `bg-gray-100 text-black` "
          @click="togglePersonal"
          class="px-2 md:m-0 h-10"
          v-if="is_staff"
        >
          <font-awesome-icon :icon="showPersonal ? 'check' : 'minus'" class="mr-2"></font-awesome-icon>
          My Tickets
        </submit-button>
      </div>
    </div>

    <!-- Columns -->
    <div class="max-w-full flex flex-grow overflow-x-auto pl-4 b-4">
      <ticket-column
        v-for="(column, i) in tickets"
        :key="i"
        :color="colors[column.label]"
        :title="column.label"
        :personal="showPersonal"
        :ticket-list="column.tickets"
        :has_next="column.has_next"
        :length="column.total"
        @input="loadStatus(column.label)"
        class="min-w-3/5 sm:min-w-1/2 md:min-w-0 pr-4"
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
</template>

<script>
  import SearchBar from "../elements/SearchBar";
  import SubmitButton from "../elements/buttons/SubmitButton";
  import TicketColumn from "./TicketColumn";
  import LabelDropdown from "../elements/dropdown/LabelDropdown";

  import {library} from '@fortawesome/fontawesome-svg-core'
  import {faCheck, faMinus} from '@fortawesome/free-solid-svg-icons'
  import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'
  import axios from "axios";
  import _ from 'lodash';

  library.add([faMinus, faCheck])

  const UNLABELLED_LABEL = {
    id: 0,
    name: "Unlabelled",
    color: "#2D3748"
  }

  export default {
    components: {
      TicketColumn,
      LabelDropdown,
      SubmitButton,
      SearchBar,
      FontAwesomeIcon
    },
    data: () => ({
      colors: {
        'Pending': '#e76f51',
        'Assigned': '#e9c46a',
        'Awaiting response': '#2a9d8f',
        'Closed': '#264653'
      },
      tickets: [
        { label: 'Pending', total: 1 },
        { label: 'Assigned', total: 4 },
        { label: 'Awaiting response', total: 2 },
        { label: 'Closed', total: 3 }
      ],
      search: null,
      showPersonal: false,
      labels: [],
      label: null,
      inbox_labels: [],
      is_staff: false,
    }),
    methods: {
      get_tickets() {
        // Call this function by using callDebounceSearch
        let labels_ids = [];
        this.labels.forEach(label => labels_ids.push(label.id));
        const inboxId = this.$route.params.inboxId

        axios.get(`/api/inboxes/${inboxId}/tickets`, {
          params: {
            q: this.search,
            show_personal: this.showPersonal,
            labels: labels_ids
          }
        }).then(response => {
          this.tickets = response.data
        })
      },
      callDebounceSearch: _.debounce(function () {
        this.get_tickets();
      }, 300),
      deleteEvent(index) {
        this.labels.splice(index, 1)

        this.get_tickets()
      },
      updateLabels(items) {
        this.labels = items

        this.get_tickets()
      },
      togglePersonal() {
        this.showPersonal = !this.showPersonal
        this.get_tickets()
      },
      loadStatus(status) {
        let labels_ids = [];
        this.labels.forEach(label => labels_ids.push(label.id));
        let index = 0

        if (status === "Pending") {
          index = 0
        } else if (status === "Assigned") {
          index = 1
        } else if (status === "Awaiting response") {
          index = 2
        } else if (status === "Closed") {
          index = 3
        }

        axios.get(`/api/inboxes/${this.$route.params.inboxId}/tickets`, {
          params: {
            q: this.search,
            show_personal: this.showPersonal,
            labels: labels_ids,
            status: status,
            page: this.tickets[index].page_num + 1
          }
        }).then(response => {
          this.tickets[index].tickets = this.tickets[index].tickets.concat(response.data.results)

          this.tickets[index].page_num += 1
          this.tickets[index].has_next = response.data.has_next
        })
      }
    },
    created() {
      axios.get(`/api/inboxes/${this.$route.params.inboxId}/labels/all`).then(response => {
        this.inbox_labels = response.data.concat([UNLABELLED_LABEL])
      })

      axios.get(`/api/inboxes/${this.$route.params.inboxId}/role`).then(response => {
        this.is_staff = response.data && (response.data.key === 'AGENT' || response.data.key === 'MANAGER')
      })

      this.get_tickets()
    },
    computed: {
      user() {
        return this.$store.state.user;
      }
    }
  }
</script>
