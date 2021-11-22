<template>
  <div
    class="rounded border-l-4 border-red-600 bg-red-100 text-red-600 p-1 flex items-center"
    role="alert"
  >
    <i class="fa fa-exclamation mr-2 self-start p-1"></i>
    <p class="text-sm md:text-base text-red-700">{{ message }}</p>
  </div>
</template>

<script>
export default {
  name: 'error',
  props: ['message']
}
</script>
