<template>
  <div v-if="role == 'MANAGER'">
    <div class="p-4">
      <div class="max-w-3xl mx-auto flex flex-col space-y-3">
        <div class="overflow-hidden rounded-lg bg-white border">
          <div class="p-2 px-4">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <InboxStackIcon class="w-6 h-6 text-gray-400" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="truncate text-sm font-medium text-gray-500">Tickets</dt>
                  <dd class="flex justify-between items-center">
                    <div class="text-xl font-medium text-primary">
                      4
                      <span class="ml-1 text-sm font-medium text-gray-500"> from 3 last week </span>
                    </div>

                    <div :class="['increase' === 'increase' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800', 'inline-flex items-baseline px-2.5 py-0.5 rounded-full text-sm font-medium md:mt-2 lg:mt-0']">
                      <ArrowSmallUpIcon v-if="'up' === 'up'" class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5" :class="['increase' === 'increase' ? 'text-green-500' : 'text-red-500']" aria-hidden="true" />
                      <ArrowSmallDownIcon v-else class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5" :class="['increase' === 'increase' ? 'text-green-500' : 'text-red-500']" aria-hidden="true" />
                      <span class="sr-only"> {{ 'increase' === 'increase' ? 'Increased' : 'Decreased' }} by </span>
                      33%
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="overflow-hidden rounded-lg bg-white border">
          <div class="p-2 px-4">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <ChatBubbleLeftRightIcon class="w-6 h-6 text-gray-400" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="truncate text-sm font-medium text-gray-500">Response time</dt>
                  <dd class="flex justify-between items-center">
                    <div class="text-xl font-medium text-primary">
                      7.9h
                      <span class="ml-1 text-sm font-medium text-gray-500"> from 6.2h last week </span>
                    </div>

                    <div :class="['decrease' === 'increase' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800', 'inline-flex items-baseline px-2.5 py-0.5 rounded-full text-sm font-medium md:mt-2 lg:mt-0']">
                      <ArrowSmallUpIcon v-if="'up' === 'up'" class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5" :class="['decrease' === 'increase' ? 'text-green-500' : 'text-red-500']" aria-hidden="true" />
                      <ArrowSmallDownIcon v-else class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5" :class="['increase' === 'increase' ? 'text-green-500' : 'text-red-500']" aria-hidden="true" />
                      <span class="sr-only"> {{ 'increase' === 'increase' ? 'Increased' : 'Decreased' }} by </span>
                      27%
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="rounded-md bg-yellow-50 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <ExclamationTriangleIcon class="h-5 w-5 text-yellow-400" aria-hidden="true" />
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-yellow-800">Attention needed</h3>
              <div class="mt-2 text-sm text-yellow-700">
                <p>There are suddenly a lot of tickets about: <strong>Assignment 2</strong></p>
                <router-link :to="`/inboxes/${$route.params.inboxId}/tickets`" class="flex items-center mt-1">
                  <span>See tickets</span>
                  <ArrowRightIcon class="inline-block w-4 h-4 ml-1" />
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else-if="role == 'AGENT'">
    <div class="p-4">
      <div class="max-w-3xl mx-auto flex flex-col space-y-4">
        <router-link
          :to="`/inboxes/1/tickets/1`"
          class="group border rounded-lg flex flex-col p-3"
        >
          <div class="flex justify-between">
            <div class="flex space-x-2 text-red-600">
              <ExclamationCircleIcon class="w-5 h-5" />
              <span class="font-medium text-sm">HIGH</span>
            </div>
            <span
              class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800"
              >Created</span
            >
          </div>

          <h2
            class="font-semibold text-lg group-hover:underline mt-1 leading-6"
          >
            Should we write the individual report in the passive form?
          </h2>

          <div class="flex justify-between items-center">
            <h3 class="text-xs text-gray-500 dark:text-gray-400">
              <span class="font-medium">Ivan de Wolf</span>・Today at 00:35
            </h3>
          </div>

          <div class="flex mt-2">
            <chip background="#FF0000">Assignment</chip>
          </div>
        </router-link>

        <router-link
          :to="`/inboxes/1/tickets/1`"
          class="group border rounded-lg flex flex-col p-3"
        >
          <div class="flex justify-between">
            <div class="flex space-x-2 text-yellow-600">
              <BellIcon class="w-5 h-5" />
              <span class="font-medium text-sm">MEDIUM</span>
            </div>
            <span
              class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-yellow-100 text-yellow-800"
              >Reaction</span
            >
          </div>

          <h2
            class="font-semibold text-lg group-hover:underline mt-1 leading-6"
          >
            Is there a lecture on the day of the demo?
          </h2>

          <div class="flex justify-between items-center">
            <h3 class="text-xs text-gray-500 dark:text-gray-400">
              <span class="font-medium">Jurre Brandsen</span>・Yesterday 17:36
            </h3>
          </div>

          <div class="flex mt-2">
            <chip background="#0000FF">Lectures</chip>
          </div>
        </router-link>
      </div>
    </div>
  </div>

  <div class="flex h-full" v-else-if="role == 'STUDENT'">
    <div class="flex flex-col h-full p-4 pb-0 overflow-hidden">
      <h2 class="text-sm uppercase text-gray-600 border-b pb-1">Active tickets</h2>

      <div class="pt-2 pb-4 space-y-2 overflow-y-auto">
        <TicketCard v-for="ticket in ticketsFlattened?.filter(t => t.open)" :key="ticket" :ticket="ticket" :assignee_show="false" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"
