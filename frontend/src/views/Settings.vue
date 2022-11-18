<template>
  <div class="overflow-y-auto h-full">
    <!-- Tabs -->
    <div class="p-4 sm:p-0 pb-0">
      <div class="sm:hidden">
        <label for="tabs" class="sr-only">Select a tab</label>
        <!-- Use an "onChange" listener to redirect the user to the selected tab URL. -->
        <select id="tabs" name="tabs" @change="switchTab($event.target.value)" class="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm rounded-md">
          <option v-for="tab in tabs" :key="tab.name" :selected="tab.current">
            {{ tab.name }}
          </option>
        </select>
      </div>
      <div class="hidden sm:block">
        <div class="flex items-center border-b border-gray-200">
          <nav class="flex-1 -mb-px flex space-x-6 xl:space-x-8 px-4" aria-label="Tabs">
            <router-link v-for="tab in tabs" :key="tab.name" :aria-current="tab.current ? 'page' : undefined" :to="{ name: 'Settings', params: { inboxId: this.$route.params.inboxId, tab: tab.name.toLowerCase() } }" :class="[tab.current ? 'border-primary text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300', 'cursor-pointer group inline-flex items-center py-4 px-1 border-b-2 font-medium text-sm']">
              <component :is="tab.icon" :class="[tab.current ? 'text-primary' : 'text-gray-400 group-hover:text-gray-500', '-ml-0.5 mr-2 h-5 w-5']" aria-hidden="true" />
              <span>{{ tab.name }}</span>
            </router-link>
          </nav>
        </div>
      </div>
    </div>

    <!-- Pages -->
    <div class="p-4 max-w-4xl mx-auto">
      <form v-if="tabs.find(t => t.name == 'Appearance').current" @submit.prevent="onSave" method="POST">
        <!-- Inbox section -->
        <div>
          <h2 class="text-lg leading-6 font-medium text-gray-900">Inbox</h2>
          <p class="mt-1 text-sm text-gray-500">
            This information is about the inbox and the look and feel of the
            inbox.
          </p>
        </div>

        <div class="mt-6 flex flex-col lg:flex-row">
          <div class="flex-grow space-y-6">
            <div>
              <label
                for="name"
                class="block text-sm font-medium text-gray-700"
              >
                <span class="mr-1">Name</span>
                <span
                  class="inline-flex items-center px-2.5 rounded-md text-sm font-medium bg-gray-100 text-primary"
                >
                  LTI
                </span>
              </label>
              <div class="mt-1 flex">
                <input
                  disabled
                  v-model="inbox.name"
                  type="text"
                  name="name"
                  id="name"
                  autocomplete="name"
                  class="cursor-not-allowed border rounded-md focus:ring-primary focus:border-primary flex-grow block w-full min-w-0 sm:text-sm border-gray-300"
                />
              </div>
            </div>

            <div>
              <label
                for="code"
                class="block text-sm font-medium text-gray-700"
              >
                <span class="mr-1">Code</span>
                <span
                  class="inline-flex items-center px-2.5 rounded-md text-sm font-medium bg-gray-100 text-primary"
                >
                  LTI
                </span>
              </label>
              <div class="mt-1 flex">
                <input
                  disabled
                  v-model="inbox.lti_context_label"
                  type="text"
                  name="code"
                  id="code"
                  autocomplete="name"
                  class="cursor-not-allowed border rounded-md focus:ring-primary focus:border-primary flex-grow block w-full min-w-0 sm:text-sm border-gray-300"
                />
              </div>
            </div>
          </div>

          <div
            class="mt-6 mb-4 flex-grow lg:mt-0 lg:ml-6 lg:flex-grow-0 lg:flex-shrink-0"
          >
            <p class="text-sm font-medium text-gray-700" aria-hidden="true">
              Cover photo
            </p>
            <div class="mt-1 lg:hidden">
              <div class="flex items-center">
                <div
                  class="flex-shrink-0 inline-block rounded-md overflow-hidden h-16 w-20"
                  aria-hidden="true"
                >
                  <img
                    class="rounded-md h-full w-full"
                    :src="im_url || '/img/default-inbox.png'"
                    alt=""
                  />
                </div>
                <div class="ml-5 rounded-md shadow-sm">
                  <div
                    class="group relative border border-gray-300 rounded-md py-2 px-3 flex items-center justify-center hover:bg-gray-50 focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-primary"
                  >
                    <label
                      for="inbox-photo"
                      class="relative text-sm leading-4 font-medium text-gray-700 pointer-events-none"
                    >
                      <span>Change</span>
                      <span class="sr-only"> inbox photo</span>
                    </label>
                    <input
                      @change="onChange"
                      id="inbox-photo"
                      name="inbox-photo"
                      type="file"
                      class="absolute w-full h-full opacity-0 cursor-pointer border-gray-300 rounded-md"
                    />
                  </div>
                </div>
              </div>
            </div>

            <div
              class="hidden relative rounded-md overflow-hidden lg:block"
            >
              <img
                class="relative rounded-md w-64 h-40"
                :src="im_url || '/img/default-inbox.png'"
                alt=""
              />
              <label
                for="inbox-photo"
                class="absolute inset-0 w-full h-full bg-black bg-opacity-75 flex items-center justify-center text-sm font-medium text-white opacity-0 hover:opacity-100 focus-within:opacity-100"
              >
                <span>Change</span>
                <span class="sr-only"> inbox photo</span>
                <input
                  @change="onChange"
                  type="file"
                  id="inbox-photo"
                  name="inbox-photo"
                  class="absolute inset-0 w-full h-full opacity-0 cursor-pointer border-gray-300 rounded-md"
                />
              </label>
            </div>
          </div>
        </div>
        <div class="py-4 flex justify-end space-x-4 border-t">
          <button
            @click="onCancel"
            type="button"
            class="bg-white border border-gray-300 rounded-md shadow-sm py-2 px-4 inline-flex justify-center text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="ml-5 bg-primary border border-transparent rounded-md shadow-sm py-2 px-4 inline-flex justify-center text-sm font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          >
            Save
          </button>
        </div>
      </form>

      <form v-if="tabs.find(t => t.name == 'Tickets').current" @submit.prevent="onSave" method="POST">
        <!-- Privacy section -->
        <div class="divide-y divide-gray-200">
          <div>
            <div>
              <h2 class="text-lg leading-6 font-medium text-gray-900">
                Tickets
              </h2>
              <p class="mt-1 text-sm text-gray-500">
                Some settings regarding the tickets in the inbox.
              </p>
            </div>
            <ul class="mt-2 divide-y divide-gray-200">
              <SwitchGroup
                as="li"
                class="py-4 flex items-center justify-between space-x-2"
              >
                <div class="flex flex-col">
                  <SwitchLabel
                    as="p"
                    class="text-sm font-medium text-gray-900"
                    passive
                  >
                    Assignee visible to students
                  </SwitchLabel>
                  <SwitchDescription class="text-sm text-gray-500">
                    Whether or not to show who is assigned to the ticket.
                  </SwitchDescription>
                </div>
                <Switch
                  v-model="inbox.show_assignee_to_guest"
                  :class="[
                    inbox.show_assignee_to_guest
                      ? 'bg-primary'
                      : 'bg-gray-200',
                    'ml-4 relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary',
                  ]"
                >
                  <span
                    aria-hidden="true"
                    :class="[
                      inbox.show_assignee_to_guest
                        ? 'translate-x-5'
                        : 'translate-x-0',
                      'inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200',
                    ]"
                  />
                </Switch>
              </SwitchGroup>
              <SwitchGroup
                as="li"
                class="py-4 flex items-center justify-between space-x-2"
              >
                <div class="flex flex-col">
                  <SwitchLabel
                    as="p"
                    class="text-sm font-medium text-gray-900"
                    passive
                  >
                    Automatically close tickets
                  </SwitchLabel>
                  <SwitchDescription class="text-sm text-gray-500">
                    Automatically close tickets after some weeks with no
                    activity.
                  </SwitchDescription>
                </div>
                <!-- <select-input v-model="close_answered_weeks" :data="closeTicketsOptions" /> -->
                <Listbox as="div" v-model="close_answered_weeks">
                  <div class="mt-1 relative">
                    <ListboxButton
                      class="relative w-full bg-white border border-gray-300 rounded-md pl-3 pr-10 py-2 text-left cursor-pointer focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary sm:text-sm"
                    >
                      <span class="flex items-center">
                        <span
                          v-if="close_answered_weeks?.color"
                          class="flex-shrink-0 inline-block h-2 w-2 rounded-full mr-3"
                          :style="`background-color: ${close_answered_weeks?.color}`"
                        />
                        <img
                          v-if="close_answered_weeks?.avatar"
                          :src="close_answered_weeks.avatar"
                          alt=""
                          class="flex-shrink-0 h-5 w-5 rounded-full"
                        />
                        <span
                          :class="[
                            close_answered_weeks?.avatar ? 'ml-3' : '',
                            'block truncate',
                          ]"
                          >{{ close_answered_weeks?.name }}</span
                        >
                      </span>
                      <span
                        class="ml-3 absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none"
                      >
                        <ChevronUpDownIcon
                          class="h-5 w-5 text-gray-400"
                          aria-hidden="true"
                        />
                      </span>
                    </ListboxButton>

                    <transition
                      leave-active-class="transition ease-in duration-100"
                      leave-from-class="opacity-100"
                      leave-to-class="opacity-0"
                    >
                      <ListboxOptions
                        class="absolute z-20 mt-1 bg-white shadow-lg max-h-56 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm"
                      >
                        <ListboxOption
                          as="template"
                          v-for="element in closeTicketsOptions"
                          :key="element.value"
                          :value="element"
                          v-slot="{ active, selected }"
                        >
                          <li
                            :class="[
                              active
                                ? 'text-white bg-primary-600'
                                : 'text-gray-900',
                              'cursor-pointer select-none relative py-2 pl-3 pr-9',
                            ]"
                          >
                            <div class="flex items-center">
                              <span
                                v-if="element.color"
                                class="flex-shrink-0 inline-block h-2 w-2 rounded-full mr-3"
                                :style="`background-color: ${element.color}`"
                              />
                              <img
                                v-if="element.avatar"
                                :src="element.avatar"
                                alt=""
                                class="flex-shrink-0 h-6 w-6 rounded-full"
                              />
                              <span
                                :class="[
                                  selected ? 'font-semibold' : 'font-normal',
                                  element.avatar ? 'ml-3' : '',
                                  'block truncate',
                                ]"
                              >
                                {{ element.name }}
                              </span>
                            </div>

                            <span
                              v-if="selected"
                              :class="[
                                active ? 'text-white' : 'text-primary-600',
                                'absolute inset-y-0 right-0 flex items-center pr-4',
                              ]"
                            >
                              <CheckIcon class="h-5 w-5" aria-hidden="true" />
                            </span>
                          </li>
                        </ListboxOption>
                      </ListboxOptions>
                    </transition>
                  </div>
                </Listbox>
              </SwitchGroup>
              <SwitchGroup
                as="li"
                class="py-4 flex items-center justify-between space-x-2"
              >
                <div class="flex flex-col">
                  <SwitchLabel
                    as="p"
                    class="text-sm font-medium text-gray-900"
                    passive
                  >
                    Send alert unanswered tickets
                  </SwitchLabel>
                  <SwitchDescription class="text-sm text-gray-500">
                    Automatically send an alert when a ticket is unanswered
                    after some days.
                  </SwitchDescription>
                </div>
                <!-- <select-input v-model="alert_coordinator_unanswered_days" :data="sendAlertOptions" /> -->
                <Listbox as="div" v-model="alert_coordinator_unanswered_days">
                  <div class="mt-1 relative">
                    <ListboxButton
                      class="relative w-full bg-white border border-gray-300 rounded-md pl-3 pr-10 py-2 text-left cursor-pointer focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary sm:text-sm"
                    >
                      <span class="flex items-center">
                        <span
                          v-if="alert_coordinator_unanswered_days?.color"
                          class="flex-shrink-0 inline-block h-2 w-2 rounded-full mr-3"
                          :style="`background-color: ${alert_coordinator_unanswered_days?.color}`"
                        />
                        <img
                          v-if="alert_coordinator_unanswered_days?.avatar"
                          :src="alert_coordinator_unanswered_days.avatar"
                          alt=""
                          class="flex-shrink-0 h-5 w-5 rounded-full"
                        />
                        <span
                          :class="[
                            alert_coordinator_unanswered_days?.avatar
                              ? 'ml-3'
                              : '',
                            'block truncate',
                          ]"
                          >{{ alert_coordinator_unanswered_days?.name }}</span
                        >
                      </span>
                      <span
                        class="ml-3 absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none"
                      >
                        <ChevronUpDownIcon
                          class="h-5 w-5 text-gray-400"
                          aria-hidden="true"
                        />
                      </span>
                    </ListboxButton>

                    <transition
                      leave-active-class="transition ease-in duration-100"
                      leave-from-class="opacity-100"
                      leave-to-class="opacity-0"
                    >
                      <ListboxOptions
                        class="absolute z-20 mt-1 bg-white shadow-lg max-h-56 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm"
                      >
                        <ListboxOption
                          as="template"
                          v-for="element in sendAlertOptions"
                          :key="element.value"
                          :value="element"
                          v-slot="{ active, selected }"
                        >
                          <li
                            :class="[
                              active
                                ? 'text-white bg-primary-600'
                                : 'text-gray-900',
                              'cursor-pointer select-none relative py-2 pl-3 pr-9',
                            ]"
                          >
                            <div class="flex items-center">
                              <span
                                v-if="element.color"
                                class="flex-shrink-0 inline-block h-2 w-2 rounded-full mr-3"
                                :style="`background-color: ${element.color}`"
                              />
                              <img
                                v-if="element.avatar"
                                :src="element.avatar"
                                alt=""
                                class="flex-shrink-0 h-6 w-6 rounded-full"
                              />
                              <span
                                :class="[
                                  selected ? 'font-semibold' : 'font-normal',
                                  element.avatar ? 'ml-3' : '',
                                  'block truncate',
                                ]"
                              >
                                {{ element.name }}
                              </span>
                            </div>

                            <span
                              v-if="selected"
                              :class="[
                                active ? 'text-white' : 'text-primary-600',
                                'absolute inset-y-0 right-0 flex items-center pr-4',
                              ]"
                            >
                              <CheckIcon class="h-5 w-5" aria-hidden="true" />
                            </span>
                          </li>
                        </ListboxOption>
                      </ListboxOptions>
                    </transition>
                  </div>
                </Listbox>
              </SwitchGroup>
            </ul>
          </div>
          <div class="py-4 flex justify-end space-x-4">
            <button
              @click="onCancel"
              type="button"
              class="bg-white border border-gray-300 rounded-md shadow-sm py-2 px-4 inline-flex justify-center text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="ml-5 bg-primary border border-transparent rounded-md shadow-sm py-2 px-4 inline-flex justify-center text-sm font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
            >
              Save
            </button>
          </div>
        </div>
      </form>
      
      <div v-if="tabs.find(t => t.name == 'Labels').current">
        <SettingsLabels />
      </div>
      
      <div v-if="tabs.find(t => t.name == 'Automation').current">
        <SettingsAutomation />
      </div>
      
      <div v-if="tabs.find(t => t.name == 'Users').current">
        <!-- <SettingsUsers /> -->
      </div>

      <div v-if="tabs.find(t => t.name == 'Intelligence').current">
        <h2 class="text-lg leading-6 font-medium text-gray-900">Context</h2>
        <p class="mt-1 text-sm text-gray-500">
          You can give your inbox context material which will be used to search for answers within those material before a ticket gets created. This way some questions can be answered without creating a ticket.
        </p>

        <label for="attachments" class="block text-sm font-medium text-gray-700 mt-4">
          Files
        </label>
        <div v-if="documents.length > 0" class="w-full grid grid-cols-1 sm:grid-cols-2 gap-4 mt-1">
          <attachment v-for="(document, index) in documents" :key="index" :attachment="document"
                      @remove="$emit('uploaded')" show-delete/>
        </div>
        <div class="flex flex-col justify-center w-full mt-2">
          <Error class="mb-2" v-for="error in errors.attachments" :key="error" :message="error" />
          <FileUpload ref="upload" v-on:input="setFiles" class="w-full" />
        </div>
      </div>

      <div v-if="tabs.find(t => t.name == 'Email').current">
        <Email :connected="inbox.is_email_setup" />
      </div>
    </div>
  </div>

  <!-- Global notification live region, render this permanently at the end of the document -->
  <div
    aria-live="assertive"
    class="fixed inset-0 bottom-16 flex items-end px-4 py-6 pointer-events-none sm:p-6 sm:items-start"
  >
    <div class="w-full flex flex-col items-center space-y-4 sm:items-end">
      <!-- Notification panel, dynamically insert this into the live region when it needs to be displayed -->
      <transition
        enter-active-class="transform ease-out duration-300 transition"
        enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
        enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
        leave-active-class="transition ease-in duration-100"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div
          v-if="show_saved_notification"
          class="max-w-sm w-full bg-white shadow-lg rounded-lg pointer-events-auto ring-1 ring-black ring-opacity-5 overflow-hidden"
        >
          <div class="p-4">
            <div class="flex items-start">
              <div class="flex-shrink-0">
                <CheckCircleIcon
                  class="h-6 w-6 text-green-400"
                  aria-hidden="true"
                />
              </div>
              <div class="ml-3 w-0 flex-1 pt-0.5">
                <p class="text-sm font-medium text-gray-900">
                  Successfully saved!
                </p>
                <p class="mt-1 text-sm text-gray-500">
                  The settings have been saved.
                </p>
              </div>
              <div class="ml-4 flex-shrink-0 flex">
                <button
                  @click="show_saved_notification = false"
                  class="bg-white rounded-md inline-flex text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
                >
                  <span class="sr-only">Close</span>
                  <XMarkIcon class="h-5 w-5" aria-hidden="true" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import axios from "axios"
