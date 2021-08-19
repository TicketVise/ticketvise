<template>
  <div class="w-full h-full overflow-y-auto">
    <div class="w-screen max-w-screen-lg mx-auto p-4">
      <form @submit.prevent="submit" autocomplete="off">
        <div class="space-y-6">
          <div>
            <h1 class="text-xl leading-6 font-medium text-gray-900">
              Create a new ticket
            </h1>
            <p class="mt-1 text-sm text-gray-500">
              Let’s get started by filling in the information below to create your new ticket.
            </p>
          </div>

          <!-- Title of the ticket. -->
          <div>
            <label for="project-name" class="block text-sm font-medium text-gray-700">
              Title
            </label>
            <div class="mt-1">
              <input v-model="title" type="text" name="project-name" id="project-name" class="block w-full focus:ring-primary focus:border-primary sm:text-sm border-gray-300 rounded-md" placeholder="Short and concise title for your ticket" />
            </div>
          </div>

          <!-- Description of the ticket. -->
          <div>
            <label for="content" class="block text-sm font-medium text-gray-700">
              Content
            </label>
            <div class="mt-1">
              <textarea v-model="content" id="content" name="content" rows="4" class="block w-full focus:ring-primary focus:border-primary sm:text-sm border border-gray-300 rounded-md" placeholder="This is the space to describe your ticket" />
            </div>
          </div>

          <!-- The labels of the ticket. -->
          <select-input v-model="label" label="Labels" :data="inbox?.labels || []" emptyLabel="Select label" />

          <!-- This privacy setting for ticket. -->
          <RadioGroup v-model="privacy">
            <RadioGroupLabel class="text-sm font-medium text-gray-700">
              Privacy
            </RadioGroupLabel>

            <div class="mt-1 bg-white rounded-md -space-y-px">
              <RadioGroupOption as="template" v-for="(setting, settingIdx) in settings" :key="setting.key" :value="setting" v-slot="{ checked, active }">
                <div :class="[settingIdx === 0 ? 'rounded-tl-md rounded-tr-md' : '', settingIdx === settings.length - 1 ? 'rounded-bl-md rounded-br-md' : '', checked ? 'bg-primary-50 border-primary-200 z-10' : 'border-gray-200', 'relative border p-4 flex cursor-pointer focus:outline-none']">
                  <span :class="[checked ? 'bg-primary-600 border-transparent' : 'bg-white border-gray-300', active ? 'ring-2 ring-offset-2 ring-primary' : '', 'h-4 w-4 mt-0.5 cursor-pointer rounded-full border flex items-center justify-center']" aria-hidden="true">
                    <span class="rounded-full bg-white w-1.5 h-1.5" />
                  </span>
                  <div class="ml-3 flex flex-col">
                    <RadioGroupLabel as="span" class="text-gray-900 block text-sm font-medium">
                      {{ setting.name }}
                    </RadioGroupLabel>
                    <RadioGroupDescription as="span" :class="[checked ? 'text-primary-700' : 'text-gray-500', 'block text-sm']">
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
              <label for="add-team-members" class="block text-sm font-medium text-gray-700">
                Add fellow members
              </label>
              <p id="add-team-members-helper" class="sr-only">Search by name</p>
              <FormTextFieldWithSuggestions @add="data => sharedWith.push(data)" :data="guestsFiltered || []" emptyLabel="John Doe" />
            </div>

            <div class="border-b border-gray-200">
              <ul class="divide-y divide-gray-200">
                <li v-for="person in sharedWith" :key="person.name" class="py-2 flex items-center justify-between">
                  <div class="flex items-center">
                    <img class="h-6 w-6 rounded-full" :src="person.avatar" alt="" />
                    <span class="ml-3 text-sm font-medium text-gray-900">{{ person.name }}</span>
                  </div>
                  <XIcon @click="sharedWith.splice(sharedWith.findIndex(s => s.id === person.id), 1)" class="h-5 w-5 text-gray-500 cursor-pointer" aria-hidden="true" />
                </li>
              </ul>
            </div>
          </div>

          <!-- Attachments of ticket. -->
          <div>
            <label for="attachments" class="block text-sm font-medium text-gray-700">
              Attachments
            </label>
            <div class="flex flex-col justify-center w-full mt-1">
              <file-upload ref="upload" v-bind:value="files" v-on:input="setFiles" class="w-full" />
              <error class="mb-2" v-for="error in this.errors.attachments" :key="error" :message="error"></error>
            </div>
          </div>

          <!-- Form buttons -->
          <div class="flex justify-end">
            <button type="button" class="bg-white py-2 px-4 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
              Cancel
            </button>
            <button type="submit" class="ml-3 inline-flex justify-center py-2 px-4 border border-transparent rounded-md text-sm font-medium text-white bg-primary hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
              Create this ticket
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import router from '@/router'
import { mapState } from 'vuex'

