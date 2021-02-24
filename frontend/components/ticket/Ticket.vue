<template>
  <div v-if="ticket" class="min-h-full flex flex-1 flex-col">
    <div class="lg:h-full flex-1 flex flex-col-reverse items-stretch lg:flex-row w-full">
      <div class="max-w-screen lg:max-w-sm bg-gray-100 md:border-r border-t lg:border-t-0 space-y-2 pb-4">
        <!-- Ticket Author -->
        <div class="p-6 flex space-x-4 border-b">
          <img class="h-12 w-12 rounded-full" :src="ticket.author.avatar_url" alt="User image">
          <div class="flex flex-col">
            <span class="text-lg font-bold">
              {{ ticket.author.first_name }} {{ ticket.author.last_name }}
            </span>
            <span v-if="ticket.author_role" class="text-sm">{{ ticket.author_role.label }}</span>
          </div>
        </div>

        <!-- Recent question -->
        <recent-questions :author="ticket.author" :inbox_id="ticket.inbox" class="mx-4"
                          v-if="is_staff"/>

        <!-- Sharing -->
        <div class="px-4">
          <edit-share-with :errors="errors" :inbox_id="ticket.inbox" :shared_with="ticket.shared_with"
                           :author="ticket.author" v-on:input="updateSharedWith"
                           :can_share="canShare"></edit-share-with>
        </div>

        <!-- Labels -->
        <div class="px-4">
          <h4 class="block text-gray-800 font-semibold mb-2">Labels</h4>
          <error :key="error" :message="error" v-for="error in errors.labels"></error>
          <div class="flex flex-wrap mb-2" v-if="labels.length > 0">
            <chip :background="label.color" :key="label.id" class="mr-1 mb-1" v-for="label in labels">
              {{ label.name }}
            </chip>
          </div>
          <div class="flex flex-wrap mb-2" v-else>
            No labels selected
          </div>
          <label-dropdown :selected="labels" :values="inbox.labels" v-if="inbox && canShare" v-model="labels"
                          v-on:input="updateLabels"/>
        </div>

        <!-- Assignee -->
        <div class="px-4" v-if="is_staff">
          <h4 class="font-semibold text-gray-800 mb-2">Assignee</h4>
          <user-dropdown :assignee="ticket.assignee" :staff="staff" v-if="staff" v-on:input="updateAssignee"/>
        </div>

        <!-- Participants -->
        <div class="px-4">
          <h4 class="font-semibold text-gray-800 mb-2">Participants</h4>
          <avatars :users="ticket.participants"/>
        </div>
      </div>

      <div class="relative h-full flex-grow">
        <div class="m-4 mt-2 xl:flex xl:items-center xl:justify-between">
          <div class="flex-1 min-w-0">
            <router-link :to="`/inboxes/${ticket.inbox}/tickets`"
                         class="text-xs text-gray-700 hover:underline cursor-pointer">
              <i class="fa fa-arrow-left mr-2"></i>
              {{ inbox ? inbox.name : '' }}
            </router-link>
            <h2 class="text-2xl font-bold leading-7 text-gray-900 xl:text-3xl xl:leading-9" v-if="!editTitleActive">
              #{{ ticket.ticket_inbox_id }} - {{ ticket.title }}
            </h2>
            <h2 class="text-2xl font-bold leading-7 text-gray-900 xl:text-3xl xl:leading-9" v-if="editTitleActive">
              #{{ ticket.ticket_inbox_id }} - <input v-model="ticket.title"
                                                     class="w-5/6 bg-gray-100 px-2 rounded-md border-2 ">
            </h2>
            <error :key="error" :message="error" v-for="error in errors.title"></error>
            <div class="flex flex-row flex-wrap space-x-4 sm:space-x-6">
              <div class="mt-2 flex items-center text-sm leading-5 text-gray-500" title="Ticket Status">
                <i
                        class="fa mr-1"
                        :class="{ 'fa-envelope-open': ticket.status === 'PNDG' || ticket.status === 'ASGD', 'fa-envelope': ticket.status === 'ANSD' || ticket.status === 'CLSD' }"
                ></i>
                {{ status[ticket.status] }}
              </div>
              <div class="mt-2 flex items-center text-sm leading-5 text-gray-500" title="Assigned to"
                   v-if="ticket.assignee && ticket.assignee.username">
                <i class="fa fa-user mr-1"></i>
                {{ ticket.assignee.first_name }} {{ ticket.assignee.last_name }}
              </div>
              <div class="mt-2 flex items-center text-sm leading-5 text-gray-500" title="Created at">
                <i class="fa fa-calendar mr-1"></i>
                {{ date(this.ticket.date_created) }}
              </div>
            </div>
          </div>
          <div class="mt-5 flex xl:mt-0 xl:ml-4 space-x-4">
            <button type="button" @click="editTitleActive = true" v-if="!editTitleActive"
                    class="inline-flex items-center px-4 py-2 border border-transparent text-sm leading-5 font-medium rounded-md text-black bg-gray-100 hover:bg-gray-300 focus:outline-none focus:shadow-outline-orange focus:border-orange-700 active:bg-orange-700 transition duration-150 ease-in-out">
              <i class="fa fa-pencil mr-2"></i>
              Edit title
            </button>
            <button type="button" @click="saveTitle" v-if="editTitleActive"
                    class="inline-flex items-center px-4 py-2 border border-transparent text-sm leading-5 font-medium rounded-md text-black bg-gray-100 hover:bg-gray-300 focus:outline-none focus:shadow-outline-orange focus:border-orange-700 active:bg-orange-700 transition duration-150 ease-in-out">
              <i class="fa fa-floppy-o mr-2"></i>
              Save
            </button>
            <span v-if="ticket.status !== 'CLSD'" class="shadow-sm rounded-md">
              <button type="button" @click="closeTicket"
                      class="inline-flex items-center px-4 py-2 border border-transparent text-sm leading-5 font-medium rounded-md text-white bg-primary hover:bg-orange-500 focus:outline-none focus:shadow-outline-orange focus:border-orange-700 active:bg-orange-700 transition duration-150 ease-in-out">
                <i class="fa fa-archive mr-2"></i>
                Close Ticket
              </button>
            </span>
            <span v-if="is_staff && ticket.status === 'CLSD'" class="shadow-sm rounded-md">
              <button type="button" @click="openTicket"
                      class="inline-flex items-center px-4 py-2 border border-transparent text-sm leading-5 font-medium rounded-md text-white bg-primary hover:bg-orange-500 focus:outline-none focus:shadow-outline-orange focus:border-orange-700 active:bg-orange-700 transition duration-150 ease-in-out">
                <i class="fa fa-envelope-open-o mr-2"></i>
                Reopen Ticket
              </button>
            </span>
          </div>
        </div>
        <div class="flex flex-col">
          <ul class="flex border-b mb-2 text-sm">
            <tab :active="activeTab === 'external'" @click="activeTab = 'external'" title="Question"
                 :badge="replies.length + 1"/>
            <tab :active="activeTab === 'internal'" @click="activeTab = 'internal'" title="Staff discussion"
                 :badge="comments.length" v-if="is_staff"/>
            <tab :active="activeTab === 'attachments'" @click="activeTab = 'attachments'" title="Attachments"
                 :badge="ticket.attachments.length"/>
          </ul>

          <div class="lg:container">
            <external-tab v-show="ticket && user && replies && events && activeTab === 'external'" :ticket="ticket"
                          :replies="replies" :events="events" v-on:post="onReplyPost" :user="user"/>
            <internal-tab v-show="ticket && user && comments && is_staff && activeTab === 'internal'" :ticket="ticket"
                          :comments="comments" v-on:post="onCommentPost" :user="user" :staff="staff_excluding_self"/>
            <attachments-tab v-if="ticket && activeTab === 'attachments'" :ticket="ticket" @uploaded="updateTicket"
                             :is_staff="is_staff" :user="user"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import Comment from "./Comment";
  import Avatar from "../elements/Avatar";
  import axios from "axios";
  import 'codemirror/lib/codemirror.css';
  import VueTribute from 'vue-tribute';

  import Mention from "../elements/mention/Mention";
  import Tab from "../elements/Tab"
  import ExternalTab from "./ExternalTab";
  import InternalTab from "./InternalTab";
  import Card from '../elements/card/Card'
  import AttachmentsTab from "./AttachmentsTab";
  import Avatars from "../elements/Avatars";
  import EditShareWith from "./EditShareWith";
  import UserDropdown from "../elements/dropdown/UserDropdown";
  import LabelDropdown from "../elements/dropdown/LabelDropdown";
  import RecentQuestions from "./RecentQuestions";
  import {calendarDate} from "../../utils";
  import Error from "../elements/message/Error";

  export default {
    components: {
      Error,
      EditShareWith,
      Avatars,
      AttachmentsTab,
      InternalTab,
      ExternalTab,
      Mention,
      UserDropdown,
      LabelDropdown,
      Avatar,
      Comment,
      VueTribute,
      RecentQuestions,
      Tab,
      Card
    },
    data() {
      return {
        inbox: null,
        ticket: null,
        editTitleActive: false,
        replies: [],
        labels: [],
        comments: [],
        staff: [],
        events: [],
        activeTab: 'external',
        user: {},
        role: "",
        errors: [],
        status: {
          PNDG: 'Pending',
          ASGD: 'Assigned',
          ANSD: 'Awaiting response',
          CLSD: 'Closed'
        }
      }
    },
    mounted() {
      this.loadTicket()
    },
    beforeRouteUpdate(to, from, next) {
      if (from.params.ticketInboxId !== to.params.ticketInboxId) {
        next()
        this.loadTicket()
      }
    },
    computed: {
      is_staff: function () {
        return this.isStaff()
      },
      staff_excluding_self: function () {
        if (!this.staff || !this.user) return [];

        return this.staff.filter(user => user.id !== this.user.id)
      },
      canShare: function () {
        return this.is_staff || (this.user && this.ticket.author.id === this.user.id)
      }
    },
    methods: {
      loadTicket: function () {
        let formData = {
          "ticket": true,
          "role": true,
          "me": true,
          "inbox": true,
          "staff": true,
          "comments": true,
          "replies": true,
          "events": true
        };


        axios.get(this.getTicketUrl(), {params: formData}).then(response => {
          this.ticket = response.data.ticket;
          this.labels = response.data.ticket.labels;
          this.user = response.data.me;
          this.role = response.data.role;
          this.inbox = response.data.inbox;
          this.events = response.data.events;
          this.replies = response.data.replies;

          if (this.isStaff()) {
            this.staff = response.data.staff;
            this.comments = response.data.comments;
          }
        });
      },
      date: calendarDate,
      isStaff: function () {
        return (this.role && (this.role === 'AGENT' || this.role === 'MANAGER')) || (this.user && this.user.is_superuser)
      },
      getTicketUrl: function () {
        const inboxId = this.$route.params.inboxId
        const ticketInboxId = this.$route.params.ticketInboxId

        return `/api/inboxes/${inboxId}/tickets/${ticketInboxId}`
      },
      onReplyPost: function () {
        let data = {
          "ticket": true,
          "replies": true,
          "events": true,
        };

        axios.get(this.getTicketUrl(), {params: data}).then(response => {
          this.replies = response.data.replies;
          this.events = response.data.events;
          this.ticket = response.data.ticket;
        });
      },
      onCommentPost: function () {
        let data = {
          "ticket": true,
          "comments": true,
        };

        axios.get(this.getTicketUrl(), {params: data}).then(response => {
          this.ticket = response.data.ticket;
          this.comments = response.data.comments;
        });

      },
      closeTicket: function () {
        let data = {
          "events": true
        };

        this.ticket.status = "CLSD";
        axios.patch(this.getTicketUrl() + "/status/close").then(_ => {
          return axios.get(this.getTicketUrl(), {params: data})
        }).then(response => {
          this.events = response.data.events;
        });

      },
      openTicket: function () {
        let data = {
          "ticket": true
        };

        axios.patch(this.getTicketUrl() + "/status/open").then(_ => {
          return axios.get(this.getTicketUrl(), {params: data})
        }).then(response => {
          this.ticket.status = response.data.ticket.status;
        });
      },
      updateSharedWith() {
        let formData = new FormData();
        this.ticket.shared_with.forEach(shared_with => formData.append("shared_with", shared_with.id));

        axios.put(this.getTicketUrl() + "/shared", formData).then(_ => {
          return axios.get(this.getTicketUrl(), {params: {"ticket": true}})
        }).then(response => {
          this.ticket = response.data.ticket;
        }).catch(error => {
          this.errors = error.response.data
        })
      }
      ,
      updateAssignee() {
        let data = {
          "ticket": true,
          "events": true
        };

        axios.get(this.getTicketUrl(), {params: data}).then(response => {
          this.ticket = response.data.ticket;
          this.events = response.data.events;
        });
      }
      ,
      updateLabels() {
        let data = {
          "events": true
        };

        const inboxId = this.$route.params.inboxId
        const ticketInboxId = this.$route.params.ticketInboxId

        axios.put(this.getTicketUrl() + "/labels",
            {
              "labels": this.labels.map(label => label.id)
            }).then(_ => {
          return axios.get(this.getTicketUrl(), {params: data})
        }).then(response => {
          this.events = response.data.events;
        }).catch(error => {
          this.errors = error.response.data
        });
      }
      ,
      updateTicket() {
        let data = {
          "ticket": true
        };

        axios.get(this.getTicketUrl(), {params: data}).then(response => {
          this.ticket = response.data.ticket;
        })
      },
      saveTitle() {
        let data = {
          "title": this.ticket.title
        };

        this.editTitleActive = false
        axios.put(this.getTicketUrl() + "/title", data).then(response => {
          this.ticket.title = response.data.title
        }).catch(error => {
          this.errors = error.response.data
        })
      }
    }
  }
</script>
