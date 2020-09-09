<template>
  <div class="space-y-1" @click="open = !open">
    <div class="relative">
      <span class="inline-block w-full rounded-md shadow-sm" @click="open = !open">
        <button aria-expanded="true" aria-haspopup="listbox" aria-labelledby="listbox-label"
                class="cursor-pointer relative w-full rounded-md border border-gray-300 bg-white pl-3 pr-10 py-2 text-left focus:outline-none transition ease-in-out duration-150 sm:text-sm sm:leading-5"
                tabindex="-1"
                type="button">
          <div class="flex items-center space-x-3">
            <span class="block truncate">{{ values && values.length ? "Select labels" : "No labels available" }}</span>
          </div>
          <span class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="none" stroke="currentColor">
                <path d="M7 7l3-3 3 3m0 6l-3 3-3-3" stroke-linecap="round" stroke-linejoin="round"
                      stroke-width="1.5"/>
            </svg>
          </span>
        </button>
      </span>

      <div class="absolute mt-1 w-full rounded-md bg-white shadow-lg z-50" v-if="open && values && values.length">
        <ul aria-activedescendant="listbox-item-3" aria-labelledby="listbox-label"
            class="max-h-56 rounded-md py-1 text-base leading-6 shadow-xs overflow-auto focus:outline-none sm:text-sm sm:leading-5"
            role="listbox"
            tabindex="-1">
          <li :key="item.id" :value="item.id" @click="switchItem(item)"
              class="text-gray-900 hover:text-white hover:bg-orange-400 cursor-pointer select-none relative py-2 pl-3 pr-9"
              id="listbox-item-0"
              role="option"
              v-for="item in values">
            <div class="flex items-center space-x-3">
              <div :style="`background-color: ${item.color};`" class="w-2 h-2 rounded-full"></div>
              <span :class="{ 'font-semibold': containsObject(labels, item.id) }" class="font-normal block truncate">{{ item.name }}</span>
            </div>
            <span class="absolute inset-y-0 right-0 flex items-center pr-4" v-if="containsObject(labels, item.id)">
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
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
    props: ["values", "selected"],
    data: () => ({
      open: false,
      labels: []
    }),
    created() {
      this.labels = this.selected ? this.selected : []
    },
    methods: {
      switchItem(value) {
        if (this.containsObject(this.labels, value.id))
          this.labels.splice(this.labels.findIndex(e => e.id === value.id), 1);
        else
          this.labels.push(value);

        this.$emit("input", this.labels)
      },
      away() {
        this.open = false
      },
      containsObject(list, id) {
        return list && list.some(e => e.id === id);
      }
    }
  }
</script>

<style scoped>

</style>
