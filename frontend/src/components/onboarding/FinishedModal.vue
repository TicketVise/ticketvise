<template>
  <div>
    <div>
      <div class="mt-3 text-center sm:mt-5">
        <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-headline">
          All done!
        </h3>
        <div class="mt-2">
          <p class="text-sm text-gray-500">
            <img :src="image" alt="Options" class="w-2/3 md:w-1/2 mx-auto py-8">
            The inbox is now ready for use. Students will be able to create tickets to ask their questions. Assistants
            will be able to help these students once they have connected to the course by visiting TicketVise from
            canvas.
          </p>
        </div>
      </div>
    </div>
    <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
      <button type="button" @click="$emit('next')"
              class="w-full inline-flex justify-center rounded-md px-4 py-2 bg-primary text-base font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:col-start-2 sm:text-sm">
        Finish
      </button>
      <button type="button" @click="$emit('cancel')"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:mt-0 sm:col-start-1 sm:text-sm">
        Back
      </button>
    </div>
  </div>
</template>

<script>
import image from '@/assets/img/svg/celebration.svg'

export default {
  name: 'FinishedModal',
  setup () {
    return { image }
  }
}
</script>
