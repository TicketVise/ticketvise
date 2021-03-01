<template>
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
              <td class="px-4 py-2 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="text-sm leading-5 font-medium text-gray-900">
                    Mention
                  </div>
                </div>
              </td>
              <td class="px-4 py-2 whitespace-nowrap">
                <input @change="updateNotifications()" type="checkbox" class="border-2"
                        v-model="settings.notification_mention_app">
              </td>
              <td class="px-4 py-2 whitespace-nowrap">
                <input @change="updateNotifications" type="checkbox"  class="border-2"
                       v-model="settings.notification_mention_mail">
              </td>
            </tr>
            <tr>
              <td class="px-4 py-2 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="text-sm leading-5 font-medium text-gray-900">
                    New ticket
                  </div>
                </div>
              </td>
              <td class="px-4 py-2 whitespace-nowrap">
                <input @change="updateNotifications()" type="checkbox" class="border-2"
                        v-model="settings.notification_new_ticket_app">
              </td>
              <td class="px-4 py-2 whitespace-nowrap">
                <input @change="updateNotifications" type="checkbox" class="border-2"
                        v-model="settings.notification_new_ticket_mail">
              </td>
            </tr>
            <tr>
              <td class="px-4 py-2 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="text-sm leading-5 font-medium text-gray-900">
                    Comment/Reply
                  </div>
                </div>
              </td>
              <td class="px-4 py-2 whitespace-nowrap">
                <input @change="updateNotifications()" type="checkbox" class="border-2"
                        v-model="settings.notification_comment_app">
              </td>
              <td class="px-4 py-2 whitespace-nowrap">
                <input @change="updateNotifications" type="checkbox" class="border-2"
                       v-model="settings.notification_comment_mail">
              </td>
            </tr>
            <tr>
              <td class="px-4 py-2 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="text-sm leading-5 font-medium text-gray-900">
                    Ticket assigned
                  </div>
                </div>
              </td>
              <td class="px-4 py-2 whitespace-nowrap">
                <input @change="updateNotifications()" type="checkbox" class="border-2"
                        v-model="settings.notification_assigned_app">
              </td>
              <td class="px-4 py-2 whitespace-nowrap">
                <input @change="updateNotifications" type="checkbox" class="border-2"
                        v-model="settings.notification_assigned_mail">
              </td>
            </tr>
            <tr>
              <td class="px-4 py-2 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="text-sm leading-5 font-medium text-gray-900">
                    Ticket reminder
                  </div>
                </div>
              </td>
              <td class="px-4 py-2 whitespace-nowrap">
                <input @change="updateNotifications()" type="checkbox" class="border-2"
                        v-model="settings.notification_ticket_reminder_app">
              </td>
              <td class="px-4 py-2 whitespace-nowrap">
                <input @change="updateNotifications" type="checkbox" class="border-2"
                        v-model="settings.notification_ticket_reminder_mail">
              </td>
            </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import store from "../../store";

export default {
  data: () => ({
    settings: []
  }),
  mounted() {
    axios.get('/api/me/settings').then(response => {
      this.settings = response.data
    })
  },
  methods: {
    updateNotifications() {
      axios.put('/api/me/settings', this.settings).then(response => {
        this.settings = response.data
      })
    }
  },
  computed: {
    user() {
      return store.state.user
    }
  }
}
</script>

<style>

</style>
