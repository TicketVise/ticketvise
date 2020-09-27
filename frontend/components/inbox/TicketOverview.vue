<template>
  <section class="flex flex-col h-full flex-grow">
    <div class="flex flex-col md:grid md:grid-cols-5 md:gap-2 p-4 space-y-2 md:space-y-0">
      <div class="flex space-x-2 md:col-span-3 items-center">
        <search-bar v-model="search" v-on:input="get_tickets" class="flex-grow px-2"></search-bar>

        <!-- Change view -->
        <button
          class="md:hidden border rounded h-10 px-3 focus:outline-none hover:bg-gray-100"
          :title="list ? 'Show Columns View' : 'Show List View'"
          @click="toggleView"
        >
          <font-awesome-icon :icon="list ? 'columns' : 'list'"></font-awesome-icon>
        </button>
      </div>

      <!--MY TICKETS-->
      <div class="flex space-x-2 md:col-span-2 items-center">
        <!--FILTER LABELS-->
        <div class="flex-grow">
          <label-dropdown :selected="labels" :values="inbox_labels" v-model="labels" v-on:input="updateLabels"/>
        </div>

        <submit-button
            :class="showPersonal ? `bg-orange-500 text-white` : `bg-gray-100 text-black shadow` "
            @click="showPersonal = !showPersonal; get_tickets()"
            class="px-2 md:m-0"
            v-if="is_staff"> My Tickets
        </submit-button>

        <!-- Change view -->
        <button
          class="hidden md:block border rounded h-10 px-3 focus:outline-none hover:bg-gray-100"
          :title="list ? 'Show Columns View' : 'Show List View'"
          @click="list = !list"
        >
          <font-awesome-icon :icon="list ? 'columns' : 'list'"></font-awesome-icon>
        </button>
      </div>
    </div>

    <!-- List -->
    <div v-if="list" class="container mx-auto flex flex-col space-y-4 mb-4">
      <ticket-list
        :color="colors[i]"
        :key="column.label"
        :ticket-list="column.tickets"
        :title="column.label"
        v-for="(column, i) in tickets"
      />

      <div v-if="tickets.length" class="flex flex-col items-center w-full">
        <img src="/static/img/svg/undraw_blank_canvas_3rbb.svg" alt="Nothing here" class="w-1/2 md:w-1/3 mx-auto py-8">
        <span class="text-gray-600 text-lg md:text-xl">You have no tickets (yet)!</span>
      </div>
    </div>

    <!-- Columns -->
    <div v-else class="w-full flex md:space-x-4 flex-grow overflow-x-auto px-4 mb-4 space-x-2">
      <ticket-column
        :color="colors[i]"
        :key="column.label"
        :ticket-list="column.tickets"
        :title="column.label"
        class="min-w-3/4 sm:min-w-1/2 lg:min-w-0"
        v-for="(column, i) in tickets"
      />
    </div>
  </section>
</template>

<script>
import SearchBar from "../elements/SearchBar";
import SubmitButton from "../elements/buttons/SubmitButton";
import TicketColumn from "./TicketColumn";
import LabelDropdown from "../elements/dropdown/LabelDropdown";

import axios from "axios";

const UNLABELLED_LABEL = {
  id: 0,
  name: "Unlabelled",
  color: "#2D3748"
}

export default {
  components: {TicketColumn, LabelDropdown, SubmitButton, SearchBar},
  data: () => ({
    colors: ['#e76f51', '#e9c46a', '#2a9d8f', '#264653'],
    tickets: [],
    search: null,
    showPersonal: false,
    labels: [],
    label: null,
    inbox_labels: [],
    inbox_id: window.location.pathname.split('/')[2],
    is_staff: false,
    user: null,
    list: false
  }),
  methods: {
    get_tickets() {
      let labels_ids = []
      this.labels.forEach(label => labels_ids.push(label.id))

      axios.get(`/api${window.location.pathname}`, {
        params: {
          columns: true,
          q: this.search,
          show_personal: this.showPersonal,
          labels: labels_ids
        }
      }).then(response => {
        this.tickets = response.data
      })
    },
    deleteEvent(index) {
      this.labels.splice(index, 1)

      this.get_tickets()
    },
    updateLabels(items) {
      this.labels = items

      this.get_tickets()
    },
    toggleView() {
      this.list = !this.list
      localStorage.setItem('inbox_view', (this.list ? 'list' : 'column'))
    }
  },
  created() {
    this.get_tickets()
    axios.get("/api/inboxes/" + this.inbox_id + "/labels").then(response => {
      this.inbox_labels = response.data.concat([UNLABELLED_LABEL])
    })

    axios.get("/api/me").then(response => {
      this.user = response.data
    })

    axios.get("/api/inboxes/" + this.inbox_id + "/role").then(response => {
      this.is_staff = response.data && (response.data.key === 'AGENT' || response.data.key === 'MANAGER')

      let pref = localStorage.getItem('inbox_view')
      if (!pref) {
        localStorage.setItem('inbox_view', this.is_staff ? 'column' : 'list')
        pref = localStorage.getItem('inbox_view')
      }
      this.list = pref == 'list'
    })
  }
}
</script>
