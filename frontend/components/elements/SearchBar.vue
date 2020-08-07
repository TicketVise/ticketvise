<template>
  <div>
    <card class="flex" outlined>
      <i class="fa fa-search cursor-pointer p-1"></i>
      <input class="flex-grow m-2" v-model="search" placeholder="Search" @keyup="emitValue">
    </card>
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