<template>
  <div class="fixed z-10 inset-0 overflow-y-auto">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">

      <div class="fixed inset-0 transition-opacity" aria-hidden="true">
        <div class="absolute inset-0 bg-gray-400 opacity-50"></div>
      </div>

      <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6"
           role="dialog" aria-modal="true" aria-labelledby="modal-headline">

        <welcome-modal v-if="onboarding.step === 0" />
        <tickets-modal v-if="onboarding.step === 2" />
        <scheduling-modal v-if="onboarding.step === 3" />
        <labels-modal v-if="onboarding.step === 4" />
        <statistics-modal v-if="onboarding.step === 5" />
        <finished-modal v-if="onboarding.step === 6" />

        <div v-if="onboarding.step > 0" class="flex items-center justify-center pt-4" aria-label="Progress">
          <p class="text-sm font-medium">Step {{ onboarding.step }} of {{ maxModal }}</p>

          <ol class="ml-8 flex items-center space-x-5">
            <li v-for="thisModal in maxModal" :key="thisModal">
              <button @click="onboarding.step = thisModal"
                      class="block w-2.5 h-2.5 bg-primary-600 rounded-full hover:bg-primary-900"
                      v-if="thisModal < onboarding.step">
                <span class="sr-only">Step {{thisModal}}</span>
              </button>

              <button class="relative flex items-center justify-center" aria-current="step"
                      v-if="thisModal === onboarding.step">
              <span class="absolute w-5 h-5 p-px flex" aria-hidden="true">
                <span class="w-full h-full rounded-full bg-primary-200"></span>
              </span>
                <span class="relative block w-2.5 h-2.5 bg-primary-600 rounded-full" aria-hidden="true"></span>
                <span class="sr-only">Step {{ thisModal }}</span>
              </button>

              <button @click="onboarding.step = thisModal"
                      class="block w-2.5 h-2.5 bg-gray-200 rounded-full hover:bg-gray-400"
                      v-if="thisModal > onboarding.step">
                <span class="sr-only">Step {{ thisModal }}</span>
              </button>
            </li>
          </ol>
        </div>

        <div class="mt-5 sm:mt-4 space-y-2 sm:space-y-0 sm:flex sm:flex-row-reverse">
          <button @click="nextStep()" type="button" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary sm:ml-3 sm:w-auto sm:text-sm">
            {{ onboarding.step === 0 ? 'Start' : 'Next' }}
          </button>
          <!-- <button v-if="onboarding.step === 0" type="button" class="w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary sm:ml-3 sm:w-auto sm:text-sm">
            Settings
          </button> -->
          <button v-if="onboarding.step === 0" type="button" class="w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary sm:ml-3 sm:w-auto sm:text-sm" @click="finishIntroduction">
            Skip
          </button>
          <button v-if="onboarding.step > 0" @click="prevStep()" type="button" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary sm:mt-0 sm:w-auto sm:text-sm">
            Previous
          </button>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import axios from 'axios'
import store from '@/store'
import { mapState, mapActions } from "vuex"

import WelcomeModal from './WelcomeModal.vue'
import FinishedModal from './FinishedModal.vue'
import StatisticsModal from './StatisticsModal.vue'
import LabelsModal from './LabelsModal.vue'
import SchedulingModal from './SchedulingModal.vue'
import TicketsModal from './TicketsModal.vue'

export default {
  name: 'GettingStarted',
  components: {
    TicketsModal,
    SchedulingModal,
    LabelsModal,
    StatisticsModal,
    FinishedModal,
    WelcomeModal
  },
  data: () => ({
    // modalNumber: 0,
    maxModal: 6
  }),
  methods: {
    ...mapActions('onboarding', {
      nextStep: 'next',
      prevStep: 'prev'
    }),
    finishIntroduction () {
      axios.put('/api/me/introduction')
      // this.modalNumber = 0
      this.$emit('update')
    }
  },
  computed: {
    ...mapState('onboarding', {
      onboarding: (state) => state.status
    })
  },
  watch: {
    async modalNumber (newVal) {
      const { inboxId } = this.$route.params

      // switch (newVal) {
      //   case 0:
      //     this.$router.push({ name: 'Overview', params: { inboxId: inboxId } })
      //     await store.commit('update_inboxes')
      //     break
      //   case 1:
      //     this.$router.push({ name: 'Tickets', params: { inboxId: inboxId } })
      //     // store.dispatch('demo_tickets', { inboxId: inboxId, status: 'pending' })
      //     break
      //   case 2:
      //     this.$router.push({ name: 'Automation', params: { inboxId: inboxId } })
      //     break
      //   case 3:
      //     this.$router.push({ name: 'Labels', params: { inboxId: inboxId } })
      //     break
      // }
    }
  }
}
</script>
