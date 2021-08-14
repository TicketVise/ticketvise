<template>
  <div>
    <div>
      <div class="mt-3 text-center sm:mt-5">
        <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-headline">
          Welcome!
        </h3>
        <div class="mt-2">
          <img :src="image" alt="Options" class="w-2/3 md:w-1/2 mx-auto py-8">

          <p class="text-sm text-gray-500">
            Connected users can now access this inbox and create tickets. To get to know TicketVise and to personalize
            this inbox, we guide you through the most important things. For more information, visit the getting started
            page found under the question mark in the navigation.
          </p>
        </div>
      </div>
    </div>
    <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
      <button type="button" @click="$emit('click')"
              class="w-full inline-flex justify-center rounded-md px-4 py-2 bg-primary text-base font-medium text-white hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 sm:col-start-2 sm:text-sm">
        Continue
      </button>
      <button type="button" @click="$emit('cancel')"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:col-start-1 sm:text-sm">
        Skip introduction
      </button>
    </div>
  </div>
</template>

<script>
const image = require('@/assets/img/svg/options.svg')

export default {
  name: 'WelcomeModal',
  setup () {
    return { image }
  }
}
</script>
