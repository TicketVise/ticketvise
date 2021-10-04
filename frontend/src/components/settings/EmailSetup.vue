<template>

  <div class="fixed z-10 inset-0 overflow-y-auto">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">

      <div class="fixed inset-0 transition-opacity" aria-hidden="true">
        <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
      </div>

      <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6"
           role="dialog" aria-modal="true" aria-labelledby="modal-headline">
        <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-headline">
          Email configuration
        </h3>
        <div class="mt-2 mb-2">
          <img :src="mailboxImage" alt="mailbox" class="w-2/3 md:w-1/2 mx-auto py-8">

          <p class="text-sm text-gray-500">
            Provide your email address and password to connect your mailbox to your TicketVise inbox.
          </p>
        </div>
        <form class="space-y-6" @submit.prevent="submit()">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">
              Email address
            </label>
            <div class="mt-1">
              <input id="email" name="email" type="email" autocomplete="email" v-model="email" required="" class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              Password
            </label>
            <div class="mt-1">
              <input id="password" name="password" type="password" v-model="password" autocomplete="current-password" required="" class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
            </div>
          </div>
            <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
              <button :disabled="loading" type="submit" :class="{'cursor-not-allowed': loading}" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:col-start-2 sm:text-sm">
                <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                Sign in
              </button>
              <button :disabled="loading" type="button" :class="{'cursor-not-allowed': loading}" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:col-start-1 sm:text-sm" @click="close()">
                Cancel
              </button>
            </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

const Mailbox = require('@/assets/img/svg/mailbox.svg')

  export default {
    name: 'EmailSetup',
    data () {
      return {
        mailboxImage: Mailbox,
        email: "",
        password: "",
        loading: false
      }
    },
    methods: {
      close() {
        this.$emit('close')
      },
      submit() {
        const inboxId = this.$route.params.inboxId
        const data = {
            email: this.email,
            password: this.password
        }

        this.loading = true
        axios.post(`/api/inboxes/${ inboxId }/email/login`, data).then(() => {
            this.email = this.password = ''
        })
      }
    }
  }
</script>
