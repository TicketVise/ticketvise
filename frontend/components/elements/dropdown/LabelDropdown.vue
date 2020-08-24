<template>
  <!-- <select v-on:input="updateValue($event.target.value)"
          class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline">
      <option>Add label</option>
      <option :value="item.id" v-for="item in values" :key="item.id">{{item.name}}</option>
  </select> -->
  <div class="space-y-1">
    <div class="relative">
                <span class="inline-block w-full rounded-md shadow-sm" @click="open = !open">
                    <button aria-expanded="true" aria-haspopup="listbox" aria-labelledby="listbox-label" class="cursor-pointer relative w-full rounded-md border border-gray-300 bg-white pl-3 pr-10 py-2 text-left focus:outline-none transition ease-in-out duration-150 sm:text-sm sm:leading-5"
                            tabindex="-1"
                            type="button">
                        <div class="flex items-center space-x-3">
                            <span class="block truncate">Select labels</span>
                        </div>
                        <span class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
                            <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="none" stroke="currentColor">
                                <path d="M7 7l3-3 3 3m0 6l-3 3-3-3" stroke-linecap="round" stroke-linejoin="round"
                                      stroke-width="1.5"/>
                            </svg>
                        </span>
                    </button>
                </span>

      <div class="absolute mt-1 w-full rounded-md bg-white shadow-lg" v-if="open">
        <ul aria-activedescendant="listbox-item-3" aria-labelledby="listbox-label" class="max-h-56 rounded-md py-1 text-base leading-6 shadow-xs overflow-auto focus:outline-none sm:text-sm sm:leading-5" role="listbox"
            tabindex="-1">
          <li :key="item.id" :value="item.id" @click="switchItem(item)" class="text-gray-900 hover:text-white hover:bg-orange-400 cursor-pointer select-none relative py-2 pl-3 pr-9" id="listbox-item-0"
              role="option"
              v-for="item in values">
            <div class="flex items-center space-x-3">
              <div :style="`background-color: ${item.color};`" class="w-2 h-2 rounded-full"></div>
              <span :class="{ 'font-semibold': selected.includes(item) }" class="font-normal block truncate">{{ item.name }}</span>
            </div>
            <span class="absolute inset-y-0 right-0 flex items-center pr-4" v-if="selected.includes(item)">
                                <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                    <path clip-rule="evenodd"
                                          d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                          fill-rule="evenodd"/>
                                </svg>
                            </span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "Dropdown",
    props: ["values"],
    data: () => ({
      open: false,
      selected: []
    }),
    methods: {
      // updateValue: function (value) {
      //     const selected = this.values.filter(label => label.id === parseInt(value))[0]
      //     this.$emit('input', selected)
      // }
      switchItem(value) {
        if (this.selected.includes(value))
          this.$delete(this.selected, this.selected.indexOf(value))
        else
          this.selected.push(value)

        this.$emit('update', this.selected)
      },
      away() {
        this.open = false
      }
    }
  }
</script>

<style scoped>

</style>
