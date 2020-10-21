<template>
  <div class="space-y-1 h-10" v-on-clickaway="away">
    <div class="relative">
      <span class="inline-block w-full rounded" @click="open = !open">
        <button
          aria-expanded="true" aria-haspopup="listbox" aria-labelledby="listbox-label"
          class="h-10 cursor-pointer relative w-full rounded-md border border-gray-300 bg-white pl-3 pr-10 py-2 text-left focus:outline-none transition ease-in-out duration-150"
          tabindex="-1"
          type="button"
        >
          <div class="flex items-center space-x-3">
            <span v-if="!multiple || (multiple && selected.length === 0)" class="block truncate">
              {{ multiple ? ((items && items.length) ? ((selected && selected.length) ? '' : (emptyMsg || 'Select items')) : 'No items available') : ((items && items.length) ? ((selected && selected.length) ? items[selected[0]] : (emptyMsg || 'Select item')) : 'No items available') }}
            </span>
            <div v-else class="flex items-center space-x-1 w-full overflow-hidden">
              <span class="border rounded px-1 text-xs whitespace-no-wrap" v-for="item in selected" :key="item">
                {{ items[item].name || items[item] }}
              </span>
            </div>
          </div>
          <span class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="none" stroke="currentColor">
              <path
                d="M7 7l3-3 3 3m0 6l-3 3-3-3"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1.5"
              />
            </svg>
          </span>
        </button>
      </span>

      <div class="absolute mt-1 w-full rounded bg-white shadow-lg z-10" v-if="open && items && items.length">
        <ul aria-activedescendant="listbox-item-3" aria-labelledby="listbox-label"
            class="max-h-56 rounded-md py-1 text-base leading-6 shadow-xs overflow-auto focus:outline-none sm:text-sm sm:leading-5"
            role="listbox"
            tabindex="-1">
          <li :key="index" :value="item" @click="switchItem(index)"
              class="text-gray-900 hover:text-white hover:bg-orange-400 cursor-pointer select-none relative py-2 pl-3 pr-9"
              id="listbox-item-0"
              role="option"
              v-for="(item, index) in items">
            <div class="flex items-center space-x-3">
              <div v-if="item.color" :style="`background-color: ${item.color};`" class="w-2 h-2 rounded-full"></div>
              <span :class="{ 'font-semibold': containsObject(selected, index) }"
                    class="font-normal block truncate">{{ item.name || item }}</span>
            </div>
            <span class="absolute inset-y-0 right-0 flex items-center pr-4" v-if="containsObject(selected, index)">
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
import { mixin as clickaway } from 'vue-clickaway'

export default {
  name: "Select",
  mixins: [ clickaway ],
  props: {
    items: {
      default: () => []
    },
    selected: {
      default: () => []
    },
    multiple: {
      type: Boolean,
      required: false,
      default: false
    },
    emptyMsg: {
      type: String,
      required: false,
      default: ''
    }
  },
  data: () => ({
    open: false
  }),
  methods: {
    switchItem(value) {
      if (this.multiple && this.containsObject(this.selected, value))
        this.selected.splice(this.selected.findIndex(e => e === value), 1)
      else if (this.multiple)
        this.selected.push(value)
      else if (this.containsObject(this.selected, value))
        this.open = false
      else {
        this.selected[0] = value
        this.open = false
      }

      this.$emit("input", this.selected)
    },
    away() {
      this.open = false
    },
    containsObject(list, id) {
      return list && list.some(i => i === id)
    }
  }
}
</script>
