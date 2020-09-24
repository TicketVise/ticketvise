<template>
  <section class="flex flex-col h-full flex-grow">
    <div class="flex flex-col md:grid md:grid-cols-5 md:gap-2 p-4 space-y-2 md:space-y-0">
      <search-bar v-model="search" v-on:input="get_tickets" class="flex-grow px-2 md:col-span-3"></search-bar>

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
                v-if="is_staff"> My Tickets </submit-button>
      </div>
    </div>

    <div class="w-full flex md:space-x-4 flex-grow overflow-x-auto px-4 mb-4 space-x-2">
      <!-- Columns -->
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
      is_staff: true,
      user: null
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
      }
    },
    created() {
      this.get_tickets()
      axios.get("/api/inboxes/" + this.inbox_id + "/labels").then(response => {
        this.inbox_labels = response.data;

        axios.get("/api/me").then(response => {
          this.user = response.data

          axios.get("/api/inboxes/" + this.inbox_id + "/role").then(response => {
            this.is_staff = response.data && (response.data.key === 'AGENT' || response.data.key === 'MANAGER')
          })
        })
      });
    },
    computed: {
      unused_labels: function () {
        if (!this.inbox_labels) {
          return []
        }

        const label_ids = this.labels.map(label => label.id)

        return this.inbox_labels.filter(label => !label_ids.includes(label.id))
      }
    }
  }
</script>