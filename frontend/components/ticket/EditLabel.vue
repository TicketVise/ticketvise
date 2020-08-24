<template>
  <div class="flex flex-column items-start">
    <h4 class="font-semibold text-gray-800 mb-2">Labels</h4>
    <div class="flex flex-wrap mb-2">
      <chip :background="label.color" :key="label.id" class="m-1" v-for="(label, index) in ticket.labels">
        {{label.name}}
        <a @click="deleteEvent(index)" class="fa fa-close"></a>
      </chip>
    </div>

    <label-dropdown :values="unused_labels" class="w-full" v-bind:value="value" v-on:input="submit"/>
  </div>

</template>

<script>
  import Chip from "../elements/chip/Chip";
  import LabelDropdown from "../elements/dropdown/LabelDropdown";
  import axios from "axios";

  export default {
    components: {LabelDropdown, Chip},
    name: "EditLabel",
    props: ["ticket"],
    data() {
      return {
        value: null,
        labels: [],
      }
    },
    mounted() {
      axios.get("/api/inboxes/" + this.ticket.inbox + "/labels").then(response => {
        this.labels = response.data;
      });
    },
    methods: {
      submit(label) {
        this.ticket.labels.push(label)

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

        axios.put("/api" + window.location.pathname + "/labels",
            {
              "labels": this.ticket.labels.map(label => label.id)
            }).then(response => {
          this.value = null
        });
      },
      deleteEvent: function (index) {
        this.ticket.labels.splice(index, 1);

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

        axios.put("/api" + window.location.pathname + "/labels",
            {
              "labels": this.ticket.labels.map(label => label.id)
            }).then(_ => {
        });
      }
    },
    computed: {
      unused_labels: function () {
        if (!this.labels) {
          return []
        }

        const ticket_label_ids = this.ticket.labels.map(label => label.id)

        return this.labels.filter(label => !ticket_label_ids.includes(label.id))
      }
    }
  }
</script>

<style scoped>

</style>