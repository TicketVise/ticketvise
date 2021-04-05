<template>
  <span class="inline-block bg-white border border-gray-200 rounded-full px-2 py-1 text-xs font-medium text-gray-700"
        style="line-height: 1 !important;">
    <div class="flex flex-row items-center">
    <div :style="style" class="w-2 h-2 rounded-full flex-col mr-1" v-if="background"></div>
    <slot></slot>
    </div>
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
        style: {
          backgroundColor: this.background,
        },
      }
    }
  }
</script>

<style>

</style>
