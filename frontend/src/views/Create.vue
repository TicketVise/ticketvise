<template>
  <div class="w-full h-full overflow-y-auto pb-16">
    <div class="w-full max-w-screen-lg mx-auto p-4">
      <form @submit.prevent="submit" autocomplete="off">
        <div class="space-y-6">
          <div>
            <h1 class="text-xl leading-6 font-medium text-gray-900">
              Create a new ticket
            </h1>
            <p class="mt-1 text-sm text-gray-500">
              Let’s get started by filling in the information below to create
              your new ticket.
            </p>
          </div>

          <!-- Title of the ticket. -->
          <div>
            <label
              for="project-name"
              class="block text-sm font-medium text-gray-700"
            >
              Title
            </label>
            <div class="relative mt-1">
              <input
                v-model="title"
                type="text"
                name="project-name"
                id="project-name"
                class="block w-full sm:text-sm rounded-md"
                :class="
                  errors.content
                    ? 'border-red-300 text-red-900 placeholder-red-300 focus:ring-red-500 focus:border-red-500'
                    : 'focus:ring-primary focus:border-primary border-gray-300'
                "
                placeholder="Short and concise title for your ticket"
              />
              <div
                v-if="errors.title"
                class="absolute inset-y-0 right-0 items-center pr-3 flex pointer-events-none"
              >
                <ExclamationCircleIcon
                  class="h-5 w-5 text-red-500"
                  aria-hidden="true"
                />
              </div>
            </div>
            <p
              v-if="errors.title"
              class="mt-2 text-sm text-red-600"
              id="email-error"
            >
              {{ errors.title[0] }}
            </p>
          </div>

          <!-- Description of the ticket. -->
          <div>
            <label
              for="content"
              class="block text-sm font-medium text-gray-700"
            >
              Content
            </label>
            <div class="relative mt-1">
              <TicketInput
                v-model="content"
                :class="
                  errors.content
                    ? 'border-red-300 text-red-900 placeholder-red-300 focus:ring-red-500 focus:border-red-500'
                    : 'focus:ring-primary focus:border-primary border-gray-300'
                "
              />
              <div
                v-if="errors.content"
                class="absolute inset-y-0 right-0 top-2 pr-3 flex pointer-events-none"
              >
                <ExclamationCircleIcon
                  class="h-5 w-5 text-red-500"
                  aria-hidden="true"
                />
              </div>
            </div>
            <p
              v-if="errors.content"
              class="mt-2 text-sm text-red-600"
              id="email-error"
            >
              {{ errors.content[0] }}
            </p>
          </div>

          <!-- Automatically search for an answer. -->
          <div v-if="ai.prefetchingAnswers.active">
            <label for="content" class="relative block text-sm font-medium text-gray-700">
              Automatic Answer
            </label>
            <div class="rounded-md bg-blue-50 p-4 my-2">
              <div class="flex">
                <div class="flex-shrink-0">
                  <InformationCircleIcon class="h-5 w-5 text-blue-400" aria-hidden="true" />
                </div>
                <div class="ml-3 flex-1 md:flex md:justify-between">
                  <p class="text-sm text-blue-700">We are developing a system which looks for answers within the material from this course. After you have filled in your question, please click the button below to let the system prefetch an answers to your question. If it does not answer your question, you can still just submit your ticket.</p>
                </div>
              </div>
            </div>
            <div v-if="ai.prefetchingAnswers.response" class="mt-1">
              <div class="font-semibold">Answer:</div>
              <span class="text-sm italic">{{ ai.prefetchingAnswers.response.answer }}</span>
              <div class="text-sm mt-2">We are <strong>{{ parseInt(ai.prefetchingAnswers.response.score * 100) }}%</strong> sure about the answer which we found on page <strong>{{ ai.prefetchingAnswers.response.page }}</strong> of the following file:</div>
              <Attachment class="w-2/3" v-if="ai.prefetchingAnswers.response?.file" :show-delete="false" :attachment="{ file: ai.prefetchingAnswers.response.file, id: null }" />
            </div>
            <div class="mt-2">
              <button :disabled="!content" v-if="!ai.prefetchingAnswers.loading" @click="prefetchAnswer" type="button" :class="['inline-flex items-center px-4 py-2 font-semibold leading-6 text-sm shadow rounded-md transition ease-in-out duration-150', content ? 'text-white bg-primary hover:bg-primary-400' : 'text-gray-500 bg-gray-100']">
                <svg xmlns="http://www.w3.org/2000/svg" class="-ml-1 mr-3 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <span> Find an answer </span>
              </button>
              <button v-else type="button" class="inline-flex items-center px-4 py-2 font-semibold leading-6 text-sm shadow rounded-md text-white bg-primary hover:bg-primary-400 transition ease-in-out duration-150 cursor-not-allowed" disabled="">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Looking through the files...
              </button>
            </div>
          </div>

          <!-- The labels of the ticket. -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Labels
            </label>
            <label-dropdown
              :selected="labels"
              :values="inbox?.labels || []"
              v-model="labels"
            />
          </div>

          <!-- This privacy setting for ticket. -->
          <RadioGroup v-model="privacy">
            <RadioGroupLabel class="text-sm font-medium text-gray-700">
              Privacy
            </RadioGroupLabel>

            <div class="mt-1 bg-white rounded-md -space-y-px">
              <RadioGroupOption
                as="template"
                v-for="(setting, settingIdx) in settings"
                :key="setting.key"
                :value="setting"
                v-slot="{ checked, active }"
              >
                <div
                  :class="[
                    settingIdx === 0 ? 'rounded-tl-md rounded-tr-md' : '',
                    settingIdx === settings.length - 1
                      ? 'rounded-bl-md rounded-br-md'
                      : '',
                    checked
                      ? 'bg-primary-50 border-primary-200 z-10'
                      : 'border-gray-200',
                    'relative border p-4 flex cursor-pointer focus:outline-none',
                  ]"
                >
                  <span
                    :class="[
                      checked
                        ? 'bg-primary-600 border-transparent'
                        : 'bg-white border-gray-300',
                      active ? 'ring-2 ring-offset-2 ring-primary' : '',
                      'h-4 w-4 mt-0.5 cursor-pointer rounded-full border flex items-center justify-center',
                    ]"
                    aria-hidden="true"
                  >
                    <span class="rounded-full bg-white w-1.5 h-1.5" />
                  </span>
                  <div class="ml-3 flex flex-col">
                    <RadioGroupLabel
                      as="span"
                      class="text-gray-900 block text-sm font-medium"
                    >
                      {{ setting.name }}
                    </RadioGroupLabel>
                    <RadioGroupDescription
                      as="span"
                      :class="[
                        checked ? 'text-primary-700' : 'text-gray-500',
                        'block text-sm',
                      ]"
                    >
                      {{ setting.description }}
                    </RadioGroupDescription>
                  </div>
                </div>
              </RadioGroupOption>
            </div>
          </RadioGroup>

          <!-- Sharing ticket with multiple members. -->
          <div class="space-y-2">
            <div class="space-y-1">
              <label
                for="add-team-members"
                class="block text-sm font-medium text-gray-700"
              >
                Add fellow members
              </label>
              <p id="add-team-members-helper" class="sr-only">Search by name</p>
              <FormTextFieldWithSuggestions
                @add="(data) => sharedWith.push(data)"
                :data="guestsFiltered || []"
                emptyLabel="John Doe"
              />
            </div>

            <div class="border-b border-gray-200">
              <ul class="divide-y divide-gray-200">
                <li
                  v-for="person in sharedWith"
                  :key="person.name"
                  class="py-2 flex items-center justify-between"
                >
                  <div class="flex items-center">
                    <img
                      class="h-6 w-6 rounded-full"
                      :src="person.avatar"
                      alt=""
                    />
                    <span class="ml-3 text-sm font-medium text-gray-900">{{
                      person.name
                    }}</span>
                  </div>
                  <XMarkIcon
                    @click="
                      sharedWith.splice(
                        sharedWith.findIndex((s) => s.id === person.id),
                        1
                      )
                    "
                    class="h-5 w-5 text-gray-500 cursor-pointer"
                    aria-hidden="true"
                  />
                </li>
              </ul>
            </div>
          </div>

          <!-- Attachments of ticket. -->
          <div>
            <label
              for="attachments"
              class="block text-sm font-medium text-gray-700"
            >
              Attachments
            </label>
            <div class="flex flex-col justify-center w-full mt-1">
              <error
                class="mb-2"
                v-for="error in this.errors.attachments"
                :key="error"
                :message="error"
              ></error>
              <file-upload ref="upload" v-on:input="setFiles" class="w-full" />
            </div>
          </div>

          <!-- Form buttons -->
          <div class="flex justify-end">
            <button
              type="button"
              class="bg-white py-2 px-4 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
            >
              Cancel
            </button>
            <button
              :disabled="buttonDisabled"
              type="submit"
              class="ml-3 inline-flex justify-center py-2 px-4 border border-transparent rounded-md text-sm font-medium text-white focus:outline-none"
              :class="
                buttonDisabled
                  ? 'bg-primary-200 cursor-wait'
                  : 'bg-primary hover:bg-primary-600 focus:ring-2 focus:ring-offset-2 focus:ring-primary'
              "
            >
              Create this ticket
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import router from "@/router";
import { mapState } from "vuex";

