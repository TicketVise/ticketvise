<template>
  <div class="container mx-auto max-w-3xl">
    <div v-if="label" class="sm:mt-4">
      <div class="bg-gray-50 px-4 py-3 sm:gap-4 sm:px-6 border-b-2 hidden sm:block">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Label
        </h3>
        <p class="mt-1 max-w-2xl text-sm leading-5 text-gray-500">
          Manage properties related to a label.
        </p>
      </div>
      <div class="bg-gray-50 px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 border-b-2">
        <dt class="text-sm leading-5 font-medium text-gray-700 flex items-center">
          Name
        </dt>
        <dd class="mt-1 text-sm leading-5 text-gray-900 sm:mt-0 sm:col-span-2">
          <input type="text" v-model="label.name"
                 class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow-sm leading-tight focus:outline-none focus:shadow-outline"
                 :class="{'mb-2 border-red-600 hover:border-red-700 ' : !label.name }" autofocus>

          <p v-if="!label.name" class="text-sm text-red-600">Omschrijving is verplicht</p>
        </dd>
      </div>
      <div class="bg-gray-50 px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 border-b-2">
        <dt class="text-sm leading-5 font-medium text-gray-700 flex items-center">
          Color
        </dt>
        <dd class="mt-1 text-sm leading-5 text-gray-900 sm:mt-0 sm:col-span-2">
          <input type="color" v-model="label.color"
                 class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 {% endif %} overflow-hidden rounded shadow-sm leading-tight focus:outline-none focus:shadow-outline">
        </dd>
      </div>
      <div class="bg-gray-50 px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 border-b-2">
        <label for="is_visible_to_guest" class="text-sm leading-5 font-medium text-gray-700 flex items-center">
          Visible for students
        </label>
        <dd class="mt-1 text-sm leading-5 text-gray-900 sm:mt-0 sm:col-span-2">
          <input type="checkbox" class="block" v-model="label.is_visible_to_guest">
        </dd>
      </div>
      <div class="bg-gray-50 px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 border-b-2">
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
              class="group inline-flex items-center px-4 py-2 border border-gray-300 text-sm leading-5 font-medium rounded-md text-gray-700 bg-white hover:text-gray-500 focus:outline-none focus:shadow-outline-blue focus:border-blue-300 active:text-gray-800 active:bg-gray-50">
        <span class="left-0 inset-y-0 flex items-center">
          <i class="fa fa-times mr-2"></i>
        </span>
        Cancel
      </button>
      <button type="button" @click="onSave()"
              class="group inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm leading-5 font-medium rounded-md bg-green-200 text-green-700 hover:bg-green-100 focus:outline-none focus:shadow-outline-indigo focus:border-green-700 active:bg-green-700 ">
        <span class="left-0 inset-y-0 flex items-center">
          <i class="fa fa-check mr-2"></i>
        </span>
        Save
      </button>
    </div>

    <div v-if="label && label.id" class="bg-white shadow overflow-hidden sm:rounded-lg mt-4 mb-4 px-4 py-5">
      <h3 class="text-lg leading-6 font-medium text-gray-900">
        Remove label
      </h3>
      <p class="mt-1 max-w-2xl text-sm leading-5 text-gray-500">
        When removing a label, the label will be removed from all ticket associated with it.
        This action in irreversible.
      </p>
      <button type="button" @click="onDelete()"
              class="group relative w-full sm:w-auto mt-4 inline-flex justify-center items-center rounded-md border border-transparent px-4 py-2 bg-red-200 text-red-600 co text-base leading-6 font-medium shadow-sm hover:bg-red-100 focus:outline-none focus:border-red-700 focus:shadow-outline-red transition ease-in-out duration-150 sm:text-sm sm:leading-5">
        <span class="absolute sm:relative left-0 inset-y-0 flex items-center pl-3 sm:pl-0">
          <i class="fa fa-trash mr-3"></i>
        </span>
        Remove
      </button>
    </div>
  </div>

</template>

<script>
import axios from "axios";

export default {
  name: "Label",
  data() {
    return {
      label: null,
    }
  },
  mounted() {
    const colors = [
        "#686F7D",
        "#6B7280",
        "#EC5050",
        "#F05252",
        "#FF5A1F",
        "#C27803",
        "#0E9F6E",
        "#0694A2",
        "#3F83F8",
        "#6875F5",
        "#9061F9"
    ]

    if (window.location.pathname.includes("new")) {
      this.label = {
        id: null,
        name: "",
        color: _.sample(colors),
        is_visible_to_guest: true,
        is_active: true
      }
    } else {
      const inboxId = this.$route.params.inboxId
      const labelId = this.$route.params.labelId

      axios.get(`/api/inboxes/${inboxId}/labels/${labelId}`).then(response => {
        this.label = response.data
      })
    }
  },
  methods: {
    onSave: function () {
      const inboxId = this.$route.params.inboxId
      const labelId = this.$route.params.labelId

      if (this.label.id) {
        axios.put(`/api/inboxes/${inboxId}/labels/${labelId}`, this.label).then(_ => {
          history.back()
        })
      } else {
        axios.post(`/api/inboxes/${inboxId}/labels/${labelId}`.replace("/new", ""), this.label).then(_ => {
          history.back()
        })
      }

    },
    onCancel: function () {
      window.history.back();
    },
    onDelete: function () {
      const inboxId = this.$route.params.inboxId
      const labelId = this.$route.params.labelId

      if (confirm('Are you sure?')) {
        axios.delete(`/api/inboxes/${inboxId}/labels/${labelId}`).then(_ => {
          history.back()
        })
      }
    }
  }
}
</script>

<style scoped>

</style>