<template>
  <span class="inline-block bg-gray-200 rounded-full px-2 py-1 text-xs font-semibold text-gray-700"
        style="line-height: 1 !important;" :style="bgColor">
    <slot></slot>
  </span>
</template>

<script>
  export default {
    props: {
      background: {
        type: String,
        default: null,
        required: false
      }
    },
    data() {
      return {
        bgColor: {
          backgroundColor: this.background
        }
      }
    }
  }
</script>

<style>

</style>
