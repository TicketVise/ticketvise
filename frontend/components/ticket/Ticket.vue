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
            <span v-if="ticket.author.role" class="text-sm">{{ ticket.author.role.label }}</span>
          </div>
        </div>

        <!-- Recent question -->
        <recent-questions :author="ticket.author" :inbox_id="ticket.inbox" class="mx-4" v-if="is_staff"/>

        <!-- Sharing -->
        <div class="px-4" v-if="canShare">
          <edit-share-with :errors="errors" :inbox_id="ticket.inbox" :shared_with="shared_with"
            v-on:input="updateSharedWith"></edit-share-with>
        </div>

        <!-- Labels -->
        <div class="px-4">
          <h4 class="block text-gray-800 font-semibold mb-2">Labels</h4>
          <error :key="error" :message="error" v-for="error in this.errors.labels"></error>
          <div class="flex flex-wrap mb-2" v-if="labels.length > 0">
            <chip :background="label.color" :key="label.id" class="mr-1 mb-1" v-for="label in labels">
              {{ label.name }}
            </chip>
          </div>
          <div class="flex flex-wrap mb-2" v-else>
            No labels selected
          </div>
            <label-dropdown :selected="labels" :values="inbox.labels" v-if="canShare" v-model="labels"
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
            <a :href="`/inboxes/${ticket.inbox}/tickets`" class="text-xs text-gray-700 hover:underline cursor-pointer">
              <i class="fa fa-arrow-left mr-2"></i>
              {{ inbox ? inbox.name : '' }}
            </a>
            <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:leading-9 sm:truncate">
              #{{ ticket.ticket_inbox_id }} - {{ ticket.title }}
            </h2>
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
                {{ date }}
              </div>
            </div>
          </div>
          <div class="mt-5 flex xl:mt-0 xl:ml-4 space-x-4">
            <span v-if="is_staff && ticket.status !== 'CLSD'" class="shadow-sm rounded-md">
              <button type="button" @click="closeTicket"
                      class="inline-flex items-center px-4 py-2 border border-transparent text-sm leading-5 font-medium rounded-md text-white bg-primary hover:bg-orange-500 focus:outline-none focus:shadow-outline-orange focus:border-orange-700 active:bg-orange-700 transition duration-150 ease-in-out">
                <i class="fa fa-archive mr-2"></i>
                Close Ticket
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

          <external-tab v-if="ticket && user && replies && activeTab === 'external'" :ticket="ticket" :replies="replies"
                        v-on:post="onReplyPost" :user="user"/>
          <internal-tab v-if="ticket && user && comments && is_staff && activeTab === 'internal'" :ticket="ticket"
                        :comments="comments"
                        v-on:post="onCommentPost" :user="user" :staff="staff_excluding_self"/>
          <attachments-tab v-if="ticket && activeTab === 'attachments'" :ticket="ticket" @uploaded="updateTicket"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import Comment from "./Comment";
  import Avatar from "../elements/Avatar";
  import axios from "axios";
  import moment from "moment"
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

  export default {
    components: {
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
        replies: [],
        labels: [],
        comments: [],
        staff: [],
        activeTab: 'external',
        user: null,
        role: "",
        shared_with: [],
        errors: [],
        status: {
          PNDG: 'Pending',
          ASGD: 'Assigned',
          ANSD: 'Answered',
          CLSD: 'Closed'
        }
      }
    },
    created() {
      axios.get("/api" + window.location.pathname).then(response => {
        this.ticket = response.data;
        this.labels = response.data.labels;

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

        axios.put("/api/notifications/read" + window.location.pathname).then(_ => {
        });

        axios.get("/api/me").then(response => {
          this.user = response.data;

          axios.get("/api/inboxes/" + this.ticket.inbox + "/role").then(response => {
            this.role = response.data;

            if (this.isStaff()) {
              axios.get("/api" + window.location.pathname + "/comments").then(response => {
                this.comments = response.data;
              });

              axios.get("/api/inboxes/" + this.ticket.inbox + "/staff").then(response => {
                this.staff = response.data;
              });
            }
            if (this.isStaff() || (this.ticket.author && this.ticket.author.id === this.user.id)) {
              axios.get("/api" + window.location.pathname + "/shared").then(response => {
                this.shared_with = response.data.shared_with;
              });
            }
          });
          axios.get("/api/inboxes/" + this.ticket.inbox + "/users/" + this.ticket.author.id + "/roles").then(response => {
            this.$set(this.ticket.author, 'role', response.data)
          })
        });
        axios.get("/api/inboxes/" + this.ticket.inbox).then(response => {
          this.inbox = response.data
        })
      });
      axios.get("/api" + window.location.pathname + "/replies").then(response => {
        this.replies = response.data;
      });
    },
    computed: {
      date: function () {
        return moment.parseZone(this.ticket.date_created).fromNow()
      },
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
      isStaff: function () {
        return this.role && (this.role.key === 'AGENT' || this.role.key === 'MANAGER')
      },
      onReplyPost: function () {
        axios.get("/api" + window.location.pathname + "/replies").then(response => {
          this.replies = response.data;
        });

        axios.get("/api" + window.location.pathname).then(response => {
          this.ticket = response.data;
        });
      },
      onCommentPost: function () {
        axios.get("/api" + window.location.pathname + "/comments").then(response => {
          this.comments = response.data;
        });

        axios.get("/api" + window.location.pathname).then(response => {
          this.ticket = response.data;
        });
      },
      closeTicket: function () {
        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

        this.ticket.status = "CLSD";
        axios.put("/api" + window.location.pathname + "/status", {
          "status": this.ticket.status
        }).then(_ => {
        })
      },
      updateSharedWith() {
        let formData = new FormData();
        this.shared_with.forEach(shared_with => formData.append("shared_with", shared_with.id));

        axios.defaults.xsrfCookieName = "csrftoken";
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

        axios.put("/api" + window.location.pathname + "/shared", formData).then(_ => {

        }).catch(error => {
          this.errors = error.response.data
        })
      },
      updateAssignee() {
        axios.get("/api" + window.location.pathname).then(response => {
          this.ticket = response.data;
        })
      },
      updateLabels() {
        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

        axios.put("/api" + window.location.pathname + "/labels",
            {
              "labels": this.labels.map(label => label.id)
            }).then(_ => {

        });
      },
      updateTicket() {
        axios.get("/api" + window.location.pathname).then(response => {
          this.ticket = response.data;
        })
      }
    }
  }
</script>
