<template>
  <div v-if="page" class="flex-1 flex items-center justify-between">
    <div>
      <p class="text-sm leading-5 text-gray-700">
        Showing
        <span class="font-medium">{{ (page.page_number - 1) * page.page_size + 1 }}</span>
        to
        <span class="font-medium">{{ (page.page_number - 1) * page.page_size + page.results.length }}</span>
        of
        <span class="font-medium">{{ page.count }}</span>
        results
      </p>
    </div>
    <div v-if="page.previous || page.next">
      <nav class="relative z-0 inline-flex shadow-sm">
        <button type="button" v-if="page.previous" @click="$emit('go', 1)"
                class="-ml-px relative inline-flex items-center rounded-l-md px-4 py-2 border border-gray-300 bg-white text-sm leading-5 font-medium text-gray-700 hover:text-gray-500 focus:z-10 focus:outline-none focus:border-blue-300 focus:ring-blue active:bg-gray-100 active:text-gray-700 transition ease-in-out duration-150">
          1
        </button>
        <span v-if="page.previous"
              class="-ml-px relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm leading-5 font-medium text-gray-700">
          ...
        </span>
        <button type="button" v-if="page.previous" @click="$emit('go', page.page_number - 1)"
                class="-ml-px relative inline-flex items-center px-2 py-2 border border-gray-300 bg-white text-sm leading-5 font-medium text-gray-500 hover:text-gray-400 focus:z-10 focus:outline-none focus:border-blue-300 focus:ring-blue active:bg-gray-100 active:text-gray-500 transition ease-in-out duration-150"
                aria-label="Previous" v-bind:class="{'rounded-l-md' : !page.hasOwnProperty('previous')}">
          <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd"
                  d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
                  clip-rule="evenodd"/>
          </svg>
        </button>
        <span
            class="-ml-px relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm leading-5 font-medium text-gray-700"
            v-bind:class="{'rounded-l-md' : !page.previous, 'rounded-r-md' : !page.next}">
          {{ page.page_number }}
        </span>
        <button type="button" v-if="page.next" @click="$emit('go', page.page_number + 1)"
                class="-ml-px relative inline-flex items-center px-2 py-2 border border-gray-300 bg-white text-sm leading-5 font-medium text-gray-500 hover:text-gray-400 focus:z-10 focus:outline-none focus:border-blue-300 focus:ring-blue active:bg-gray-100 active:text-gray-500 transition ease-in-out duration-150"
                aria-label="Next" v-bind:class="{'rounded-r-md' : !page.hasOwnProperty('next')}">
          <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd"
                  d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                  clip-rule="evenodd"/>
          </svg>
        </button>
        <span v-if="page.next"
              class="-ml-px relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm leading-5 font-medium text-gray-700">
          ...
        </span>
        <button type="button" v-if="page.next" @click="$emit('go', page.total_pages)"
                class="-ml-px relative inline-flex items-center rounded-r-md px-4 py-2 border border-gray-300 bg-white text-sm leading-5 font-medium text-gray-700 hover:text-gray-500 focus:z-10 focus:outline-none focus:border-blue-300 focus:ring-blue active:bg-gray-100 active:text-gray-700 transition ease-in-out duration-150">
          {{ page.total_pages }}
        </button>
      </nav>
    </div>
  </div>

</template>

<script>
export default {
  name: "Pagination",
  props: {
    page: {
      required: true
    }
  }
}
</script>

<style scoped>

</style>
