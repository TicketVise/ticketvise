<template>
  <div class="rounded-md bg-red-50 px-4 py-2">
    <div class="flex">
      <div class="flex-shrink-0">
        <XCircleIcon class="h-5 w-5 text-red-400" aria-hidden="true" />
      </div>
      <div class="ml-3">
        <h3 class="text-sm font-medium text-red-800">
          {{ message }}
        </h3>
      </div>
    </div>
  </div>
</template>

<script>
import { XCircleIcon } from '@heroicons/vue/solid'

export default {
  name: 'Error',
  components: {
    XCircleIcon
  },
  props: ['message']
}
</script>
