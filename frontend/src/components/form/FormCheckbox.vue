<template>
  <div class="flex items-center">
    <input id="remember_me" name="remember_me" type="checkbox" class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded" :checked="checked" />
    <label for="remember_me" class="ml-2 block text-sm text-gray-900" :text="label" />
  </div>
</template>

<script>
export default {
  name: 'FormCheckbox',
  props: {
    label: {
      type: String,
      required: false,
      default: ''
    },
    checked: {
      type: Boolean,
      required: false,
      default: false
    }
  }
}
</script>

<style>

</style>