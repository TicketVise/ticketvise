<template>
  <div class="w-full h-full overflow-y-auto">
    <div class="relative w-screen max-w-screen-lg mx-auto bg-white">
      <div class="divide-y divide-gray-200 lg:divide-y-0 lg:divide-x">
        <form class="divide-y divide-gray-200" action="#" method="POST">
          <!-- Inbox section -->
          <div class="p-4">
            <div>
              <h2 class="text-lg leading-6 font-medium text-gray-900">Inbox</h2>
              <p class="mt-1 text-sm text-gray-500">
                This information is about the inbox and the look and feel of the inbox.
              </p>
            </div>

            <div class="mt-6 flex flex-col lg:flex-row">
              <div class="flex-grow space-y-6">
                <div>
                  <label for="name" class="block text-sm font-medium text-gray-700">
                    <span class="mr-1">Name</span>
                    <span class="inline-flex items-center px-2.5 rounded-md text-sm font-medium bg-gray-100 text-primary">
                      LTI
                    </span>
                  </label>
                  <div class="mt-1 flex">
                    <input disabled v-model="inbox.name" type="text" name="name" id="name" autocomplete="name" class="cursor-not-allowed border rounded-md focus:ring-primary focus:border-primary flex-grow block w-full min-w-0 sm:text-sm border-gray-300" />
                  </div>
                </div>

                <div class="grid gap-4 grid-cols-2">
                  <div>
                    <label for="code" class="block text-sm font-medium text-gray-700">
                      <span class="mr-1">Code</span>
                      <span class="inline-flex items-center px-2.5 rounded-md text-sm font-medium bg-gray-100 text-primary">
                        LTI
                      </span>
                    </label>
                    <div class="mt-1 flex">
                      <input disabled v-model="inbox.code" type="text" name="code" id="code" autocomplete="name" class="cursor-not-allowed border rounded-md focus:ring-primary focus:border-primary flex-grow block w-full min-w-0 sm:text-sm border-gray-300" />
                    </div>
                  </div>

                  <select-input v-if="coordinators.length > 0 && inbox.coordinator" label="Displayed Coordinator" :data="coordinators" :init="coordinators.filter(x => x.id === inbox.coordinator.id)[0]" />
                </div>
              </div>

              <div class="mt-6 flex-grow lg:mt-0 lg:ml-6 lg:flex-grow-0 lg:flex-shrink-0">
                <p class="text-sm font-medium text-gray-700" aria-hidden="true">
                  Cover photo
                </p>
                <div class="mt-1 lg:hidden">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 inline-block rounded-md overflow-hidden h-16 w-20" aria-hidden="true">
                      <img class="rounded-md h-full w-full" :src="im_url" alt="" />
                    </div>
                    <div class="ml-5 rounded-md shadow-sm">
                      <div class="group relative border border-gray-300 rounded-md py-2 px-3 flex items-center justify-center hover:bg-gray-50 focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-primary">
                        <label for="inbox-photo" class="relative text-sm leading-4 font-medium text-gray-700 pointer-events-none">
                          <span>Change</span>
                          <span class="sr-only"> inbox photo</span>
                        </label>
                        <input id="inbox-photo" name="inbox-photo" type="file" class="absolute w-full h-full opacity-0 cursor-pointer border-gray-300 rounded-md" />
                      </div>
                    </div>
                  </div>
                </div>

                <div class="hidden relative rounded-md overflow-hidden lg:block">
                  <img class="relative rounded-md w-64 h-40" :src="im_url" alt="" />
                  <label for="inbox-photo" class="absolute inset-0 w-full h-full bg-black bg-opacity-75 flex items-center justify-center text-sm font-medium text-white opacity-0 hover:opacity-100 focus-within:opacity-100">
                    <span>Change</span>
                    <span class="sr-only"> inbox photo</span>
                    <input type="file" id="inbox-photo" name="inbox-photo" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer border-gray-300 rounded-md" />
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- Privacy section -->
          <div class="pt-6 divide-y divide-gray-200">
            <div class="px-4">
              <div>
                <h2 class="text-lg leading-6 font-medium text-gray-900">General</h2>
                <p class="mt-1 text-sm text-gray-500">
                  Some general settings regarding the tickets in the inbox.
                </p>
              </div>
              <ul class="mt-2 divide-y divide-gray-200">
                <SwitchGroup as="li" class="py-4 flex items-center justify-between space-x-2">
                  <div class="flex flex-col">
                    <SwitchLabel as="p" class="text-sm font-medium text-gray-900" passive>
                      Assignee visible to students
                    </SwitchLabel>
                    <SwitchDescription class="text-sm text-gray-500">
                      Whether or not to show who is assigned to the ticket.
                    </SwitchDescription>
                  </div>
                  <Switch v-model="assigneeVisible" :class="[assigneeVisible ? 'bg-primary' : 'bg-gray-200', 'ml-4 relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary']">
                    <span aria-hidden="true" :class="[assigneeVisible ? 'translate-x-5' : 'translate-x-0', 'inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']" />
                  </Switch>
                </SwitchGroup>
                <SwitchGroup as="li" class="py-4 flex items-center justify-between space-x-2">
                  <div class="flex flex-col">
                    <SwitchLabel as="p" class="text-sm font-medium text-gray-900" passive>
                      Automatically close tickets
                    </SwitchLabel>
                    <SwitchDescription class="text-sm text-gray-500">
                      Automatically close tickets after some weeks with no activity.
                    </SwitchDescription>
                  </div>
                  <select-input :data="closeTicketsOptions" :init="closeTicketsOptions[0]" />
                </SwitchGroup>
                <SwitchGroup as="li" class="py-4 flex items-center justify-between space-x-2">
                  <div class="flex flex-col">
                    <SwitchLabel as="p" class="text-sm font-medium text-gray-900" passive>
                      Send alert unanswered tickets
                    </SwitchLabel>
                    <SwitchDescription class="text-sm text-gray-500">
                      Automatically send an alert when a ticket is unanswered after some days.
                    </SwitchDescription>
                  </div>
                  <select-input :data="sendAlertOptions" :init="sendAlertOptions[0]" />
                </SwitchGroup>
              </ul>
            </div>
            <div class="mt-4 py-4 px-4 flex justify-end sm:px-6 space-x-4">
              <button type="button" class="bg-white border border-gray-300 rounded-md shadow-sm py-2 px-4 inline-flex justify-center text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                Cancel
              </button>
              <button type="submit" class="ml-5 bg-primary border border-transparent rounded-md shadow-sm py-2 px-4 inline-flex justify-center text-sm font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                Save
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'
import SelectInput from '@/components/inputs/SelectInput'
// import Error from '@/components/inputs/Error'

