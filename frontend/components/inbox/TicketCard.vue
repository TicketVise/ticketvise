<template>
  <div
    class="relative rounded overflow-hidden bg-white p-2 border"
    v-bind:class="{ 'py-1': small, 'border-primary': ticket.assignee && ticket.assignee.username == user.username }"
  >
    <div class="flex justify-between items-start pb-1">
      <router-link
        :to="link"
        class="font-medium leading-4 text-gray-900 hover:underline"
      >
        {{ ticket.title }}
      </router-link>

      <span class="text-xs text-gray-500 float-right">
        #{{ ticket.ticket_inbox_id }}
      </span>
    </div>

    <div class="flex justify-between items-center">
      <h3 v-if="!small" class="text-xs text-gray-500">
        <span class="font-medium">{{ ticket.author.first_name }} {{ ticket.author.last_name }}</span>・{{ date(ticket.date_created) }}
      </h3>
      <div v-if="ticket.labels.length == 0 && ticket.assignee.avatar_url" class="flex-shrink-0">
        <img class="h-5 w-5 rounded-full" :src="ticket.assignee.avatar_url" alt="" :title="ticket.assignee.first_name + ' ' + ticket.assignee.last_name" />
      </div>
    </div>
    <!-- TODO: Implement easy assign button. -->
    <!-- <h3
      v-if="!ticket || !ticket.assignee || !ticket.assignee.username"
      class="text-xs text-gray-500"
      >Assignee: No one—<button class="hover:text-orange-600 no-underline">
        Assign yourself
      </button></h3
    > -->
    <!-- <h3
      class="text-xs text-gray-500"
      v-if="!small && ticket.assignee && ticket.assignee.username"
    >
      {{ ticket.author.first_name }} {{ ticket.author.last_name }}
    </h3> -->

    <div class="flex justify-between items-center">
      <div v-if="!small" class="space-x-1 select-none">
        <chip
          :background="label.color"
          :key="label.id"
          v-for="label in ticket.labels"
        >
          {{ label.name }}
        </chip>
      </div>
      <div v-if="ticket.labels.length > 0 && ticket.assignee.avatar_url" class="flex-shrink-0">
        <img class="h-5 w-5 rounded-full" :src="ticket.assignee.avatar_url" alt="" :title="ticket.assignee.first_name + ' ' + ticket.assignee.last_name" />
      </div>
    </div>
  </div>
</template>

<script>
import Card from "../elements/card/Card";
import { calendarDate } from "../../utils";
import Chip from "../elements/chip/Chip";

export default {
  props: {
    ticket: {
      type: Object,
      require: true,
    },
    small: {
      type: Boolean,
      required: false,
      default: false,
    },
    assignee_show: {
      type: Boolean,
      required: false,
      default: true,
    },
  },
  components: {
    Chip,
    Card,
  },
  methods: {
    date: calendarDate,
  },
  computed: {
    link: function () {
      return `/inboxes/${this.$route.params.inboxId}/tickets/${this.ticket.ticket_inbox_id}`;
    },
    user() {
      return this.$store.state.user;
    }
  },
};
</script>
