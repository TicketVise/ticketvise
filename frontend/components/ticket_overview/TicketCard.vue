<template>
  <card class="p-2" outlined v-bind:class="{ 'py-1': small }">
    <span class="text-xs text-gray-500 float-right">
      #{{ ticket.ticket_inbox_id }}
    </span>
    <h3 v-if="!small" class="text-xs text-gray-500">{{ date(ticket.date_created) }}</h3>
    <a :href="link" class="font-medium text-gray-900 hover:underline">
      {{ ticket.title }}
    </a>

    <div v-if="!small" class="space-x-1 select-none">
      <chip :key="label.id"
              v-for="label in ticket.labels"
      >{{ label.name }}
      </chip>
    </div>
  </card>
</template>

<script>
  const moment = require('moment')

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
      }
    },
    methods: {
      date: function (date) {
        return moment(date).calendar()
      }
    },
    computed: {
      link: function () {
        return window.location.href + '/' + this.ticket.ticket_inbox_id
      },
      full_name: function () {
        return this.ticket.author.first_name + ' ' + this.ticket.author.last_name
      }
    }
  }
</script>
