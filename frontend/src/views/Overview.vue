<template>
  <div v-if="role == 'MANAGER'">
    <div class="p-4 overflow-y-auto">
      <div class="max-w-3xl mx-auto flex flex-col space-y-3">
        <div class="mb-1">
          <h2 class="text-gray-800 text-xl font-bold leading-6">Overview</h2>
          <span class="text-gray-400">Here you find the most important information for you</span>
        </div>

        <div class="grid grid-cols-2 gap-2">
          <div class="overflow-hidden rounded-lg bg-white border">
            <div class="p-2 px-4">
              <div class="flex items-center">
                <div class="hidden sm:flex flex-shrink-0">
                  <InboxStackIcon class="w-6 h-6 text-gray-400" />
                </div>
                <div class="sm:ml-5 w-0 flex-1">
                  <dl>
                    <dt class="truncate text-sm font-medium text-gray-500">Tickets this week</dt>
                    <dd class="flex justify-between items-center">
                      <div class="text-xl font-medium text-primary">
                        {{ statsData.total_tickets }}
                        <span class="hidden lg:inline ml-1 text-sm font-medium text-gray-500"> from {{ statsData.last_week_total_tickets }} last week </span>
                      </div>

                      <!-- <div :class="['increase' === 'increase' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800', 'inline-flex items-baseline px-2.5 py-0.5 rounded-full text-sm font-medium md:mt-2 lg:mt-0']">
                        <ArrowSmallUpIcon v-if="'up' === 'up'" class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5" :class="['increase' === 'increase' ? 'text-green-500' : 'text-red-500']" aria-hidden="true" />
                        <ArrowSmallDownIcon v-else class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5" :class="['increase' === 'increase' ? 'text-green-500' : 'text-red-500']" aria-hidden="true" />
                        <span class="sr-only"> {{ 'increase' === 'increase' ? 'Increased' : 'Decreased' }} by </span>
                        33%
                      </div> -->
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="overflow-hidden rounded-lg bg-white border">
            <div class="p-2 px-4">
              <div class="flex items-center">
                <div class="hidden sm:flex flex-shrink-0">
                  <ChatBubbleLeftRightIcon class="w-6 h-6 text-gray-400" />
                </div>
                <div class="sm:ml-5 w-0 flex-1">
                  <dl>
                    <dt class="truncate text-sm font-medium text-gray-500">Average response time</dt>
                    <dd class="flex justify-between items-center">
                      <div class="text-xl font-medium text-primary">
                        {{ statsData.avg_response_time }}h
                        <span class="hidden lg:inline ml-1 text-sm font-medium text-gray-500"> from 6.2h last week </span>
                      </div>

                      <!-- <div :class="['decrease' === 'increase' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800', 'inline-flex items-baseline px-2.5 py-0.5 rounded-full text-sm font-medium md:mt-2 lg:mt-0']">
                        <ArrowSmallUpIcon v-if="'up' === 'up'" class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5" :class="['decrease' === 'increase' ? 'text-green-500' : 'text-red-500']" aria-hidden="true" />
                        <ArrowSmallDownIcon v-else class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5" :class="['increase' === 'increase' ? 'text-green-500' : 'text-red-500']" aria-hidden="true" />
                        <span class="sr-only"> {{ 'increase' === 'increase' ? 'Increased' : 'Decreased' }} by </span>
                        27%
                      </div> -->
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        <h2 class="text-gray-700 text-lg font-semibold leading-4 pt-4">Updates</h2>

        <div v-if="onboarding.active" class="border border-primary rounded-lg flex px-4 py-3">
          <div class="flex flex-col text-gray-800">
            <h2 class="font-bold text-primary text-xl">Hi There! 👋</h2>
            <p class="text-sm mt-1 text-justify">This is the <strong>overview page</strong>. Here you will find the necessary information relevant for you. We will show you important insights about the inbox and show you the tickets that are relevant for you. Like the example ticket you see below!</p>
            <div class="flex justify-end text-sm mt-2">
              <button @click="nextStep()">
                <span class="text-primary uppercase font-medium">Got it!</span>
              </button>
            </div>
          </div>
        </div>

        <div v-else-if="updates.length == 0" class="border rounded-lg flex p-2">
          <img :src="awesome" class="w-1/3 md:w-1/5" />
          <div class="flex flex-col px-4">
            <h2 class="font-bold text-primary text-xl">All good</h2>
            <p class="text-sm">Right now there are no updates that require your attention</p>
          </div>
        </div>

        <div v-else>
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

        <div v-if="onboarding.active">
          <h2 class="text-gray-700 text-lg font-semibold leading-4 pt-4">Tickets</h2>
          
          <div class="group border rounded-lg flex flex-col p-3 mt-2">
            <div class="flex justify-between mb-1">
              <div class="flex space-x-2 text-red-600">
                <ExclamationCircleIcon class="w-5 h-5" />
                <span class="font-medium text-sm">HIGH</span>
              </div>
              <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">Created</span>
            </div>
  
            <h2 class="font-semibold text-lg group-hover:underline leading-6">
              This is an example ticket
            </h2>
  
            <div class="flex justify-between items-center">
              <h3 class="text-xs text-gray-500 dark:text-gray-400">
                <span class="font-medium">John Doe</span>・{{ moment().calendar() }}
              </h3>
            </div>
  
            <div class="flex mt-2 space-x-1 select-none items-center">
              <chip :background="'#dd6b20'">Lectures</chip>
            </div>
          </div>
        </div>

        <h2 v-if="ticketsFlattened?.filter(t => t.open)?.length > 0" class="text-gray-700 text-lg font-semibold leading-4 pt-4">Tickets</h2>
        
        <div v-if="ticketsFlattened?.filter(t => t.open)?.length > 0" class="flex flex-col space-y-2">
          <router-link
            v-for="ticket in ticketsFlattened?.filter(t => t.open)"
            :key="ticket.id"
            :to="`/inboxes/${1}/tickets/${ticket.ticket_inbox_id}`"
            class="group border rounded-lg flex flex-col p-3"
          >
            <div v-if="false" class="flex justify-between mb-1">
              <div class="flex space-x-2 text-orange-600">
                <ExclamationCircleIcon class="w-5 h-5" />
                <span class="font-medium text-sm">MEDIUM</span>
              </div>
              <span
                class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800"
                >Response</span
              >
            </div>
  
            <h2 class="font-semibold text-lg group-hover:underline leading-6">
              {{ ticket.title }}
            </h2>
  
            <div class="flex justify-between items-center">
              <h3 class="text-xs text-gray-500 dark:text-gray-400">
                <span class="font-medium">{{ ticket.author.first_name + ' ' + ticket.author.last_name }}</span>・{{ moment(ticket.created_at).calendar() }}
              </h3>
            </div>
  
            <div class="flex mt-2 space-x-1 select-none items-center">
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
          </router-link>
        </div>
      </div>
    </div>
  </div>

  <div v-else-if="role == 'AGENT'">
    <div class="p-4">
      <div class="max-w-3xl mx-auto flex flex-col space-y-2">
        <div class="mb-1">
          <h2 class="text-gray-700 text-xl font-bold leading-6">Overview</h2>
          <span class="text-gray-400">Here you find the most important information for you</span>
        </div>

        <div class="grid grid-cols-2 gap-2">
          <div class="overflow-hidden rounded-lg bg-white border">
            <div class="p-2 px-4">
              <div class="flex items-center">
                <div class="hidden sm:flex flex-shrink-0">
                  <InboxStackIcon class="w-6 h-6 text-gray-400" />
                </div>
                <div class="sm:ml-5 w-0 flex-1">
                  <dl>
                    <dt class="truncate text-sm font-medium text-gray-500">Helpfulness</dt>
                    <dd class="flex justify-between items-center">
                      <div class="text-xl font-medium text-primary">
                        85%
                        <span class="hidden lg:inline ml-1 text-sm font-medium text-gray-500"> from 71% last week </span>
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
                <div class="hidden sm:flex flex-shrink-0">
                  <ChatBubbleLeftRightIcon class="w-6 h-6 text-gray-400" />
                </div>
                <div class="sm:ml-5 w-0 flex-1">
                  <dl>
                    <dt class="truncate text-sm font-medium text-gray-500">Your response time</dt>
                    <dd class="flex justify-between items-center">
                      <div class="text-xl font-medium text-primary">
                        7.9h
                        <span class="hidden lg:inline ml-1 text-sm font-medium text-gray-500"> from 6.2h last week </span>
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
        </div>

        <h2 class="text-gray-700 text-lg font-semibold leading-4 pt-4">Updates</h2>

        <div class="rounded-md bg-blue-50 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <ClockIcon class="h-5 w-5 text-blue-400" aria-hidden="true" />
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-blue-700">Good you are here</h3>
              <div class="mt-2 text-sm text-blue-700">
                <p>But most tickets come around <strong>15:00</strong>, so try to come back then to answer tickets quickly</p>
              </div>
            </div>
          </div>
        </div>

        <h2 class="text-gray-700 text-lg font-semibold leading-4 pt-4">Tickets</h2>

        <div v-if="tickets?.length == 0" class="border rounded-lg flex p-2">
          <img :src="awesome" class="w-1/3 md:w-1/5" />
          <div class="flex flex-col px-4">
            <h2 class="font-bold text-primary text-xl">Well done!</h2>
            <p class="text-sm">Right now there are no tickets that require your attention</p>
          </div>
        </div>
        
        <div v-else>
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
        </div>
      </div>
    </div>
  </div>

  <div v-else-if="role == 'STUDENT'">
    <div class="p-4">
      <div class="max-w-3xl mx-auto flex flex-col space-y-2">
        <div class="mb-1">
          <h2 class="text-gray-700 text-xl font-bold leading-6">Your tickets</h2>
          <span class="text-gray-400">Here you find your tickets</span>
        </div>

        <div v-if="ticketsFlattened?.filter(t => t.open)?.length == 0">
          <router-link :to="`/inboxes/${$route.params.inboxId}/tickets/new`" type="button" class="relative block w-full rounded-lg border-2 border-dashed border-gray-300 p-4 text-center hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2">
            <svg class="mx-auto h-12 w-12 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>

            <span class="mt-2 block text-sm font-medium text-gray-900">Create a new ticket</span>
          </router-link>
        </div>

        <div v-else>
          <ul class="border-b border-gray-200 divide-y divide-gray-100">
            <li v-for="ticket in ticketsFlattened?.filter(t => t.open)" :key="ticket.id">
              <router-link
                :to="`/inboxes/${$route.params.inboxId}/tickets/${ticket.ticket_inbox_id}`"
                class="group flex items-center justify-between py-3 hover:bg-gray-50 sm:px-6"
              >
                <span class="flex flex-col items-start space-y-1">
                  <span class="font-medium text-sm leading-4">
                    {{ ticket.title }}
                  </span>
                  <chip>{{ Math.random() > 0.5 ? 'Response' : 'Waiting' }}</chip>
                </span>
                <ChevronRightIcon
                  class="ml-4 h-5 w-5 text-gray-400 group-hover:text-gray-500"
                  aria-hidden="true"
                />
              </router-link>
            </li>
          </ul>
        </div>

        <div v-if="ticketsFlattened?.filter(t => !t.open).length > 0">
          <h2 class="text-gray-700 text-lg font-semibold leading-4 pb-2 pt-4">Closed tickets</h2>

          <ul class="border-b border-gray-200 divide-y divide-gray-100">
            <li v-for="ticket in ticketsFlattened?.filter(t => !t.open)" :key="ticket.id">
              <router-link
                :to="`/inboxes/${$route.params.inboxId}/tickets/${ticket.ticket_inbox_id}`"
                class="group flex items-center justify-between py-3 hover:bg-gray-50 sm:px-6"
              >
                <span class="flex items-center truncate space-x-2">
                  <span class="font-medium truncate text-sm leading-4">
                    {{ ticket.title }}
                  </span>
                </span>
                <ChevronRightIcon
                  class="ml-4 h-5 w-5 text-gray-400 group-hover:text-gray-500"
                  aria-hidden="true"
                />
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"
import store from "@/store"
import { mapState, mapActions } from "vuex"
import moment from "moment"