import Attachment from '@/components/tickets/Attachment.vue'
import FileUpload from '@/components/inputs/FileInput.vue'
import TicketInput from '@/components/inputs/TicketInput.vue'
import LabelDropdown from '@/components/dropdown/LabelDropdown.vue'
import FormTextFieldWithSuggestions from '@/components/form/FormTextFieldWithSuggestions.vue'
import Error from '@/components/inputs/Error.vue'

import { ref } from "vue";
import {
  RadioGroup,
  RadioGroupDescription,
  RadioGroupLabel,
  RadioGroupOption,
} from "@headlessui/vue";
import { XMarkIcon, ExclamationCircleIcon, InformationCircleIcon } from "@heroicons/vue/24/solid";

const settings = [
  {
    key: "private",
    name: "Private ticket",
    description:
      "Only you and the staff team will be able to access this ticket",
  },
  {
    key: "public",
    name: "Public ticket",
    description: "This ticket will be available to anyone in this inbox",
  },
  {
    key: "anonymous",
    name: "Anonymous Public ticket",
    description:
      "This ticket will be available to anyone in this inbox and we won't show you as the author. You are responsible to exclude private information in this ticket's content!",
  },
];

export default {
  name: "Create",
  components: {
    Attachment,
    Error,
    FileUpload,
    TicketInput,
    FormTextFieldWithSuggestions,
    LabelDropdown,
    RadioGroup,
    RadioGroupDescription,
    RadioGroupLabel,
    RadioGroupOption,
    XMarkIcon,
    ExclamationCircleIcon,
    InformationCircleIcon
  },
  data: () => ({
    inbox: {},
    title: "",
    content: "",
    labels: [],
    shareInput: "",
    sharedWith: [],
    files: [],
    errors: [],
    buttonDisabled: false,
    ai: {
      prefetchingAnswers: {
        active: false,
        loading: false,
        response: null
      }
    }
  }),
  setup() {
    const open = ref(false);
    const privacy = ref(settings[0]);

    return {
      settings,
      open,
      privacy,
    };
  },
  mounted() {
    axios
      .get(`/api/inboxes/${this.$route.params.inboxId}/labels/all`)
      .then((response) => {
        this.inbox.labels = response.data;
      });

    axios.get(`/ai/prefetchingAnswers/healthz`)
      .then((response) => {
        this.ai.prefetchingAnswers.active = true
      })

    axios.get(`/api/inboxes/${this.$route.params.inboxId}/guests`)
      .then((response) => {
        this.inbox.guests = response.data.map((g) => ({
          id: g.id,
          name: g.first_name + " " + g.last_name,
          avatar: g.avatar_url,
        }));
      });
  },
  methods: {
    submit() {
      this.buttonDisabled = true;
      const formData = new FormData();

      formData.append("content", this.content);
      formData.append("title", this.title);

      this.labels.forEach((label) => formData.append("labels", label.id));
      this.files.forEach((file) => formData.append("files", file));
      this.sharedWith.forEach((sharedWith) =>
        formData.append("shared_with", sharedWith.id)
      );
      formData.append(
        "make_public",
        this.privacy.key === "public" || this.privacy.key === "anonymous"
      );
      formData.append("is_anonymous", this.privacy.key === "anonymous");

      axios
        .post(
          `/api/inboxes/${this.$route.params.inboxId}/tickets/new`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        )
        .then((response) => {
          router.push({
            name: "Ticket",
            params: {
              inboxId: this.$route.params.inboxId,
              ticketInboxId: response.data.ticket_inbox_id,
            },
          });
        })
        .catch((error) => {
          if (error.response.status === 413) {
            this.errors.attachments = [
              "The files you are trying to upload are too big.",
            ];
          } else {
            this.errors = error.response.data;
          }
          this.buttonDisabled = false;
        });
    },
    setFiles(files) {
      this.files = files;
    },
    setFiles (files) {
      this.files = files
    },
    prefetchAnswer () {
      this.ai.prefetchingAnswers.response = null
      this.ai.prefetchingAnswers.loading = true
      axios.get('/ai/prefetchingAnswers/question', {
        params: {
          question: this.content,
          inbox: this.$route.params.inboxId
        }
      }).then((response) => {
        this.ai.prefetchingAnswers.loading = false
        this.ai.prefetchingAnswers.response = response.data
        console.log(response.data)
      }).catch(() => {
        this.ai.prefetchingAnswers.loading = false
        this.ai.prefetchingAnswers.response = response.data
      })
    }
  },
  computed: {
    ...mapState({
      user: (state) => state.user,
    }),
    guestsFiltered() {
      return this.inbox?.guests
        ?.filter((g) => g.id !== this.user?.id)
        .filter((g) => this.sharedWith.indexOf(g) === -1);
    },
  },
};
</script>
