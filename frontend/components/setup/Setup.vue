<template>

  <div class="fixed z-10 inset-0 overflow-y-auto" v-if="modalNumber > 0">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">

      <div class="fixed inset-0 transition-opacity" aria-hidden="true">
        <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
      </div>

      <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
      <welcome-modal @click="modalNumber += 1" @cancel="modalNumber -= 1" v-if="modalNumber === 1"></welcome-modal>
      <overview-modal @click="modalNumber += 1" @cancel="modalNumber -= 1" v-if="modalNumber === 2"></overview-modal>
      <scheduling-modal @click="modalNumber += 1" @cancel="modalNumber -= 1"
                        v-if="modalNumber === 3"></scheduling-modal>
      <labels-modal @click="modalNumber += 1" @cancel="modalNumber -= 1" v-if="modalNumber === 4"></labels-modal>
      <statistics-modal @click="modalNumber += 1" @cancel="modalNumber -= 1" v-if="modalNumber === 5"></statistics-modal>
      <finished-modal @click="modalNumber = 0" @cancel="modalNumber -= 1" v-if="modalNumber === 6"></finished-modal>
    </div>
  </div>

</template>

<script>
  import WelcomeModal from "./WelcomeModal";

  export default {
    name: "Setup",
    components: {WelcomeModal},
    data() {
      return {
        // modalNumber 1 for new users to start the setup.
        modalNumber: 1,
      }
    },
    methods: {}
  }
</script>

<style scoped>

</style>