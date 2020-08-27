<template>
  <div v-if="user">
    <!-- Header -->
    <div class="border-b shadow flex justify-center">
      <div class="container px-4 my-4 mt-2 xl:flex xl:items-center xl:justify-between">
        <div class="flex-1 min-w-0">
          <a class="text-xs text-gray-700 hover:underline cursor-pointer" href="/inboxes">
            <i class="fa fa-arrow-left mr-2"></i>
            Dashboard
          </a>
          <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:leading-9 sm:truncate">
            Your profile
          </h2>
        </div>
      </div>
    </div>

    <div class="w-screen max-w-screen-lg mx-auto hidden lg:grid grid-cols-3 gap-8">
      <div class="col-span-1 p-8">
        <img :src="user.avatar_url" class="rounded-full w-full h-auto">
      </div>
      <div class="col-span-2 p-8">
        <div class="flex items-center">
          <h2 class="font-bold text-3xl text-orange-500 mr-2">{{ user.first_name }} {{ user.last_name }}</h2>
          <span class="font-light text-gray-400">@{{ user.username }}</span>
        </div>
        <div class="font-light mb-16 text-gray-700">
          <i class="fa fa-envelope mr-2"></i>
          {{ user.email }}
        </div>

        <!-- Notifications settings -->
        <div class="flex flex-col mb-8">
          <h2 class="text-xl font-bold mb-2 text-gray-700">Notification settings</h2>

          <div class="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
            <div class="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
              <div class="overflow-hidden border border-gray-200 sm:rounded">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead>
                  <tr>
                    <th
                        class="px-4 py-3 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                      Notification
                    </th>
                    <th
                        class="px-4 py-3 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                      In-app
                    </th>
                    <th
                        class="px-4 py-3 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                      Email
                    </th>
                  </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                  <tr>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <div class="flex items-center">
                        <div class="text-sm leading-5 font-medium text-gray-900">
                          New ticket
                        </div>
                      </div>
                    </td>
                    <td class="px-4 py-2 whitespace-no-wrap">
                        <input type="checkbox">
                    </td>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <span
                          class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                        Active
                      </span>
                    </td>
                  </tr>
                  <tr>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <div class="flex items-center">
                        <div class="text-sm leading-5 font-medium text-gray-900">
                          Ticket status change
                        </div>
                      </div>
                    </td>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <span
                          class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                        Active
                      </span>
                    </td>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <span
                          class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                        Active
                      </span>
                    </td>
                  </tr>
                  <tr>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <div class="flex items-center">
                        <div class="text-sm leading-5 font-medium text-gray-900">
                          Comments/Replies
                        </div>
                      </div>
                    </td>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <span
                          class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                        Active
                      </span>
                    </td>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <span
                          class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                        Active
                      </span>
                    </td>
                  </tr>
                  <tr>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <div class="flex items-center">
                        <div class="text-sm leading-5 font-medium text-gray-900">
                          Mentions
                        </div>
                      </div>
                    </td>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <span
                          class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                        Active
                      </span>
                    </td>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <span
                          class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                        Active
                      </span>
                    </td>
                  </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex space-x-4">
          <!-- <span class="shadow-sm rounded-md">
                  <a type="button" href="/password-change/"
                      class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm leading-5 font-medium rounded-md text-gray-700 bg-white hover:text-gray-500 focus:outline-none focus:shadow-outline-blue focus:border-blue-300 active:text-gray-800 active:bg-gray-50 transition duration-150 ease-in-out">
                      <i class="fa fa-cog mr-2"></i>
                      Change Password
                  </a>
              </span> -->

          <!-- <span class="shadow-sm rounded-md">
              <a type="button" href="/"
                  class="inline-flex items-center px-4 py-2 border border-transparent text-sm leading-5 font-medium rounded-md text-white bg-red-700 hover:bg-red-600 focus:outline-none focus:shadow-outline-red focus:border-red-700 active:bg-red-700 transition duration-150 ease-in-out">
                  <i class="fa fa-trash mr-2"></i>
                  DELETE ACCOUNT
              </a>
          </span> -->
        </div>
      </div>
    </div>

    <div class="container mx-auto lg:hidden grid grid-cols-3 gap-2 lg:gap-8 px-4">
      <div class="col-span-1 p-2 py-8 md:p-8">
        <img :src="user.avatar_url" class="rounded-full w-full h-auto">
      </div>
      <div class="col-span-2 p-8">
        <div class="flex flex-col md:flex-row items-start md:items-center">
          <h2 class="font-bold text-3xl text-orange-500 mr-2 leading-8">{{ user.first_name }} {{ user.last_name }}</h2>
          <span class="font-light text-gray-400">@{{ user.username }}</span>
        </div>
        <div class="flex items-center font-light mb-16 text-gray-700 text-sm sm:text-base">
          <i class="fa fa-envelope mr-2"></i>
          {{ user.email }}
        </div>

      </div>
    </div>
    <!-- Notifications settings -->
    <div class="container mx-auto flex flex-col mb-8 px-4 lg:hidden">
      <h2 class="text-xl font-bold mb-2 text-gray-700">Notification settings</h2>

      <div class="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div class="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
          <div class="overflow-hidden border border-gray-200 sm:rounded">
            <table class="min-w-full divide-y divide-gray-200">
              <thead>
              <tr>
                <th
                    class="px-4 py-3 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                  Notification
                </th>
                <th
                    class="px-4 py-3 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                  In-app
                </th>
                <th
                    class="px-4 py-3 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                  Email
                </th>
              </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
              <tr>
                <td class="px-4 py-2 whitespace-no-wrap">
                  <div class="flex items-center">
                    <div class="text-sm leading-5 font-medium text-gray-900">
                      New ticket
                    </div>
                  </div>
                </td>
                <td class="px-4 py-2 whitespace-no-wrap">
                  <span
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                    Active
                  </span>
                </td>
                <td class="px-4 py-2 whitespace-no-wrap">
                  <span
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                    Active
                  </span>
                </td>
              </tr>
              <tr>
                <td class="px-4 py-2 whitespace-no-wrap">
                  <div class="flex items-center">
                    <div class="text-sm leading-5 font-medium text-gray-900">
                      Ticket status change
                    </div>
                  </div>
                </td>
                <td class="px-4 py-2 whitespace-no-wrap">
                  <span
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                    Active
                  </span>
                </td>
                <td class="px-4 py-2 whitespace-no-wrap">
                  <span
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                    Active
                  </span>
                </td>
              </tr>
              <tr>
                <td class="px-4 py-2 whitespace-no-wrap">
                  <div class="flex items-center">
                    <div class="text-sm leading-5 font-medium text-gray-900">
                      Comments/Replies
                    </div>
                  </div>
                </td>
                <td class="px-4 py-2 whitespace-no-wrap">
                  <span
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                    Active
                  </span>
                </td>
                <td class="px-4 py-2 whitespace-no-wrap">
                  <span
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                    Active
                  </span>
                </td>
              </tr>
              <tr>
                <td class="px-4 py-2 whitespace-no-wrap">
                  <div class="flex items-center">
                    <div class="text-sm leading-5 font-medium text-gray-900">
                      Mentions
                    </div>
                  </div>
                </td>
                <td class="px-4 py-2 whitespace-no-wrap">
                  <span
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                    Active
                  </span>
                </td>
                <td class="px-4 py-2 whitespace-no-wrap">
                  <span
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                    Active
                  </span>
                </td>
              </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"

export default {
  data: () => ({
    user: null,
    notification_settings: [
      {
        "title": "",
        "name": "notification_mention_mail",
        "value": "notification_mention_mail"
      }
    ],

  }),
  mounted() {
    axios.get('/api/user').then(response => {
      this.user = response.data

      axios.get('/api/user/notifications').then(response => {
        this.notifications = response.data
      })
    })
  }
}
</script>
