<template>
  <li class="mr-1">
    <a @click.prevent="$emit('click')" class="bg-white inline-block py-2 px-4 text-gray-500 hover:text-gray-800 font-semibold"
       href="#"
       v-bind:class="{ 'border-b-2 border-orange-400 text-gray-700': active}">
      {{ title }}
      <span class="ml-1 px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-200 text-gray-800"
            v-if="badge">
                {{ badge }}
            </span>
    </a>
  </li>
</template>

<script>
  export default {
    props: {
      active: {
        type: Boolean,
        default: false
      },
      title: {
        type: String,
        required: true
      },
      badge: {
        required: false
      }
    }
  }
</script>

<style>

</style>