import FileUpload from '@/components/inputs/FileInput'
import SelectInput from '@/components/inputs/SelectInput'
import FormTextFieldWithSuggestions from '@/components/form/FormTextFieldWithSuggestions'
import Error from '@/components/inputs/Error'

import { ref } from 'vue'
import {
  RadioGroup,
  RadioGroupDescription,
  RadioGroupLabel,
  RadioGroupOption
} from '@headlessui/vue'
import { XIcon } from '@heroicons/vue/solid'

const settings = [
  { key: 'private', name: 'Private ticket', description: 'Only you and the staff team will be able to access this ticket' },
  { key: 'public', name: 'Public ticket', description: 'This ticket will be available to anyone in this inbox' },
  { key: 'anonymous', name: 'Anonymous Public ticket', description: 'This ticket will be available to anyone in this inbox and we won\'t show you as the author. You are responsible to exclude private information in this ticket\'s content!' }
]

export default {
  components: {
    Error,
    FileUpload,
    FormTextFieldWithSuggestions,
    RadioGroup,
    RadioGroupDescription,
    RadioGroupLabel,
    RadioGroupOption,
    SelectInput,
    XIcon
  },
  data: () => ({
    inbox: {},
    title: '',
    content: '',
    label: {},
    shareInput: '',
    sharedWith: [],
    files: [],
    errors: []
  }),
  setup () {
    const open = ref(false)
    const privacy = ref(settings[0])

    return {
      settings,
      open,
      privacy
    }
  },
  mounted () {
    axios.get(`/api/inboxes/${this.$route.params.inboxId}/labels/all`)
      .then((response) => {
        this.inbox.labels = response.data
      })

    axios.get(`/api/inboxes/${this.$route.params.inboxId}/guests`)
      .then((response) => {
        this.inbox.guests = response.data.map(g => ({
          id: g.id,
          name: g.first_name + ' ' + g.last_name,
          avatar: g.avatar_url
        }))
      })
  },
  methods: {
    submit () {
      const formData = new FormData()

      formData.append('content', this.content)
      formData.append('title', this.title)

      // this.labels.forEach(label => formData.append('labels', label.id))
      formData.append('labels', [this.label.id])
      this.files.forEach(file => formData.append('files', file))
      this.sharedWith.forEach(sharedWith => formData.append('shared_with', sharedWith.id))
      formData.append('make_public', this.privacy.key === 'public' || this.privacy.key === 'anonymous')
      formData.append('is_anonymous', this.privacy.key === 'anonymous')

      axios.post(`/api/inboxes/${this.$route.params.inboxId}/tickets/new`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then(response => {
        router.push({
          name: 'Ticket',
          params: {
            inboxId: this.$route.params.inboxId,
            ticketInboxId: response.data.ticket_inbox_id
          }
        })
      }).catch(error => {
        this.errors = error.response.data
      })
    },
    setFiles (files) {
      this.files = files
    }
  },
  computed: {
    ...mapState({
      user: state => state.user
    }),
    guestsFiltered () {
      return this.inbox?.guests?.filter(g => g.id !== this.user?.id)
        .filter(g => this.sharedWith.indexOf(g) === -1)
    }
  }
}
</script>
