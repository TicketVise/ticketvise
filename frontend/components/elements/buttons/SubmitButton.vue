<template>
  <button @click="$emit('click')"
          class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm leading-5 font-medium rounded-md focus:outline-none focus:shadow-outline-orange hover:bg-orange-500 hover:text-white transition duration-150 ease-in-out">
    <slot></slot>
    {{text}}
  </button>
</template>

<script>
  export default {
    name: "SubmitButton",
    props: ["text"],
  }
</script>

<style scoped>

</style>