import Error from '@/components/inputs/Error.vue'
import FileUpload from '@/components/inputs/FileInput.vue'
import Attachment from '@/components/tickets/Attachment.vue'

import SettingsLabels from '@/components/settings/SettingsLabels.vue'
import SettingsAutomation from '@/components/settings/SettingsAutomation.vue'
// import SettingsUsers from '@/components/settings/SettingsUsers.vue'

import {
  Listbox,
  ListboxButton,
  ListboxOption,
  ListboxOptions,
  Switch,
  SwitchDescription,
  SwitchGroup,
  SwitchLabel,
} from "@headlessui/vue";
import {
  CheckIcon,
  ChevronUpDownIcon,
  XMarkIcon,
} from "@heroicons/vue/24/solid";
import { CheckCircleIcon } from "@heroicons/vue/24/outline";
import Email from "../components/settings/Email.vue";

const closeTicketsOptions = [
  { name: "Disabled", value: 0 },
  { name: "1 week", value: 1 },
  { name: "2 weeks", value: 2 },
  { name: "3 weeks", value: 3 },
  { name: "4 weeks", value: 4 },
];
const sendAlertOptions = [
  { name: "Disabled", value: 0 },
  { name: "1 day", value: 1 },
  { name: "2 days", value: 2 },
  { name: "3 days", value: 3 },
  { name: "4 days", value: 4 },
  { name: "5 days", value: 5 },
  { name: "6 days", value: 6 },
  { name: "7 days", value: 7 },
];

