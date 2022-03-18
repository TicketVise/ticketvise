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
            Provide your email address to connect your mailbox to your TicketVise inbox.
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

          <div class="rounded-md bg-red-50 p-4" v-if="error">
            <div class="flex">
              <div class="flex-shrink-0">
                <XCircleIcon class="h-5 w-5 text-red-400" aria-hidden="true" />
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-red-800">
                  Encountered an error while trying to automatically configure email. Please try again, change your credentials or configure email settings <a class="underline text-blue-600 hover:text-blue-800" href="#">manually</a>.
                </h3>
                <div class="mt-2 text-sm text-red-700">
                  <ul role="list" class="list-disc pl-5 space-y-1">
                    <li>
                      {{ error }}
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

            <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
              <button :disabled="loading" type="submit" :class="{'cursor-not-allowed': loading}" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:col-start-2 sm:text-sm">
                <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                Configure
              </button>
              <button :disabled="loading" type="button" :class="{'cursor-not-allowed': loading}" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:col-start-1 sm:text-sm" @click="close()">
                Cancel
              </button>
            </div>
            <!-- <p class="text-sm text-center text-gray-500">
              Manually <a class="underline text-blue-600 hover:text-blue-800" href="#">configure</a> email settings
            </p> -->
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { XCircleIcon } from '@heroicons/vue/solid'

import Mailbox from '@/assets/img/svg/mailbox.svg'

  export default {
    name: 'EmailConnectModal',
    components: {
      XCircleIcon,
    },
    data () {
      return {
        mailboxImage: Mailbox,
        email: "",
        loading: false,
        error: ""
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
        }

        this.loading = true
        this.error = ""
        axios.post(`/api/inboxes/${ inboxId }/settings/email`, data).then((resp) => {
          window.location = resp.data.auth_uri
        }).catch((err) => {
          if (err.response) {
            this.error = err.response.data
          } else {
            this.error = "Unknown error encountered"
            console.error(err);
          }

        }).finally(() => {
          this.loading = false
        });
      }
    }
  }
</script>
