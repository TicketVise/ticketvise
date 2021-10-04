<template>
  <div class="bg-white shadow sm:rounded-lg">
    <div class="px-4 py-5 sm:p-6">
      <h3 class="text-lg leading-6 font-medium text-gray-900">
        Mailbox
      </h3>
      <div class="mt-2 sm:flex sm:items-start sm:justify-between">
        <div class="max-w-xl text-sm text-gray-500">
          <p>
            Connect a email address to your TicketVise inbox to automatically create tickets from emails
          </p>
        </div>
        <div class="mt-5 sm:mt-0 sm:ml-6 sm:flex-shrink-0 sm:flex sm:items-center">
          <button type="button" v-if="connected" class="inline-flex items-center justify-center px-4 py-2 border border-transparent font-medium rounded-md text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:text-sm">
            Disconnect
          </button>
          <button type="button" @click="showConnectModal = true" v-else class="ml-5 bg-primary border border-transparent rounded-md shadow-sm py-2 px-4 inline-flex justify-center text-sm font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
            Connect
          </button>
        </div>
      </div>
    </div>
  </div>

  <email-setup v-if="showConnectModal" @close="showConnectModal=false" />
</template>

<script>
import EmailSetup from './EmailSetup.vue'
const mailboxImage = require('@/assets/img/svg/mailbox.svg')

export default {
  name: 'EmailStatus',
  components: {
    EmailSetup
  },
  data: () => ({
    showConnectModal: false
  }),
  props: {
    connected: {
      type: Boolean,
      required: false,
      default: false
    }
  },
}
</script>
