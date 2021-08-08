<template>
  <div class="rounded overflow-hidden shadow-lg bg-white"
       v-bind:class="{ 'shadow-none border border-gray-300': outlined, 'shadow-none': flat}">
    <slot></slot>
  </div>
</template>

<script>
  export default {
    props: {
      outlined: {
        type: Boolean,
        required: false,
        default: false
      },
      flat: {
        type: Boolean,
        required: false,
        default: false
      }
    }
  }
</script>

<style>

</style>
