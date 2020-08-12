<template>
  <div class="shadow flex border border-gray-300 rounded-md overflow-hidden mr-2">
    <input class="flex-grow w-full p-2 mx-1" v-model="search" placeholder="Search" @keyup="emitValue">
    <button class="bg-white w-auto flex justify-end items-center text-gray-600 p-2 hover:text-gray-500" @click="emitValue">
      <i class="fa fa-search"></i>
    </button>
  </div>
</template>

<script>
export default {
  name: "SearchBar",
  props: ["value"],
  data() {
    return {
      search: "",
    }
  },
  methods: {
    emitValue() {
      this.$emit('input', this.search)
    }
  }
}
</script>

<style scoped>

</style>