import {
  Switch,
  SwitchDescription,
  SwitchGroup,
  SwitchLabel
} from '@headlessui/vue'

const closeTicketsOptions = [
  { name: 'Disabled' },
  { name: '1 week' },
  { name: '2 weeks' },
  { name: '3 weeks' },
  { name: '4 weeks' }
]
const sendAlertOptions = [
  { name: 'Disabled' },
  { name: '1 day' },
  { name: '2 days' },
  { name: '3 days' },
  { name: '4 days' },
  { name: '5 days' },
  { name: '6 days' },
  { name: '7 days' }
]

export default {
  name: 'InboxSettings',
  components: {
    // Error,
    Switch,
    SwitchDescription,
    SwitchGroup,
    SwitchLabel,
    SelectInput
  },
  data () {
    return {
      inbox: {},
      im_url: '',
      staff: [],
      coordinators: [],
      scheduling_options: [],
      errors: [],
      saved: false,
      user: this.$store.state.user
    }
  },
  setup () {
    const assigneeVisible = ref(true)

    return {
      assigneeVisible,
      closeTicketsOptions,
      sendAlertOptions
    }
  },
  created () {
    axios
      .get(`/api/inboxes/${this.$route.params.inboxId}/settings`)
      .then(response => {
        this.inbox = response.data.inbox
        this.staff = response.data.staff
        this.coordinators = response.data.coordinators
        this.coordinators.forEach(c => {
          c.name = c.first_name + ' ' + c.last_name
          c.avatar = c.avatar_url
        })
        this.scheduling_options = response.data.scheduling_options
        this.im_url = this.inbox.image
      })
  },
  methods: {
    onSave: function () {
      axios.defaults.xsrfCookieName = 'csrftoken'
      axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

      const formData = new FormData()

      for (const key in this.inbox) {
        if (key !== 'image') {
          formData.append(key, this.inbox[key])
        } else if (this.inbox[key] !== this.im_url) {
          formData.append(key, this.inbox[key])
        }
      }
      const config = {
        headers: { 'content-type': 'multipart/form-data' }
      }

      axios
        .put(
          `/api/inboxes/${this.$route.params.inboxId}/settings`,
          formData,
          config
        )
        .then(response => {
          this.errors = []
          this.saved = true
          this.inbox = response.data
        })
        .catch(error => {
          this.saved = false
          this.errors = error.response.data
        })
    },
    onCancel: function () {
      window.history.back()
    },

    onChange (event) {
      if (event) {
        this.inbox.image = event.target.files[0]
      }
      const reader = new FileReader()
      reader.onload = e => {
        this.im_url = e.target.result
      }
      reader.readAsDataURL(this.inbox.image)
    },
    dragover (event) {
      event.preventDefault()
      if (!event.currentTarget.classList.contains('bg-orange-300')) {
        event.currentTarget.classList.remove('bg-gray-100')
        event.currentTarget.classList.add('bg-orange-300')
      }
    },
    dragleave (event) {
      event.currentTarget.classList.add('bg-gray-100')
      event.currentTarget.classList.remove('bg-orange-300')
    },
    drop (event) {
      event.preventDefault()
      this.inbox.image = event.dataTransfer.files[0]

      this.onChange()
      this.dragleave(event)
    }
  }
}
</script>
