<template>
  <div class="w-full px-4 pt-2">
    <h4 class="font-semibold text-gray-800 mb-2">Assignee</h4>
    <user-dropdown :values="staff" class="full-w" v-bind:value="value" v-on:input="submit"/>
  </div>
</template>

<script>
  import Card from "../elements/card/Card";
  import UserDropdown from "../elements/dropdown/UserDropdown";
  import axios from "axios";

  export default {
    name: "EditAssignee",
    components: {UserDropdown, Card},
    props: ["ticket", "staff"],
    data() {
      return {
        value: this.ticket.assignee,
      }
    },
    methods: {
      submit(user) {
        this.value = user
        let formData = new FormData();
        formData.append("assignee", this.value.id);

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

        axios.put("/api" + window.location.pathname + "/assignee", formData)
            .then(_ => {
              this.ticket.assignee = this.value
            });
      },
    }
  }
</script>

<style scoped>

</style>
