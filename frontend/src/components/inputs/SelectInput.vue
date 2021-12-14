<!-- This example requires Tailwind CSS v2.0+ -->
<template>
  <Listbox as="div" v-model="selected" @change="onChange">
    <ListboxLabel class="block text-sm font-medium text-gray-700">
      {{ label }}
    </ListboxLabel>
    <div class="mt-1 relative">
      <ListboxButton :disabled="disabled" class="relative w-full bg-white border border-gray-300 rounded-md pl-3 pr-10 py-2 text-left focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary sm:text-sm" :class="disabled ? 'cursor-not-allowed text-gray-400' : 'cursor-pointer'">
        <span class="flex items-center">
          <span v-if="selected?.color" class="flex-shrink-0 inline-block h-2 w-2 rounded-full mr-3" :style="`background-color: ${selected?.color}`" />
          <img
            v-if="selected?.avatar"
            :src="selected.avatar"
            alt=""
            class="flex-shrink-0 h-5 w-5 rounded-full"
          />
          <span :class="[selected?.avatar ? 'ml-3' : '', 'block truncate']">{{ selected?.name || emptyLabel }}</span>
        </span>
        <span
          class="ml-3 absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none"
        >
          <SelectorIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
        </span>
      </ListboxButton>

      <transition
        leave-active-class="transition ease-in duration-100"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <ListboxOptions
          class="absolute z-20 mt-1 bg-white shadow-lg max-h-56 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm "
        >
          <ListboxOption
            as="template"
            v-for="element in data"
            :key="element.value"
            :value="element"
            v-slot="{ active, selected }"
          >
            <li
              :class="[
                active ? 'text-white bg-primary-600' : 'text-gray-900',
                'cursor-pointer select-none relative py-2 pl-3 pr-9'
              ]"
            >
              <div class="flex items-center">
                <span v-if="element.color" class="flex-shrink-0 inline-block h-2 w-2 rounded-full mr-3" :style="`background-color: ${element.color}`" />
                <img
                  v-if="element.avatar"
                  :src="element.avatar"
                  alt=""
                  class="flex-shrink-0 h-6 w-6 rounded-full"
                />
                <span
                  :class="[
                    selected ? 'font-semibold' : 'font-normal',
                    element.avatar ? 'ml-3' : '',
                    'block truncate'
                  ]"
                >
                  {{ element.name }}
                </span>
              </div>

              <span
                v-if="selected"
                :class="[
                  active ? 'text-white' : 'text-primary-600',
                  'absolute inset-y-0 right-0 flex items-center pr-4'
                ]"
              >
                <CheckIcon class="h-5 w-5" aria-hidden="true" />
              </span>
            </li>
          </ListboxOption>
        </ListboxOptions>
      </transition>
    </div>
  </Listbox>
</template>

<script>
// import { ref } from 'vue'

import {
  Listbox,
  ListboxButton,
  ListboxLabel,
  ListboxOption,
  ListboxOptions
} from '@headlessui/vue'
import { CheckIcon, SelectorIcon } from '@heroicons/vue/solid'

export default {
  name: 'SelectInput',
  components: {
    Listbox,
    ListboxButton,
    ListboxLabel,
    ListboxOption,
    ListboxOptions,
    CheckIcon,
    SelectorIcon
  },
  props: {
    label: {
      required: false,
      type: String
    },
    data: {
      required: false,
      type: Array,
      default: () => []
    },
    init: {
      required: false,
      type: Object
    },
    multiple: {
      required: false,
      type: Boolean
    },
    emptyLabel: {
      required: false,
      type: String
    },
    modelValue: {
      required: false,
      type: Object
    },
    disabled: {
      default: false,
      required: false,
      type: Boolean
    }
  },
  data: () => ({
    selected: null
  }),
  methods: {
    onChange(event) {
      this.$emit('update:modelValue', event.value)
    }
  },
  watch: {
    modelValue: {
      immediate: true,
      handler(value) {
        this.selected = value
      }
    }
  }
}
</script>
