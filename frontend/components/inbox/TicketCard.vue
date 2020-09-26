<template>
  <card class="p-2" outlined v-bind:class="{ 'py-1': small }">
    <span class="text-xs text-gray-500 float-right">
      #{{ ticket.ticket_inbox_id }}
    </span>

    <h3 v-if="!small" class="text-xs text-gray-500">{{ date(ticket.date_created) }}</h3>
    <h3 class="text-xs text-gray-500" v-if="!small && ticket.assignee && ticket.assignee.username">
      Assignee: {{ticket.assignee.first_name }} {{ ticket.assignee.last_name }}
    </h3>

    <a :href="link" class="font-medium text-gray-900 hover:underline">
      {{ ticket.title }}
    </a>

    <div v-if="!small" class="space-x-1 select-none">
      <chip :background="label.color" :key="label.id" v-for="label in ticket.labels">
        {{ label.name }}
      </chip>
    </div>
  </card>
</template>

<script>
  import Card from "../elements/card/Card";
  import {calendarDate} from "../../utils";

  export default {
    props: {
      ticket: {
        type: Object,
        require: true
      },
      small: {
        type: Boolean,
        required: false,
        default: false
      },
      assignee_show: {
        type: Boolean,
        required: false,
        default: true
      }
    },
    components: {
      Card
    },
    methods: {
      date: calendarDate
    },
    computed: {
      link: function () {
        return window.location.href + '/' + this.ticket.ticket_inbox_id
      }
    }
  }
</script>
