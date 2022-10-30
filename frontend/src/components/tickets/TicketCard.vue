<template>
  <div
    class="relative rounded overflow-hidden bg-white dark:bg-transparent p-2 border"
    v-bind:class="{ 'py-1': small, 'border-primary': assigned }"
  >
    <div class="flex justify-between items-start pb-1 space-x-1">
      <router-link
        :to="link"
        class="font-medium leading-5 text-gray-900 dark:text-gray-200 hover:underline truncate"
      >
        {{ ticket.title }}
      </router-link>

      <span
        v-if="!ticket.is_public"
        class="text-xs text-gray-500 dark:text-gray-400 float-right"
      >
      </span>
      <GlobeEuropeAfricaIcon v-else class="h-4 w-4 text-gray-500 dark:text-gray-400" />
    </div>

    <div class="flex justify-between items-center">
      <h3 v-if="!small" class="text-xs text-gray-500 dark:text-gray-400">
        <span class="font-medium"
          >{{ ticket.author?.first_name }} {{ ticket.author?.last_name }}</span
        >・{{ date(ticket.date_created)
        }}<span v-if="!assignee?.first_name"
          >・<button
            @click="assignUser(ticket.ticket_inbox_id)"
            class="text-primary-600 no-underline font-medium"
          >
            Assign yourself
          </button></span
        >
      </h3>
      <div v-if="ticket.labels.length == 0 && avatar" class="flex-shrink-0">
        <img
          class="h-5 w-5 rounded-full"
          :src="avatar"
          alt=""
          :title="assignee.first_name + ' ' + assignee.last_name"
        />
      </div>
    </div>

    <div class="flex justify-between items-center mt-1">
      <div v-if="!small" class="space-x-1 select-none">
        <chip
          :background="label.color"
          :key="label.id"
          v-for="label in ticket.labels.slice(0, 1)"
        >
          {{ label.name }}
        </chip>
        <span v-if="ticket.labels.length > 1" class="text-gray-600 text-xs"
          >+{{ ticket.labels.length - 1 }}</span
        >
      </div>
      <!-- <div v-if="ticket.labels.length > 0 && avatar" class="flex-shrink-0">
        <img
          class="h-5 w-5 rounded-full"
          :src="avatar"
          alt=""
          :title="assignee.first_name + ' ' + assignee.last_name"
        />
      </div> -->
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapState } from "vuex";
import moment from "moment";
import Chip from "@/components/chip/Chip.vue";

import { GlobeEuropeAfricaIcon } from "@heroicons/vue/24/outline";

moment.locale(navigator.language);

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
    GlobeEuropeAfricaIcon,
  },
  methods: {
    date(date) {
      return moment.parseZone(date).calendar(null, {
        lastDay: "[Yesterday at] HH:mm",
        sameDay: "[Today at] HH:mm",
        nextDay: "[Tomorrow at] HH:mm",
        lastWeek: "[Last] dddd [at] HH:mm",
        nextWeek: "dddd [at] HH:mm",
        sameElse: "L [at] HH:mm",
      });
    },
    assignUser(ticketId) {
      const id =
        this.ticket?.assignee && this.ticket?.assignee.id === this.user.id
          ? []
          : this.user.id;
      const formData = new FormData();
      formData.append("assignee", id);
      axios
        .patch(
          `/api/inboxes/${this.$route.params.inboxId}/tickets/${ticketId}/assignee`,
          formData
        )
        .then((_) => {
          this.$emit("refresh");
        });
    },
  },
  computed: {
    ...mapState({
      user: (state) => state.user,
    }),
    link() {
      return `/inboxes/${this.$route.params?.inboxId}/tickets/${this.ticket?.ticket_inbox_id}`;
    },
    assignee() {
      return this.ticket?.assignee;
    },
    assigned() {
      return this.assignee?.username === this.user?.username;
    },
    avatar() {
      return this.assignee?.avatar_url;
    },
  },
};
</script>
