<template>
  <div class="rounded-md border">
    <div
      v-if="!open"
      @click="open = true"
      class="py-3 px-4 flex space-x-2 items-center cursor-pointer rounded hover:bg-gray-100"
    >
      <i class="h-4 w-4 rounded bg-gray-600"></i>
      <span class="font-medium">{{ selected }}</span>
    </div>
    <div v-else class="py-3 px-4 space-y-2">
      <div class="flex justify-between w-full">
        <span class="font-medium">Default ticket assignment</span>
        <x-icon @click="open = false" class="h-4 w-4 cursor-pointer" />
      </div>
      <div class="space-y-2">
        <div>
          <label id="listbox-label" class="block text-sm leading-5 font-medium text-primary">
            Scheduling Algorithm
          </label>
          <div class="relative">
            <span
              class="inline-block w-full rounded-md"
              @click="dropdown_algorithm = !dropdown_algorithm"
            >
              <button
                type="button"
                aria-haspopup="listbox"
                aria-expanded="true"
                aria-labelledby="listbox-label"
                class="cursor-pointer relative w-full rounded-md border border-gray-300 bg-white pl-3 pr-10 py-2 text-left focus:outline-none focus:shadow-outline-primary focus:border-primary-300 transition ease-in-out duration-150 sm:text-sm sm:leading-5"
              >
                <div class="flex items-center space-x-3">
                  <span
                    class="block truncate text-gray-800"
                    v-text="selected"
                  ></span>
                </div>
                <span
                  class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none"
                >
                  <svg
                    class="h-5 w-5 text-gray-400"
                    viewBox="0 0 20 20"
                    fill="none"
                    stroke="currentColor"
                  >
                    <path
                      d="M7 7l3-3 3 3m0 6l-3 3-3-3"
                      stroke-width="1.5"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                  </svg>
                </span>
              </button>
            </span>

            <!-- Select popover, show/hide based on select state. -->
            <div
              class="absolute mt-1 w-full rounded-md bg-white shadow-lg"
              v-if="dropdown_algorithm"
            >
              <ul
                tabindex="-1"
                role="listbox"
                aria-labelledby="listbox-label"
                aria-activedescendant="listbox-item-3"
                class="max-h-56 rounded-md py-1 text-base leading-6 shadow-xs overflow-auto focus:outline-none sm:text-sm sm:leading-5"
              >
                <li
                  id="listbox-item-0"
                  role="option"
                  v-for="item in items"
                  :key="item"
                  class="text-gray-900 cursor-pointer select-none relative py-2 pl-3 pr-9 hover:text-white hover:bg-primary"
                  :class="{ 'bg-orange-200': item == selected }"
                  @click="selected = item"
                >
                  <div class="flex items-center space-x-3">
                    <span
                      class="font-normal block truncate"
                      :class="{ 'font-semibold': item == selected }"
                      v-text="item"
                    ></span>
                  </div>
                  <span
                    class="absolute inset-y-0 right-0 flex items-center pr-4"
                    v-if="item == selected"
                  >
                    <svg
                      class="h-5 w-5 text-orange-600"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clip-rule="evenodd"
                      />
                    </svg>
                  </span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Divider -->
        <div class="w-full border-b my-2"></div>

        <!-- Buttons -->
        <div class="flex justify-end space-x-2">
          <button
            @click="cancel"
            class="rounded border px-4 py-2 focus:outline-none hover:bg-gray-100"
          >
            Cancel
          </button>
          <button
            @click="cancel"
            class="rounded border px-4 py-2 border-green-400 bg-green-300 focus:outline-none hover:bg-green-200"
          >
            Save
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  XIcon
} from '@heroicons/vue/solid'
export default {
  components: { XIcon },
  data: () => ({
    open: false,
    dropdown_algorithm: false,
    items: ['Round Robin', 'Least Assigned First', 'Nothing'],
    selected: 'Least Assigned First'
  }),
  methods: {
    away () {
      this.dropdown_algorithm = false
    },
    cancel () {
      this.open = false
    }
  }
}
</script>
