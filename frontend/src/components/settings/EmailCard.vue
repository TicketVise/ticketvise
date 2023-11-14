<template>
  <div>
    <div>
      <h3 class="text-lg leading-6 font-medium text-gray-900">
        Mailbox
      </h3>
      <div class="mt-2 sm:flex sm:items-start sm:justify-between">
        <div class="max-w-xl text-sm text-gray-500">
          <p v-if="connected">
            Remove your email inbox from your TicketVise inbox. This will remove the functionallity to automatically create tickets from emails and comments from replies.
          </p>
          <p v-else>
            Connect an email address to your TicketVise inbox to automatically create tickets from emails and comments from replies.
          </p>
        </div>
        <div class="mt-5 sm:mt-0 sm:ml-6 sm:flex-shrink-0 sm:flex sm:items-center">
          <button type="button" v-if="connected" @click="toggleDisconnectModal()" class="inline-flex items-center justify-center px-4 py-2 border border-transparent font-medium rounded-md text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:text-sm">
            Disconnect
          </button>
          <button type="button" @click="toggleConnectModal()" v-else class="ml-5 bg-primary border border-transparent rounded-md shadow-sm py-2 px-4 inline-flex justify-center text-sm font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
            Connect
          </button>
        </div>
      </div>
    </div>
    <email-connect-modal v-if="showConnectModal" @close="closeModal()" />
    <email-disconnect-modal v-if="showDisconnectModal" @close="closeModal()" 
      @disconnected="connected=false"/>
  </div>
</template>

<script>
import EmailConnectModal from './EmailConnectModal.vue'
import EmailDisconnectModal from './EmailDisconnectModal.vue'

export default {
  name: 'EmailCard',
  components: {
    EmailConnectModal,
    EmailDisconnectModal
  },
  data: () => ({
    showConnectModal: false,
    showDisconnectModal: false
  }),
  props: {
    connected: {
      type: Boolean,
      required: false,
      default: false
    }
  },
  methods: {
    toggleConnectModal() {
      this.showConnectModal = true
      this.showDisconnectModal = false
    },
    toggleDisconnectModal() {
      this.showConnectModal = false
      this.showDisconnectModal = true
    },
    closeModal() {
      this.showConnectModal = false
      this.showDisconnectModal = false
    }
  }
}
</script>
