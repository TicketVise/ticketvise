<!-- This example requires Tailwind CSS v2.0+ -->
<template>
  <Listbox as="div" v-model="selected">
    <ListboxLabel class="block text-sm font-medium text-gray-700">
      {{ label }}
    </ListboxLabel>
    <div class="mt-1 relative">
      <ListboxButton
        class="relative w-full bg-white border border-gray-300 rounded-md pl-3 pr-10 py-2 text-left cursor-default focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary sm:text-sm"
      >
        <span class="flex items-center">
          <img
            v-if="selected?.avatar"
            :src="selected.avatar"
            alt=""
            class="flex-shrink-0 h-5 w-5 rounded-full"
          />
          <span :class="[selected?.avatar ? 'ml-3' : '', 'block truncate']">{{ selected?.name }}</span>
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
          class="absolute z-10 mt-1 bg-white shadow-lg max-h-56 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm"
        >
          <ListboxOption
            as="template"
            v-for="element in data"
            :key="element.id"
            :value="element"
            v-slot="{ active, selected }"
          >
            <li
              :class="[
                active ? 'text-white bg-primary-600' : 'text-gray-900',
                'cursor-default select-none relative py-2 pl-3 pr-9'
              ]"
            >
              <div class="flex items-center">
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
import { ref } from 'vue'
import {
  Listbox,
  ListboxButton,
  ListboxLabel,
  ListboxOption,
  ListboxOptions
} from '@headlessui/vue'
import { CheckIcon, SelectorIcon } from '@heroicons/vue/solid'

export default {
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
      required: true,
      type: Array
    },
    init: {
      required: true,
      type: Object
    }
  },
  data () {
    return {
      selected: null
    }
  },
  mounted () {
    const selected = ref(this.init)

    this.selected = selected
  }
}
</script>
