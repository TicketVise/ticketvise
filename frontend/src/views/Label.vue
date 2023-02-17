<template>
  <div class="w-full h-full overflow-auto">
    <div class="relative w-full max-w-screen-lg mx-auto bg-white h-full">
      <div v-if="label">
        <div class="px-4 py-3 sm:gap-4 sm:px-6 border-b">
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            Label
          </h3>
          <p class="mt-1 max-w-2xl text-sm leading-5 text-gray-500">
            Manage properties related to a label.
          </p>
        </div>
        <div class="px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm leading-5 font-medium text-gray-700 flex items-center">
            Name
          </dt>
          <dd class="mt-1 text-sm leading-5 text-gray-900 sm:mt-0 sm:col-span-2">
            <input type="text" v-model="label.name"
                  class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow-sm leading-tight focus:outline-none focus:ring"
                  :class="{'mb-2 border-red-600 hover:border-red-700 ' : !label.name }">

            <p v-if="!label.name && !window.location.hash.includes('new')" class="text-sm text-red-600">Omschrijving is verplicht</p>
          </dd>
        </div>
        <div class="px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <dt class="text-sm leading-5 font-medium text-gray-700 flex items-center">
            Color
          </dt>
          <dd class="mt-1 text-sm leading-5 text-gray-900 sm:mt-0 sm:col-span-2">
            <input type="color" v-model="label.color"
                  class="block appearance-none w-full bg-white border-none overflow-hidden leading-tight focus:outline-none">
          </dd>
        </div>
        <div class="px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
          <label for="is_visible_to_guest" class="text-sm leading-5 font-medium text-gray-700 flex items-center">
            Visible for students
          </label>
          <dd class="mt-1 text-sm leading-5 text-gray-900 sm:mt-0 sm:col-span-2">
            <input type="checkbox" class="block" v-model="label.is_visible_to_guest">
          </dd>
        </div>
        <div class="px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 border-b">
          <label for="is_active" class="text-sm leading-5 font-medium text-gray-700 flex items-center">
            Enabled
          </label>
          <dd class="mt-1 text-sm leading-5 text-gray-900 sm:mt-0 sm:col-span-2">
            <input type="checkbox" class="block" v-model="label.is_active">
          </dd>
        </div>
      </div>

      <div class="p-2 px-4 sm:pr-0 flex space-x-2 sm:mx-4 justify-end">
        <button type="button" @click="onCancel()"
                class="group inline-flex items-center px-4 py-2 border border-gray-300 text-sm leading-5 font-medium rounded-md text-gray-700 bg-white hover:text-gray-500 focus:outline-none focus:ring-blue focus:border-blue-300 active:text-gray-800 active:bg-gray-50">
          Cancel
        </button>
        <button type="button" @click="onSave()"
                class="group inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm leading-5 font-medium rounded-md bg-green-200 text-green-700 hover:bg-green-100 focus:outline-none focus:ring-indigo focus:border-green-700 active:bg-green-700 ">
          Save
        </button>
      </div>

      <div v-if="label && label.id" class="bg-white overflow-hidden mt-4 px-4 py-5 border-t">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Remove label
        </h3>
        <p class="mt-1 max-w-2xl text-sm leading-5 text-gray-500">
          When removing a label, the label will be removed from all ticket associated with it.
          This action in irreversible.
        </p>
        <button type="button" @click="onDelete()"
                class="group relative w-full sm:w-auto mt-4 inline-flex justify-center items-center rounded-md border border-transparent px-4 py-2 bg-red-200 text-red-600 co text-base leading-6 font-medium shadow-sm hover:bg-red-100 focus:outline-none focus:border-red-700 focus:ring-red transition ease-in-out duration-150 sm:text-sm sm:leading-5">
          Remove
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import router from '@/router'

export default {
  name: 'Label',
  data () {
    return {
      window: window,
      label: null,
      colors: [
        '#686F7D',
        '#6B7280',
        '#EC5050',
        '#F05252',
        '#FF5A1F',
        '#C27803',
        '#0E9F6E',
        '#0694A2',
        '#3F83F8',
        '#6875F5',
        '#9061F9'
      ]
    }
  },
  mounted () {
    if (this.$route.params.labelId === 'new') {
      this.label = {
        id: null,
        name: '',
        color: this.colors[Math.floor(Math.random() * this.colors.length)],
        is_visible_to_guest: true,
        is_active: true
      }
    } else {
      const { inboxId, labelId } = this.$route.params

      axios.get(`/api/inboxes/${inboxId}/labels/${labelId}`).then(response => {
        this.label = response.data
      })
    }
  },
  methods: {
    onSave () {
      const { inboxId, labelId } = this.$route.params

      if (this.label.id) {
        axios.put(`/api/inboxes/${inboxId}/labels/${labelId}`, this.label).then(() => {
          router.push({ name: 'Labels', params: { inboxId: inboxId } })
        })
      } else {
        axios.post(`/api/inboxes/${inboxId}/labels/${labelId}`, this.label).then(() => {
          router.push({ name: 'Labels', params: { inboxId: inboxId } })
        })
      }
    },
    onCancel () {
      router.push({ name: 'Labels', params: { inboxId: this.$route.params.inboxId } })
    },
    onDelete () {
      const { inboxId, labelId } = this.$route.params

      if (confirm('Are you sure you want to delete this label?')) {
        axios.delete(`/api/inboxes/${inboxId}/labels/${labelId}`).then(_ => {
          router.push({ name: 'Labels', params: { inboxId: inboxId } })
        })
      }
    }
  }
}
</script>
