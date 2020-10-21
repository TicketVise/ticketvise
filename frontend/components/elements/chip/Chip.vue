<template>
  <span
    class="inline-block px-2 py-1 text-xs font-semibold text-gray-700"
    :class="{ 'rounded-full': rounded, 'rounded': !rounded, 'border bg-white': outlined, 'bg-gray-200': !outlined }"
    style="line-height: 1 !important;"
  >
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
      },
      rounded: {
        type: Boolean,
        default: true,
        required: false
      },
      outlined: {
        type: Boolean,
        default: false,
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
