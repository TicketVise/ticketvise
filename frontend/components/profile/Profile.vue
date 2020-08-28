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
                    <th class="px-4 py-3 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                      Notification
                    </th>
                    <th class="px-4 py-3 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                      In-app
                    </th>
                    <th class="px-4 py-3 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                      Email
                    </th>
                  </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                  <tr>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <div class="flex items-center">
                        <div class="text-sm leading-5 font-medium text-gray-900">
                          Mention
                        </div>
                      </div>
                    </td>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <input @change="updateNotifications()" type="checkbox"
                             v-model="settings.notification_mention_app">
                    </td>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <input @change="updateNotifications" type="checkbox" v-model="settings.notification_mention_mail">
                    </td>
                  </tr>
                  <tr>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <div class="flex items-center">
                        <div class="text-sm leading-5 font-medium text-gray-900">
                          New ticket
                        </div>
                      </div>
                    </td>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <input @change="updateNotifications()" type="checkbox"
                             v-model="settings.notification_new_ticket_app">
                    </td>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <input @change="updateNotifications" type="checkbox"
                             v-model="settings.notification_new_ticket_mail">
                    </td>
                  </tr>
                  <tr>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <div class="flex items-center">
                        <div class="text-sm leading-5 font-medium text-gray-900">
                          Comment/Reply
                        </div>
                      </div>
                    </td>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <input @change="updateNotifications()" type="checkbox"
                             v-model="settings.notification_comment_app">
                    </td>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <input @change="updateNotifications" type="checkbox" v-model="settings.notification_comment_mail">
                    </td>
                  </tr>
                  <tr>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <div class="flex items-center">
                        <div class="text-sm leading-5 font-medium text-gray-900">
                          Ticket assigned
                        </div>
                      </div>
                    </td>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <input @change="updateNotifications()" type="checkbox"
                             v-model="settings.notification_assigned_app">
                    </td>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <input @change="updateNotifications" type="checkbox"
                             v-model="settings.notification_assigned_mail">
                    </td>
                  </tr>
                  <tr>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <div class="flex items-center">
                        <div class="text-sm leading-5 font-medium text-gray-900">
                          Ticket reminder
                        </div>
                      </div>
                    </td>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <input @change="updateNotifications()" type="checkbox"
                             v-model="settings.notification_ticket_reminder_app">
                    </td>
                    <td class="px-4 py-2 whitespace-no-wrap">
                      <input @change="updateNotifications" type="checkbox"
                             v-model="settings.notification_ticket_reminder_mail">
                    </td>
                  </tr>
                  </tbody>
                </table>
              </div>
            </div>
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
    settings: [],

  }),
  mounted() {
    axios.get('/api/me').then(response => {
      this.user = response.data;
      axios.get('/api/me/settings').then(response => {
        this.settings = response.data
      })
    })
  },
  methods: {
    updateNotifications() {

      axios.defaults.xsrfCookieName = "csrftoken";
      axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

      axios.put('/api/me/settings', this.settings).then(response => {
        this.settings = response.data
      })
    }
  }
}
</script>
