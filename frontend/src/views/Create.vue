<template>
  <div class="w-full h-full overflow-y-auto">
    <div class="w-screen max-w-screen-lg mx-auto p-4">
      <form @submit.prevent="submit">
        <div class="space-y-6">
          <div>
            <h1 class="text-xl leading-6 font-medium text-gray-900">
              Create a new ticket
            </h1>
            <p class="mt-1 text-sm text-gray-500">
              Let’s get started by filling in the information below to create your new ticket.
            </p>
          </div>

          <div>
            <label for="project-name" class="block text-sm font-medium text-gray-700">
              Title
            </label>
            <div class="mt-1">
              <input v-model="title" type="text" name="project-name" id="project-name" class="block w-full focus:ring-primary focus:border-primary sm:text-sm border-gray-300 rounded-md" placeholder="Short and concise title for your ticket" />
            </div>
          </div>

          <div>
            <label for="content" class="block text-sm font-medium text-gray-700">
              Content
            </label>
            <div class="mt-1">
              <textarea v-model="content" id="content" name="content" rows="3" class="block w-full focus:ring-primary focus:border-primary sm:text-sm border border-gray-300 rounded-md" placeholder="This is the space to describe your ticket" />
            </div>
          </div>

          <div>
            <label for="labels" class="block text-sm font-medium text-gray-700">
              Labels
            </label>
            <div class="flex flex-wrap mb-2" v-if="selectedLabels?.length > 0">
              <chip :background="label.color" :key="label.id" class="m-1" v-for="label in selectedLabels">
                {{ label.name }}
              </chip>
            </div>
            <label-dropdown class="mt-1" :values="inbox?.labels" v-model="selectedLabels" />
          </div>

          <RadioGroup v-model="selected">
            <RadioGroupLabel class="text-sm font-medium text-gray-700">
              <span class="mr-1">Privacy</span>
              <span class="inline-flex items-center px-1 rounded-md text-xs font-medium bg-gray-100 text-primary">
                Work in progress
              </span>
            </RadioGroupLabel>

            <div class="mt-1 bg-white rounded-md -space-y-px">
              <RadioGroupOption disabled as="template" v-for="(setting, settingIdx) in settings" :key="setting.name" :value="setting" v-slot="{ checked, active }">
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

          <div class="space-y-2">
            <div class="space-y-1">
              <label for="add-team-members" class="block text-sm font-medium text-gray-700">
                Add fellow members
              </label>
              <p id="add-team-members-helper" class="sr-only">Search by name</p>
              <div class="flex">
                <div class="flex-grow">
                  <input type="text" name="add-team-members" id="add-team-members" class="block w-full focus:ring-primary focus:border-primary sm:text-sm border-gray-300 rounded-md" placeholder="Name" aria-describedby="add-team-members-helper" />
                </div>
                <span class="ml-3">
                  <button type="button" class="bg-white inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                    <PlusIcon class="-ml-2 mr-1 h-5 w-5 text-gray-400" aria-hidden="true" />
                    <span>Add</span>
                  </button>
                </span>
              </div>
            </div>

            <div class="border-b border-gray-200">
              <ul class="divide-y divide-gray-200">
                <li v-for="person in team" :key="person.name" class="py-2 flex items-center">
                  <img class="h-6 w-6 rounded-full" :src="person.imageUrl" alt="" />
                  <span class="ml-3 text-sm font-medium text-gray-900">{{ person.name }}</span>
                </li>
              </ul>
            </div>
          </div>

          <div>
            <label for="attachments" class="block text-sm font-medium text-gray-700">
              Attachments
            </label>
            <div class="flex flex-col justify-center w-full mt-1">
              <file-upload ref="upload" v-bind:value="files" v-on:input="setFiles" class="w-full" />
              <error class="mb-2" v-for="error in this.errors.attachments" :key="error" :message="error"></error>
            </div>
          </div>

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

import FileUpload from '@/components/inputs/FileInput'
import LabelDropdown from '@/components/dropdown/LabelDropdown'
import Chip from '@/components/chip/Chip'
import Error from '@/components/inputs/Error'

import { ref } from 'vue'
import {
  RadioGroup,
  RadioGroupDescription,
  RadioGroupLabel,
  RadioGroupOption
} from '@headlessui/vue'
import { PlusIcon } from '@heroicons/vue/solid'

const team = [
  {
    name: 'Calvin Hawkins',
    imageUrl:
      'https://images.unsplash.com/photo-1513910367299-bce8d8a0ebf6?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80'
  },
  {
    name: 'Bessie Richards',
    imageUrl:
      'https://images.unsplash.com/photo-1517841905240-472988babdf9?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80'
  }
]
const settings = [
  { name: 'Private ticket', description: 'Only you and the staff team will be able to access this ticket' },
  { name: 'Public ticket', description: 'This ticket will be available to anyone in this inbox, please make sure no sensitive information is included' }
]

export default {
  components: {
    Chip,
    Error,
    FileUpload,
    LabelDropdown,
    RadioGroup,
    RadioGroupDescription,
    RadioGroupLabel,
    RadioGroupOption,
    PlusIcon
  },
  data: () => ({
    title: '',
    content: '',
    inbox: {},
    selectedLabels: [],
    files: [],
    errors: []
  }),
  setup () {
    const open = ref(false)
    const selected = ref(settings[0])

    return {
      team,
      settings,
      open,
      selected
    }
  },
  mounted () {
    axios.get(`/api/inboxes/${this.$route.params.inboxId}/labels/all`)
      .then((response) => {
        this.inbox.labels = response.data
      })
  },
  methods: {
    submit () {
      const formData = new FormData()

      formData.append('content', this.content)
      formData.append('title', this.title)

      this.labels.forEach(label => formData.append('labels', label.id))
      this.files.forEach(file => formData.append('files', file))
      this.sharedWith.forEach(sharedWith => formData.append('sharedWith', sharedWith.id))

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
  }
}
</script>
