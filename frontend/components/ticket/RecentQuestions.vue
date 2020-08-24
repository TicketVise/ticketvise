<template>
  <div>
    <h4 class="font-semibold text-gray-800 mb-1">Recent questions</h4>
    <ul class="list-none">
      <li v-for="ticket in tickets" :key="ticket.id">
        <a class="block px-2 py-0.5 bg-gray-100 rounded hover:bg-gray-200 text-sm truncate"
           :href="'/inboxes/' + inbox_id + '/tickets/' + ticket.ticket_inbox_id">
          <span class="font-semibold mr-2">#{{ticket.ticket_inbox_id}}</span>
          {{ticket.title}}
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
  import Avatar from "../elements/Avatar";
  import Card from "../elements/card/Card";

  import axios from "axios";

  export default {
    name: "AuthorCard",
    components: {Card, Avatar},
    props: ["author", "inbox_id"],
    data() {
      return {
        tickets: null,
        role: null,
      }
    },
    mounted() {
      axios.get("/api/inboxes/" + this.inbox_id + "/users/" + this.author.id + "/tickets/recent").then(response => {
        this.tickets = response.data;
      });
      axios.get("/api/inboxes/" + this.inbox_id + "/users/" + this.author.id + "/roles").then(response => {
        this.role = response.data;
      })
    }
  }
</script>

<style scoped>

</style>
