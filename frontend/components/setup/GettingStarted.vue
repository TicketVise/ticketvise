<template>

  <div class="fixed z-10 inset-0 overflow-y-auto" v-if="modalNumber > 0">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">

      <div class="fixed inset-0 transition-opacity" aria-hidden="true">
        <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
      </div>

      <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6"
           role="dialog" aria-modal="true" aria-labelledby="modal-headline">

        <welcome-modal @click="modalNumber += 1" @cancel="finishIntroduction" v-if="modalNumber === 1"></welcome-modal>
        <overview-modal @click="modalNumber += 1" @cancel="modalNumber -= 1" v-if="modalNumber === 2"></overview-modal>
        <scheduling-modal @click="modalNumber += 1" @cancel="modalNumber -= 1"
                          v-if="modalNumber === 3"></scheduling-modal>
        <labels-modal @click="modalNumber += 1" @cancel="modalNumber -= 1" v-if="modalNumber === 4"></labels-modal>
        <statistics-modal @click="modalNumber += 1" @cancel="modalNumber -= 1"
                          v-if="modalNumber === 5"></statistics-modal>
        <finished-modal @click="finishIntroduction" @cancel="modalNumber -= 1"
                        v-if="modalNumber === maxModal"></finished-modal>
        <div class="flex items-center justify-center py-4" aria-label="Progress">
          <p class="text-sm font-medium">Step {{modalNumber}} of {{maxModal}}</p>

          <ol class="ml-8 flex items-center space-x-5">
            <li v-for="thisModal in maxModal" :key="thisModal">
              <button @click="modalNumber = thisModal"
                      class="block w-2.5 h-2.5 bg-orange-600 rounded-full hover:bg-orange-900"
                      v-if="thisModal < modalNumber">
                <span class="sr-only">Step {{thisModal}}</span>
              </button>

              <button class="relative flex items-center justify-center" aria-current="step"
                      v-if="thisModal === modalNumber">
              <span class="absolute w-5 h-5 p-px flex" aria-hidden="true">
                <span class="w-full h-full rounded-full bg-orange-200"></span>
              </span>
                <span class="relative block w-2.5 h-2.5 bg-orange-600 rounded-full" aria-hidden="true"></span>
                <span class="sr-only">Step {{thisModal}}</span>
              </button>

              <button @click="modalNumber = thisModal"
                      class="block w-2.5 h-2.5 bg-gray-200 rounded-full hover:bg-gray-400"
                      v-if="thisModal > modalNumber">
                <span class="sr-only">Step {{thisModal}}</span>
              </button>
            </li>
          </ol>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
  import axios from "axios";
  import WelcomeModal from "./WelcomeModal";
  import FinishedModal from "./FinishedModal";
  import StatisticsModal from "./StatisticsModal";
  import LabelsModal from "./LabelsModal";
  import SchedulingModal from "./SchedulingModal";
  import OverviewModal from "./OverviewModal";

  export default {
    name: "GettingStarted",
    components: {OverviewModal, SchedulingModal, LabelsModal, StatisticsModal, FinishedModal, WelcomeModal},
    data() {
      return {
        // modalNumber 1 for new users to start the setup.
        modalNumber: 1,
        maxModal: 6,
      }
    },
    methods: {
      finishIntroduction() {
        axios.put(`/api/me/introduction`)
        this.modalNumber = 0
        this.$emit("update")
      }
    }
  }
</script>

<style scoped>

</style>