<template>
  <div>
    <h4 class="font-semibold text-gray-800 mb-1">Recent questions</h4>
    <ul class="list-none">
      <li :key="ticket.id" v-for="ticket in tickets">
        <router-link :to="'/inboxes/' + inbox_id + '/tickets/' + ticket.ticket_inbox_id"
           class="block px-2 py-0.5 bg-gray-100 rounded hover:bg-gray-200 text-sm truncate">
          <span class="font-semibold mr-2">#{{ticket.ticket_inbox_id}}</span>
          {{ticket.title}}
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script>
  import Avatar from "../elements/Avatar";
  import Card from "../elements/card/Card";

  import axios from "axios";

  export default {
    name: "RecentQuestions",
    components: {Card, Avatar},
    props: ["author", "inbox_id"],
    data() {
      return {
        tickets: null,
      }
    },
    mounted() {
      axios.get(`/api/inboxes/${this.inbox_id}/users/${this.author.id}/tickets/recent`).then(response => {
        this.tickets = response.data;
      });
    }
  }
</script>

<style scoped>

</style>