import Chip from "@/components/chip/Chip.vue"
import TicketCard from "@/components/tickets/TicketCard.vue"

import { BellIcon, ChatBubbleLeftRightIcon, ExclamationCircleIcon, InboxStackIcon } from "@heroicons/vue/24/outline"
import { ArrowSmallDownIcon, ArrowSmallUpIcon, ChevronRightIcon, ClockIcon } from '@heroicons/vue/24/solid'
import { ArrowRightIcon, ExclamationTriangleIcon } from "@heroicons/vue/20/solid"

import report from "@/assets/img/svg/report.svg"
import awesome from "@/assets/img/svg/awesome.svg"

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
    ClockIcon,
    ExclamationCircleIcon,
    InboxStackIcon,
    ChatBubbleLeftRightIcon,
    ExclamationTriangleIcon,
    ArrowRightIcon,
    ChevronRightIcon,
    TicketCard
  },
  data: () => ({
    role: "STUDENT",
    labels: [],
    inbox_labels: [],
    report,
    awesome,
    updates: [],
    statsData: {}
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
  setup() {
    return { moment }
  },
  async mounted () {
    const { inboxId } = this.$route.params

    /* Gettings general statistics. */
    const statsResponse = await axios.get(`/api/inboxes/${inboxId}/statistics`)
    this.statsData = statsResponse.data
  },
  methods: {
    ...mapActions('onboarding', {
      nextStep: 'next',
      prevStep: 'prev'
    }),
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
      }
    }),
    ...mapState('onboarding', {
      onboarding: (state) => state.status
    })
  }
}
</script>