export default {
  name: "InboxSettings",
  components: {
    Attachment,
    Error,
    FileUpload,
    Switch,
    SwitchDescription,
    SwitchGroup,
    SwitchLabel,
    // SelectInput,
    Listbox,
    ListboxButton,
    ListboxOption,
    ListboxOptions,
    CheckIcon,
    ChevronUpDownIcon,
    CheckCircleIcon,
    XMarkIcon,
    Email,
    SettingsLabels,
    SettingsAutomation,
    // SettingsUsers
  },
  data() {
    return {
      inbox: {},
      im_url: "",
      staff: [],
      scheduling_options: [],
      errors: [],
      documents: [],
      files: [],
      saved: false,
      user: this.$store.state.user,
      close_answered_weeks: null,
      alert_coordinator_unanswered_days: null,
      show_saved_notification: false,
      tabs: [
        { name: 'Appearance', current: true },
        { name: 'Tickets', current: false },
        { name: 'Labels', current: false },
        { name: 'Automation', current: false },
        { name: 'Intelligence', current: false },
        { name: 'Users', current: false },
        { name: 'Email', current: false }
      ]
    }
  },
  setup() {
    return {
      closeTicketsOptions,
      sendAlertOptions,
    };
  },
  created() {
    axios
      .get(`/api/inboxes/${this.$route.params.inboxId}/settings`)
      .then((response) => {
        this.inbox = response.data.inbox;
        this.staff = response.data.staff;
        this.scheduling_options = response.data.scheduling_options;
        this.im_url = this.inbox.image;
        this.close_answered_weeks =
          this.closeTicketsOptions[this.inbox.close_answered_weeks];
        this.alert_coordinator_unanswered_days =
          this.sendAlertOptions[this.inbox.alert_coordinator_unanswered_days];
      });

    if (this.$route.params.tab) {
      this.tabs.forEach((t) => (t.current = false))
      this.tabs.find((t) => t.name.toLowerCase() === this.$route.params.tab.toLowerCase()).current = true
    }
  },
  mounted () {
    this.getDocuments()
  },
  methods: {
    onSave() {
      axios.defaults.xsrfCookieName = "csrftoken";
      axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

      const formData = new FormData();

      for (const key in this.inbox) {
        if (key === "fixed_scheduling_assignee") continue;
        if (key !== "image") {
          formData.append(key, this.inbox[key]);
        } else if (this.inbox[key] !== this.im_url) {
          formData.append(key, this.inbox[key]);
        }
      }
      formData.append(
        "close_answered_weeks",
        this.close_answered_weeks?.value || 0
      );
      formData.append(
        "alert_coordinator_unanswered_days",
        this.alert_coordinator_unanswered_days?.value || 0
      );
      const config = {
        headers: { "content-type": "multipart/form-data" },
      };

      axios
        .put(
          `/api/inboxes/${this.$route.params.inboxId}/settings`,
          formData,
          config
        )
        .then((response) => {
          this.errors = [];
          this.saved = true;
          this.inbox = response.data;
          this.show_saved_notification = true;
        })
        .catch((error) => {
          this.saved = false;
          this.errors = error.response.data;
        });
    },
    onCancel() {
      window.history.back();
    },
    onChange(event) {
      if (event) {
        this.inbox.image = event.target.files[0];
      }
      const reader = new FileReader()
      reader.onload = e => {
        this.im_url = e.target.result
      }
      reader.readAsDataURL(this.inbox.image)
    },
    uploadFiles () {
      const formData = new FormData()
      const { inboxId } = this.$route.params

      this.files.forEach(file => formData.append('files', file))

      axios.post(`/api/inboxes/${inboxId}/intelligence/material`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then(() => {
        this.$refs.upload.clear()
      }).catch(error => {
        if (error.response && error.response.status === 413)
          this.errors.attachments = ['Filesize too large, max filesize is 25MB.']
        this.$refs.upload.clear()
      })
    },
    setFiles (files) {
      this.files = files
      this.uploadFiles()
      this.getDocuments()
    },
    getDocuments () {
      axios.get(`/api/inboxes/${this.$route.params.inboxId}/intelligence/material`).then(response => {
        this.documents = response.data
      })
    },
    switchTab(name) {
      this.$router.push({ name: 'Settings', params: { inboxId: this.$route.params.inboxId, tab: name.toLowerCase() } })
    }
  }
}
</script>
