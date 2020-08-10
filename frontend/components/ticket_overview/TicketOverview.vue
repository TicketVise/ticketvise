<template>
  <div>
    <div class="flex-wrap md:flex mb-2">
      <search-bar v-model="search" v-on:input="get_tickets" class="flex-grow px-2"></search-bar>

      <!--MY TICKETS-->
      <div v-if="is_staff">
        <submit-button v-if="!showPersonal" class="bg-orange-400 px-2 m-2 md:m-0" text="My Tickets"
                       @click="showPersonal = !showPersonal; get_tickets()"></submit-button>
        <submit-button v-if="showPersonal" class="bg-orange-500 px-2 m-2 md:m-0" text="My Tickets"
                       @click="showPersonal = !showPersonal; get_tickets()"></submit-button>
      </div>

      <!--FILTER LABELS-->
      <div>
        <div class="flex flex-wrap mb-2">
          <chip class="m-1" v-for="(label, index) in labels" :key="label.id" :background="label.color">
            {{ label.name }}
            <a class="fa fa-close" @click="deleteEvent(index)"></a>
          </chip>
        </div>
        <label-dropdown v-model="label" :values="unused_labels" v-on:input="labels.push(label); get_tickets()"
                        class="mx-2"/>
      </div>

    </div>
    <div class="sm:flex-wrap md:flex md:space-x-6 flex-grow min-h-screen">
      <!-- Banner -->

      <!-- Sorteren -->

      <!-- Columns -->
      <ticket-column
          v-for="(column, i) in tickets"
          :key="column.label"
          :title="column.label"
          :color="colors[i]"
          :ticket-list="column.tickets"
          class="m-2 md:m-0"
      />
    </div>
  </div>
</template>

<script>
import SearchBar from "../elements/SearchBar";
import SubmitButton from "../elements/buttons/SubmitButton";
import TicketColumn from "./TicketColumn";
import EditAssignee from "../ticket/EditAssignee";
import EditLabel from "../ticket/EditLabel";
import axios from "axios";

export default {
  components: {EditLabel, EditAssignee, TicketColumn, SubmitButton, SearchBar},
  props: ['title'],
  data: () => ({
    colors: ['#e76f51', '#e9c46a', '#2a9d8f', '#264653'],
    tickets: [],
    search: null,
    debounce_search: null,
    showPersonal: false,
    labels: [],
    label: null,
    inbox_labels: [],
    inbox_id: window.location.pathname.split('/')[2],
    is_staff: false,
    user: null
  }),
  methods: {
    get_tickets() {
      let labels_ids = []
      this.labels.forEach(label => labels_ids.push(label.id))

      window.axios.get(`/api${window.location.pathname}`, {
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
    deleteEvent: function (index) {
      this.labels.splice(index, 1);

      this.get_tickets()
    },
  },
  created() {
    this.get_tickets()
    axios.get("/api/inboxes/" + this.inbox_id + "/labels").then(response => {
      this.inbox_labels = response.data;

      axios.get("/api/me").then(response => {
        this.user = response.data

        axios.get("/api/inboxes/" + this.inbox_id + "/users/" + this.user.id + "/roles").then(response => {

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
