<template>
  <div>
    <label v-if="label" :text="label" class="block text-xs leading-5 font-medium text-orange-500"></label>
    <input
      :type="type"
      class="border rounded w-full focus:outline-none h-10 px-3 py-2"
    />
  </div>
</template>

<script>
export default {
  props: {
    type: {
      type: String,
      required: false,
      default: 'text'
    },
    label: {
      type: String,
      required: false,
      default: ''
    }
  }
}
</script>