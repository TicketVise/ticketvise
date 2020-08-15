<template>
  <div class="container mx-auto my-3">
    <div class="flex flex-col-reverse lg:flex-row lg:space-x-3 mx-3">
      <div v-if="is_staff" class="flex flex-col w-full lg:min-w-1/4 lg:w-1/4 space-y-3">
        <author-card class="hidden lg:block" :author="ticket.author" :inbox_id="ticket.inbox"/>
        <card outlined>
          <edit-label :ticket="ticket" class="p-3 border-b border-gray-400"/>
          <edit-assignee :ticket="ticket" :staff="staff" class="p-3 border-b border-gray-400"/>
          <div class="p-3">
            <h4 class="font-semibold text-gray-800 mb-2">Participants</h4>
            <avatars :users="ticket.participants"/>
          </div>
        </card>
      </div>
      <div class="flex flex-col flex-grow">
        <div class="flex">
          <div class="p-3 flex w-full">
            <div class="flex flex-col flex-grow items-start space-y-1">
              <h1 class="flex font-bold text-xl text-gray-800 items-center">
                <span v-if="ticket.status === 'PNDG'"
                      class="mr-1 py-1 px-1 inline-flex leading-5 font-semibold rounded-full bg-red-200 text-red-700">
                    Pending
                </span>
                <span v-if="ticket.status === 'ASGD'"
                      class="mr-1 py-1 px-1 inline-flex leading-5 font-semibold rounded-full bg-orange-100 text-orange-700">
                    Assigned
                </span>
                <span v-if="ticket.status === 'ANSD'"
                      class="mr-1 py-1 px-1 inline-flex leading-5 font-semibold rounded-full bg-green-200 text-green-700">
                    Answered
                </span>
                <span v-if="ticket.status === 'CLSD'"
                      class="mr-1 py-1 px-1 inline-flex leading-5 font-semibold rounded-full bg-gray-300 text-gray-800">
                    Closed
                </span>
                #{{ ticket.ticket_inbox_id }} - {{ ticket.title }}
              </h1>
              <div>
                <chip class="mr-1" v-for="label in ticket.labels" :key="label.id"
                      :background="label.color">
                  {{ label.name }}
                </chip>
              </div>
              <span class="text-sm text-gray-600">{{ date }}</span>
            </div>
            <div class="flex-shrink w-1/6" v-if="canShare">
              <edit-share-with :shared_with="shared_with" :errors="errors" class="mb-2" :inbox_id="ticket.inbox"
                               v-on:input="updateSharedWith"></edit-share-with>
            </div>
            <div v-if="is_staff">
                        <span v-if="ticket.status !== 'CLSD'" class="sm:ml-3 shadow-sm rounded-md">
                            <button type="button" @click="closeTicket"
                                    class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm leading-5 font-medium rounded-md text-gray-700 bg-white hover:text-gray-500 focus:outline-none focus:shadow-outline-orange focus:border-orange-300 active:text-gray-800 active:bg-gray-50 active:text-gray-800">
                                <i class="fa fa-archive mr-2"></i>
                                Close
                            </button>
                        </span>
            </div>
          </div>

        </div>

        <ul class="flex border-b w-full mb-2">
          <tab :active="activeTab === 'external'" @click="activeTab = 'external'" title="External"
               :badge="replies.length + 1"/>
          <tab :active="activeTab === 'internal'" @click="activeTab = 'internal'" title="Internal"
               :badge="comments.length" v-if="is_staff"/>
          <tab :active="activeTab === 'attachments'" @click="activeTab = 'attachments'" title="Attachments"
               :badge="ticket.attachments.length"/>
        </ul>

        <external-tab v-if="activeTab === 'external'" :ticket="ticket" :replies="replies"
                      v-on:post="onReplyPost" :user="user"/>
        <internal-tab v-if="is_staff && activeTab === 'internal'" :ticket="ticket" :comments="comments"
                      v-on:post="onCommentPost" :user="user" :staff="staff_excluding_self"/>
        <attachments-tab v-if="activeTab === 'attachments'" :ticket="ticket"/>
      </div>
    </div>
  </div>
</template>

<script>
import AuthorCard from "./AuthorCard";
import Comment from "./Comment";
import Avatar from "../elements/Avatar";
import axios from "axios";
import moment from "moment"
import '@toast-ui/editor/dist/toastui-editor-viewer.css';
import 'codemirror/lib/codemirror.css';
import VueTribute from 'vue-tribute';

import '@toast-ui/editor/dist/toastui-editor.css';
import {Editor, Viewer} from '@toast-ui/vue-editor';
import EditLabel from "./EditLabel";
import EditAssignee from "./EditAssignee";
import Mention from "../elements/mention/Mention";
import Tab from "../elements/Tab"
import ExternalTab from "./ExternalTab";
import InternalTab from "./InternalTab";
import Card from '../elements/card/Card'
import AttachmentsTab from "./AttachmentsTab";
import Avatars from "../elements/Avatars";
import EditShareWith from "./EditShareWith";

export default {
  components: {
    EditShareWith,
    Avatars,
    AttachmentsTab,
    InternalTab,
    ExternalTab,
    Mention,
    EditAssignee,
    EditLabel,
    Avatar,
    AuthorCard,
    Comment,
    Viewer,
    editor: Editor,
    VueTribute,
    Tab,
    Card
  },
  data() {
    return {
      ticket: null,
      replies: [],
      comments: [],
      commentEditor: "",
      staff: [],
      activeTab: "external",
      user: null,
      role: null,
      shared_with: [],
      errors: [],
    }
  },
  mounted() {
    axios.get("/api" + window.location.pathname).then(response => {
      this.ticket = response.data;

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
          if (this.isStaff() || this.ticket.author.id === this.user.id) {
            axios.get("/api" + window.location.pathname + "/shared").then(response => {
              this.shared_with = response.data.shared_with;
            });
          }
        })
      });
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
      if (!this.staff || !this.user) {
        return []
      }

      return this.staff.filter(user => user.id !== this.user.id)
    },
    canShare: function () {
      return this.is_staff || this.ticket.author.id === this.user.id
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

      this.ticket.status = "CLSD"
      axios.put("/api" + window.location.pathname + "/status", {
        "status": this.ticket.status
      }).then(_ => {
      })
    },
    updateSharedWith() {
      let formData = new FormData()
      this.shared_with.forEach(shared_with => formData.append("shared_with", shared_with.id))

      axios.defaults.xsrfCookieName = 'csrftoken';
      axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

      axios.put("/api" + window.location.pathname + "/shared", formData).then(response => {

      }).catch(error => {
            this.errors = error.response.data
          }
      )
    }
  }
}
</script>

<style scoped>

</style>
