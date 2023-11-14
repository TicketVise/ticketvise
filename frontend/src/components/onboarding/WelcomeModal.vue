<template>
  <div>
    <img :src="image" alt="Options" class="mx-auto w-1/2 pb-4 md:w-1/3" />

    <!-- <div class="rounded-md bg-blue-50 p-4 mb-4">
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
    </div> -->

    <h3 class="text-center text-xl font-medium leading-6 text-gray-800 md:text-left">Hi there, welcome!</h3>

    <p class="mt-1 text-justify text-sm text-gray-500">So now that you are here, let us help you get started! Your inbox has been created and out of the box everything is working for users, but to get you started with some settings you can follow this quick guide. If you know your way around, you can skip this guide.</p>
  </div>
</template>

<script>
import { InformationCircleIcon } from '@heroicons/vue/24/solid'

import image from '@/assets/img/svg/welcome.svg'

export default {
  name: 'WelcomeModal',
  components: {
    InformationCircleIcon
  },
  setup() {
    return { image }
  }
}
</script>
