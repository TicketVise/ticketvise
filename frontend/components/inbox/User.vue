<template>
  <div class="container mx-auto max-w-3xl" x-data="{ modal: false }">

    <div v-if="inbox_user" class="bg-white shadow overflow-hidden sm:rounded-lg sm:mt-4 sm:mx-4">
      <div class="px-4 py-5 border-b border-gray-200 sm:px-6 flex">
        <div class="flex-shrink-0 h-10 w-10 mr-4">
          <img class="h-10 w-10 rounded-full" :src="inbox_user.user.avatar_url" alt="Profile picture"/>
        </div>
        <div>
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            User Information
          </h3>
          <p class="mt-1 max-w-2xl text-sm leading-5 text-gray-500">
            Personal details and inbox related settings.
          </p>
        </div>
      </div>
      <div>
        <dl>
          <div class="bg-gray-50 px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <dt class="text-sm leading-5 font-medium text-gray-500">
              Full name
            </dt>
            <dd class="mt-1 text-sm leading-5 text-gray-900 sm:mt-0 sm:col-span-2">
              {{ inbox_user.user.get_full_name }}
            </dd>
          </div>
          <div class="bg-white px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <dt class="text-sm leading-5 font-medium text-gray-500">
              Email address
            </dt>
            <dd class="mt-1 text-sm leading-5 text-gray-900 sm:mt-0 sm:col-span-2">
              {{ inbox_user.user.email }}
            </dd>
          </div>
          <div class="bg-gray-50 px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
            <dt class="text-sm leading-5 font-medium text-gray-500">
              Username
            </dt>
            <dd class="mt-1 text-sm leading-5 text-gray-900 sm:mt-0 sm:col-span-2">
              @{{ inbox_user.user.username }}
            </dd>
          </div>
          <div class="bg-white px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 ">
            <dt class="text-sm leading-5 font-medium text-gray-500">
              Role
            </dt>
            <dd class="text-sm leading-5 text-gray-900 sm:mt-0 sm:col-span-2">
              <select name="role" v-model="inbox_user.role"
                      class="block appearance-none bg-white border border-gray-400 hover:border-gray-500 px-4 py-1 pr-8 rounded shadow-sm leading-tight focus:outline-none focus:shadow-outline">
                <option v-for="role in roles" :value="role.key">
                  {{ role.label }}
                </option>
              </select>
            </dd>
          </div>
        </dl>
      </div>
    </div>

    <div class="p-2 px-4 sm:pr-0 flex space-x-2 sm:mx-4 justify-end">
      <button type="button" @click="onCancel"
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


    <div class="bg-white shadow overflow-hidden sm:rounded-lg mt-8 mb-4 px-4 py-5 sm:mx-4">
      <h3 class="text-lg leading-6 font-medium text-gray-900">
        Remove user
      </h3>
      <p class="mt-1 max-w-2xl text-sm leading-5 text-gray-500">
        The user will lose access to the inbox and will be unable to create new tickets or answer tickets.
      </p>
      <button type="button" @click="onDelete()"
              class="w-full sm:w-auto mt-4 inline-flex justify-center items-center rounded-md border border-transparent px-4 py-2 bg-red-200 text-red-600 co text-base leading-6 font-medium shadow-sm hover:bg-red-100 focus:outline-none focus:border-red-700 focus:shadow-outline-red transition ease-in-out duration-150 sm:text-sm sm:leading-5">
        <i class="fa fa-trash mr-3"></i>
        Remove
      </button>
    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "User",
  data() {
    return {
      inbox_user: null,
      roles: [
        {
          "key": "GUEST",
          "label": "Student"
        },
        {
          "key": "AGENT",
          "label": "Teaching Assistant"
        },
        {
          "key": "MANAGER",
          "label": "Coordinator"
        }
      ]
    }
  },
  mounted() {
    axios.get(`/api${window.location.pathname}`).then(response => {
      this.inbox_user = response.data
    })
  },
  methods: {
    onSave: function () {
      axios.defaults.xsrfCookieName = 'csrftoken';
      axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

      axios.put(`/api${window.location.pathname}`, this.inbox_user).then(_ => {
        history.back()
      })
    },
    onCancel: function () {
      window.history.back();
    },
    onDelete: function () {
      if (confirm('Are you sure?')) {
        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

        axios.delete(`/api${window.location.pathname}`).then(_ => {
          history.back()
        })
      }
    }
  }
}
</script>

<style scoped>

</style>