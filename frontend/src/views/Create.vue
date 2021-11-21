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
              Let’s get started by filling in the information below to create your new ticket.
            </p>
          </div>

          <!-- Title of the ticket. -->
          <NewTicketInput />

          <!-- This privacy setting for ticket. -->
          <TicketPrivacyInput />

          <!-- Form buttons -->
          <div class="flex justify-end">
            <button type="button" class="bg-white py-2 px-4 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
              Cancel
            </button>
            <button :disabled="buttonDisabled" type="submit" class="ml-3 inline-flex justify-center py-2 px-4 border border-transparent rounded-md text-sm font-medium text-white focus:outline-none" :class="buttonDisabled ? 'bg-primary-200 cursor-wait' : 'bg-primary hover:bg-primary-600 focus:ring-2 focus:ring-offset-2 focus:ring-primary'">
              Create ticket
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

import NewTicketInput from '@/components/inputs/NewTicketInput'
import TicketPrivacyInput from '@/components/inputs/TicketPrivacyInput'

import { ref } from 'vue'

const settings = [
  { key: 'private', name: 'Private ticket', description: 'Only you and the staff team will be able to access this ticket' },
  { key: 'public', name: 'Public ticket', description: 'This ticket will be available to anyone in this inbox' },
  { key: 'anonymous', name: 'Anonymous Public ticket', description: 'This ticket will be available to anyone in this inbox and we won\'t show you as the author. You are responsible to exclude private information in this ticket\'s content!' }
]

export default {
  name: 'Create',
  components: {
    NewTicketInput,
    TicketPrivacyInput
  },
  data: () => ({
    inbox: {},
    title: '',
    content: '',
    labels: [],
    shareInput: '',
    sharedWith: [],
    files: [],
    errors: [],
    buttonDisabled: false
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
      this.buttonDisabled = true
      const formData = new FormData()

      formData.append('content', this.content)
      formData.append('title', this.title)

      this.labels.forEach(label => formData.append('labels', label.id))
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
        if (error.response.status === 413) {
          this.errors.attachments = ['The files you are trying to upload are too big.']
        } else {
          this.errors = error.response.data
        }
        this.buttonDisabled = false
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
