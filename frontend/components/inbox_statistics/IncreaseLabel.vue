<template>
  <span v-if="b !== 0" class="px-2 py-1 text-sm rounded-full"
        :class="{
          'bg-green-200 text-green-700': value < 0,
          'bg-red-200 text-red-700': value > 0,
          'bg-gray-200 text-gray-700': value === 0,
        }">
    <i v-if="value > 0" class="fa fa-arrow-up"></i>
    <i v-else-if="value < 0" class="fa fa-arrow-down"></i>
    <i v-else class="fa fa-minus"></i>
    <span class="ml-2 font-medium ">
      {{ value }}
    </span>
  </span>

</template>

<script>
export default {
  name: "IncreaseLabel",
  props: {
    a: {
      required: true,
      type: Number
    },
    b: {
      required: true,
      type: Number
    }
  },
  computed: {
    value: function () {
      if (this.b === 0)
        return .0.toFixed(2);

      return ((this.a / this.b) * 100).toFixed(2)
    }
  }
}
</script>

<style scoped>

</style>