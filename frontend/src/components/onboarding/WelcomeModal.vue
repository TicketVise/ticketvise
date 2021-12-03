<template>
  <div>
    <div>
      <div class="mt-3sm:mt-5">
        <h3 class="text-xl text-center leading-6 font-medium text-gray-800" id="modal-headline">
          Hi there, welcome!
        </h3>
        <div class="mt-2">
          <img :src="image" alt="Options" class="w-2/3 md:w-1/2 mx-auto py-8">

          <div class="rounded-md bg-blue-50 p-4 mb-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <InformationCircleIcon class="h-5 w-5 text-blue-400" aria-hidden="true" />
              </div>
              <div class="ml-3 flex-1 md:flex md:justify-between">
                <p class="text-sm text-blue-700">
                  If you are new to TicketVise, check out our <a href="https://ticketvise.com/getting-started/" target="_blank" rel="noopener noreferrer" class="underline">Getting Started</a> guide to get an impression of what you can do with TicketVise.
                </p>
              </div>
            </div>
          </div>

          <p class="text-sm text-gray-500">
            So now that you are here, let us help you get started! Your inbox has been created and out of the box everything is working for connected users, but to get you started with some settings you can follow this quick guide. If you know your way around, you can skip this guide or go straight to the settings page to configure your inbox.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { InformationCircleIcon } from '@heroicons/vue/solid'

const image = require('@/assets/img/svg/welcome.svg')

export default {
  name: 'WelcomeModal',
  components: {
    InformationCircleIcon
  },
  setup () {
    return { image }
  }
}
</script>
