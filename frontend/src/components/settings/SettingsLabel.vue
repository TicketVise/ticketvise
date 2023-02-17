<template>
  <div class="h-full w-full overflow-y-auto">
    <div class="relative mx-auto h-full w-full max-w-screen-lg bg-white">
      <div class="border-b pb-2">
        <h2 class="text-lg leading-6 font-medium text-gray-900">Label</h2>
        <p class="mt-1 text-sm text-gray-500">
          Manage properties of the label.
        </p>
      </div>
      <div class="py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
        <dt class="flex items-center text-sm font-medium leading-5 text-gray-700">Name</dt>
        <dd class="mt-1 text-sm leading-5 text-gray-900 sm:col-span-2 sm:mt-0">
          <input type="text" v-model="label.name" class="block w-full appearance-none rounded border border-gray-400 bg-white px-4 py-2 pr-8 leading-tight shadow-sm hover:border-gray-500 focus:outline-none" :class="{ 'mb-2 border-red-600 hover:border-red-700 ': !label.name && this.$route.params.itemId != 'new' }" />

          <p v-if="!label.name && this.$route.params.itemId != 'new'" class="text-sm text-red-600">Omschrijving is verplicht</p>
        </dd>
      </div>
      <div class="py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
        <dt class="flex items-center text-sm font-medium leading-5 text-gray-700">Color</dt>
        <dd class="mt-1 text-sm leading-5 text-gray-900 sm:col-span-2 sm:mt-0">
          <input type="color" v-model="label.color" class="block w-full appearance-none overflow-hidden border-none bg-white leading-tight focus:outline-none" />
          <!-- <RadioGroup v-model="label.color" class="px-2">
            <div class="flex items-center space-x-3">
              <RadioGroupOption as="template" v-for="color in colors" :key="color.name" :value="color" v-slot="{ active, checked }">
                <div :class="[color.selectedColor, active && checked ? 'ring ring-offset-1' : '', !active && checked ? 'ring-2' : '', '-m-0.5 relative p-0.5 rounded-full flex items-center justify-center cursor-pointer focus:outline-none']">
                  <RadioGroupLabel as="span" class="sr-only">{{ color.name }}</RadioGroupLabel>
                  <span aria-hidden="true" :class="[color.bgColor, 'h-5 w-5 border border-black border-opacity-10 rounded-full']" />
                </div>
              </RadioGroupOption>
            </div>
          </RadioGroup> -->
        </dd>
      </div>
      <div class="py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
        <label for="is_visible_to_guest" class="flex items-center text-sm font-medium leading-5 text-gray-700"> Visible for students </label>
        <dd class="mt-1 text-sm leading-5 text-gray-900 sm:col-span-2 sm:mt-0">
          <input type="checkbox" class="block" v-model="label.is_visible_to_guest" />
        </dd>
      </div>
      <div class="border-b py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
        <label for="is_active" class="flex items-center text-sm font-medium leading-5 text-gray-700"> Enabled </label>
        <dd class="mt-1 text-sm leading-5 text-gray-900 sm:col-span-2 sm:mt-0">
          <input type="checkbox" class="block" v-model="label.is_active" />
        </dd>
      </div>

      <div class="flex justify-end space-x-2 p-2 px-4 sm:mx-4 sm:pr-0">
        <router-link type="button" :to="{ name: 'Settings', params: { inboxId: this.$route.params.inboxId, tab: 'labels' } }" class="focus:ring-blue group inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium leading-5 text-gray-700 hover:text-gray-500 focus:border-blue-300 focus:outline-none active:bg-gray-50 active:text-gray-800">Cancel</router-link>
        <button type="button" @click="onDelete()" class="focus:ring-red group relative inline-flex items-center justify-center rounded-md border border-transparent bg-red-200 px-4 py-2 text-base font-medium leading-6 text-red-600 shadow-sm transition duration-150 ease-in-out hover:bg-red-100 focus:border-red-700 focus:outline-none sm:w-auto sm:text-sm sm:leading-5">Remove</button>
        <button type="button" @click="onSave()" class="focus:ring-indigo group inline-flex items-center justify-center rounded-md border border-transparent bg-green-200 px-4 py-2 text-sm font-medium leading-5 text-green-700 hover:bg-green-100 focus:border-green-700 focus:outline-none active:bg-green-700">Save</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import router from '@/router'

import { RadioGroup, RadioGroupLabel, RadioGroupOption } from '@headlessui/vue'

const colors = [
  { name: 'Pink', bgColor: 'bg-pink-500', selectedColor: 'ring-pink-500' },
  { name: 'Purple', bgColor: 'bg-purple-500', selectedColor: 'ring-purple-500' },
  { name: 'Blue', bgColor: 'bg-blue-500', selectedColor: 'ring-blue-500' },
  { name: 'Green', bgColor: 'bg-green-500', selectedColor: 'ring-green-500' },
  { name: 'Yellow', bgColor: 'bg-yellow-500', selectedColor: 'ring-yellow-500' },
]

export default {
  name: 'Label',
  components: {
    RadioGroup,
    RadioGroupLabel,
    RadioGroupOption
  },
  data: () => ({
    window: window,
    label: {
      color: colors[0]
    },
    // colors
    colors: ['#686F7D', '#6B7280', '#EC5050', '#F05252', '#FF5A1F', '#C27803', '#0E9F6E', '#0694A2', '#3F83F8', '#6875F5', '#9061F9']
  }),
  mounted() {
    if (this.$route.params.labelId === 'new') {
      this.label = {
        id: null,
        name: '',
        color: this.colors[Math.floor(Math.random() * this.colors.length)],
        is_visible_to_guest: true,
        is_active: true
      }
    } else {
      const { inboxId, itemId } = this.$route.params

      axios.get(`/api/inboxes/${inboxId}/labels/${itemId}`).then((response) => {
        this.label = response.data
      })
    }
  },
  methods: {
    onSave() {
      const { inboxId, itemId } = this.$route.params

      if (this.label.id) {
        axios.put(`/api/inboxes/${inboxId}/labels/${itemId}`, this.label).then(() => {
          router.push({ name: 'Labels', params: { inboxId: inboxId } })
        })
      } else {
        axios.post(`/api/inboxes/${inboxId}/labels/${itemId}`, this.label).then(() => {
          router.push({ name: 'Labels', params: { inboxId: inboxId } })
        })
      }
    },
    onDelete() {
      const { inboxId, itemId } = this.$route.params

      if (confirm('Are you sure you want to delete this label?')) {
        axios.delete(`/api/inboxes/${inboxId}/labels/${itemId}`).then((_) => {
          router.push({ name: 'Labels', params: { inboxId: inboxId } })
        })
      }
    }
  }
}
</script>
