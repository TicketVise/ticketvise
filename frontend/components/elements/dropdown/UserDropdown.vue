<template>
  <div class="inline-block relative w-full">
    <select class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded leading-tight focus:outline-none cursor-pointer"
            v-on:input="updateValue($event.target.value)">
      <option :value="null">Choose assignee</option>
      <option :key="item.id" :selected="value != null && value.id === item.id" :value="item.id" v-for="item in values">
        {{item.first_name}} {{item.last_name}}
      </option>
    </select>

    <span class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="none"
                 stroke="currentColor">
                <path d="M7 7l3-3 3 3m0 6l-3 3-3-3" stroke-width="1.5" stroke-linecap="round"
                      stroke-linejoin="round"/>
            </svg>
        </span>
  </div>
</template>

<script>
  export default {
    name: "Dropdown",
    props: {
      value: {
        type: Object,
      }, values: {
        required: true
      },
    },
    methods: {
      updateValue: function (value) {
        const selected = this.values.filter(user => user.id === parseInt(value))[0];
        this.$emit('input', selected)
      }
    }
  }
</script>

<style scoped>

</style>