import store from "@/store"
import { mapState } from "vuex"

import Chip from "@/components/chip/Chip.vue"
import TicketCard from "@/components/tickets/TicketCard.vue"

import { BellIcon, ChatBubbleLeftRightIcon, ExclamationCircleIcon, InboxStackIcon } from "@heroicons/vue/24/outline"
import { ArrowSmallDownIcon, ArrowSmallUpIcon } from '@heroicons/vue/24/solid'
import { ArrowRightIcon, ExclamationTriangleIcon } from "@heroicons/vue/20/solid"

import report from "@/assets/img/svg/report.svg"

const UNLABELLED_LABEL = {
  id: 0,
  name: "Unlabelled",
  color: "#2D3748",
}

export default {
  name: "Overview",
  components: {
    ArrowSmallDownIcon,
    ArrowSmallUpIcon,
    BellIcon,
    Chip,
    ExclamationCircleIcon,
    InboxStackIcon,
    ChatBubbleLeftRightIcon,
    ExclamationTriangleIcon,
    ArrowRightIcon,
    TicketCard
  },
  data: () => ({
    role: "STUDENT",
    labels: [],
    inbox_labels: [],
    report
  }),
  created() {
    axios
      .get(`/api/inboxes/${this.$route.params.inboxId}/labels/all`)
      .then((response) => {
        this.inbox_labels = response.data.concat([UNLABELLED_LABEL]);
      })

    axios
      .get(`/api/inboxes/${this.$route.params.inboxId}/role`)
      .then((response) => {
        if (response.data.key === "MANAGER") this.role = "MANAGER"
        else if (response.data.key === "AGENT") this.role = "AGENT"
        else this.role = "STUDENT"
      })

    this.get_tickets()
  },
  methods: {
    get_tickets() {
      // Call this function by using callDebounceGetTickets
      const labelsIds = [];
      this.labels.forEach((label) => labelsIds.push(label.id));
      const { inboxId } = this.$route.params;

      axios
        .get(`/api/inboxes/${inboxId}/tickets`, {
          params: {
            q: this.search,
            show_personal: this.showPersonal,
            labels: labelsIds,
          },
        })
        .then(async (response) => {
          if (!store.getters.inbox(inboxId))
            await store.dispatch("update_inboxes");

          store.commit("update_tickets", {
            inbox: inboxId,
            tickets: response.data,
          });
        });
    }
  },
  computed: {
    ticketsFlattened() {
      return this.tickets
        ?.flatMap((c) => {
          for (let i = 0; i < c.tickets.length; i++)
            c.tickets[i].open = c.label !== "Closed";

          return c.tickets;
        })
        .sort((a, b) => a.lastUpdated < b.lastUpdated);
    },
    ...mapState({
      user: (state) => state.user,
      tickets() {
        return store.getters.inbox(this.$route.params.inboxId)?.tickets
      },
    }),
  },
}
</script>
