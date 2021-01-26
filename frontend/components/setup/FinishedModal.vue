<template>
  <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6"
       role="dialog" aria-modal="true" aria-labelledby="modal-headline">
    <div>
      <div class="mt-3 text-center sm:mt-5">
        <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-headline">
          All done!
        </h3>
        <div class="mt-2">
          <p class="text-sm text-gray-500">
            <img src="/static/img/svg/undraw_celebration_0jvk.svg" alt="Options" class="w-2/3 md:w-1/2 mx-auto py-8">

            The inbox is now ready for use. Students will be able to create tickets to ask their questions.

          </p>
        </div>
      </div>
    </div>
    <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
      <button type="button" @click="$emit('click')"
              class="w-full inline-flex justify-center rounded-md px-4 py-2 bg-primary text-base font-medium text-white hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 sm:col-start-2 sm:text-sm">
        Finish
      </button>
      <button type="button" @click="$emit('cancel')"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:col-start-1 sm:text-sm">
        Back
      </button>
    </div>
  </div>
</template>

<script>
  export default {
    name: "WelcomeModal"
  }
</script>

<style scoped>

</style>