<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:max-w-7xl lg:px-8">
    <h1 class="sr-only">Profile</h1>
    <!-- Main 3 column grid -->
    <div class="grid grid-cols-1 gap-4 items-start">
      <h2 class="text-lg leading-6 font-medium text-gray-100">Your account</h2>
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <div v-for="stat in stats" :key="stat.label" class="bg-white overflow-hidden shadow rounded">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <component :is="stat.icon" class="h-6 w-6 text-gray-400" aria-hidden="true"/>
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-gray-500 truncate">
                    {{ stat.label }}
                  </dt>
                  <dd>
                    <div class="text-lg font-medium text-gray-900">
                      {{ stat.value }}
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="grid md:grid-cols-2 gap-4">
        <!-- Basic information section -->
        <section aria-labelledby="payment-details-heading">
          <form @submit.prevent="">
            <div class="shadow rounded sm:overflow-hidden">
              <div class="bg-white py-6 px-4 sm:p-6">
                <div>
                  <h2 id="payment-details-heading" class="text-lg leading-6 font-medium text-gray-900">General
                    information</h2>
                  <p class="mt-1 text-sm text-gray-500">Change your basic information here, we won't ask you for more
                    personal information.</p>
                </div>
                <div class="mt-6 flex flex-col lg:flex-row">
                  <div class="flex-grow space-y-4">
                    <div>
                      <label for="last_name" class="block text-sm font-medium text-gray-700">
                        <span class="mr-1">Username</span>
                        <span
                          class="inline-flex items-center px-2.5 rounded-md text-sm font-medium bg-gray-100 text-primary">
                          LTI
                        </span>
                      </label>
                      <div class="mt-1 rounded-md flex">
                        <input disabled type="text" name="username" id="username" autocomplete="username"
                               class="focus:ring-sky-500 focus:border-sky-500 flex-grow block w-full min-w-0 rounded-md sm:text-sm border-gray-300"
                               :value="user.username"/>
                      </div>
                    </div>

                    <div>
                      <label for="first_name" class="block text-sm font-medium text-gray-700">
                        <span class="mr-1">First Name</span>
                        <span
                          class="inline-flex items-center px-2.5 rounded-md text-sm font-medium bg-gray-100 text-primary">
                          LTI
                        </span>
                      </label>
                      <div class="mt-1 rounded-md flex">
                        <input disabled type="text" name="first_name" id="first_name" autocomplete="first_name"
                               class="focus:ring-sky-500 focus:border-sky-500 flex-grow block w-full min-w-0 rounded-md sm:text-sm border-gray-300"
                               :value="user.first_name"/>
                      </div>
                    </div>

                    <div>
                      <label for="last_name" class="block text-sm font-medium text-gray-700">
                        <span class="mr-1">Last Name</span>
                        <span
                          class="inline-flex items-center px-2.5 rounded-md text-sm font-medium bg-gray-100 text-primary">
                          LTI
                        </span>
                      </label>
                      <div class="mt-1 rounded-md flex">
                        <input disabled type="text" name="last_name" id="last_name" autocomplete="last_name"
                               class="focus:ring-sky-500 focus:border-sky-500 flex-grow block w-full min-w-0 rounded-md sm:text-sm border-gray-300"
                               :value="user.last_name"/>
                      </div>
                    </div>

                    <div>
                      <label for="last_name" class="block text-sm font-medium text-gray-700">
                        <span class="mr-1">Email</span>
                        <span
                          class="inline-flex items-center px-2.5 rounded-md text-sm font-medium bg-gray-100 text-primary">
                          LTI
                        </span>
                      </label>
                      <div class="mt-1 rounded-md flex">
                        <input disabled type="text" name="email" id="email" autocomplete="email"
                               class="focus:ring-sky-500 focus:border-sky-500 flex-grow block w-full min-w-0 rounded-md sm:text-sm border-gray-300"
                               :value="user.email"/>
                      </div>
                    </div>
                  </div>

                  <div class="mt-6 flex-grow lg:mt-0 lg:ml-6 lg:flex-grow-0 lg:flex-shrink-0">
                    <p class="text-sm font-medium text-gray-700 mb-1" aria-hidden="true">
                      <span class="mr-1">Photo</span>
                      <span
                        class="inline-flex items-center px-2.5 rounded-md text-sm font-medium bg-gray-100 text-primary">
                        LTI
                      </span>
                    </p>
                    <div class="mt-1 lg:hidden">
                      <div class="flex items-center">
                        <div class="flex-shrink-0 inline-block rounded-full overflow-hidden h-12 w-12"
                             aria-hidden="true">
                          <img class="rounded-full h-full w-full" :src="user.avatar_url" alt=""/>
                        </div>
                        <div class="ml-5 rounded-md">
                          <div
                            class="group relative border border-gray-300 rounded-md py-2 px-3 flex items-center justify-center hover:bg-gray-50 focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-sky-500">
                            <label for="user-photo"
                                   class="relative text-sm leading-4 font-medium text-gray-300 pointer-events-none">
                              <span>Change</span>
                              <span class="sr-only"> user photo</span>
                            </label>
                            <input id="user-photo" name="user-photo" type="file" disabled
                                   class="absolute w-full h-full opacity-0 cursor-pointer border-gray-300 rounded-md"/>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div class="hidden relative rounded-full overflow-hidden lg:block">
                      <img class="relative rounded-full w-40 h-40" :src="user.avatar_url" alt=""/>
                      <!-- <label for="user-photo"
                             class="absolute inset-0 w-full h-full bg-black bg-opacity-75 flex items-center justify-center text-sm font-medium text-white opacity-0 hover:opacity-100 focus-within:opacity-100">
                        <span>Change</span>
                        <span class="sr-only"> user photo</span>
                        <input type="file" id="user-photo" name="user-photo"
                               class="absolute inset-0 w-full h-full opacity-0 cursor-pointer border-gray-300 rounded-md"/>
                      </label> -->
                    </div>
                  </div>
                </div>
              </div>
              <div class="rounded-md bg-blue-50 p-4">
                <div class="flex">
                  <div class="flex-shrink-0">
                    <InformationCircleIcon class="h-5 w-5 text-blue-400" aria-hidden="true"/>
                  </div>
                  <div class="ml-3 flex-1 md:flex md:justify-between">
                    <p class="text-sm text-blue-700">
                      Your account details are given to us by the LTI provider, so you can't change them here.
                    </p>
                  </div>
                </div>
              </div>
              <div class="px-4 py-3 bg-gray-50 text-right sm:px-6">
                <button disabled type="submit"
                        class="bg-primary-100 border border-transparent rounded-md py-2 px-4 inline-flex justify-center text-sm font-medium text-primary-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-900">
                  Save
                </button>
                <!-- <button type="submit" class="bg-gray-800 border border-transparent rounded-md py-2 px-4 inline-flex justify-center text-sm font-medium text-white hover:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-900">
                  Save
                </button> -->
              </div>
            </div>
          </form>
        </section>

        <table class="min-w-full divide-y divide-gray-200 shadow rounded sm:overflow-hidden">
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
              <div class="flex flex-col">
                <div>
                  <span class="text-sm leading-5 font-medium text-gray-900">Comments and replies </span>
                </div>
                <span class="text-sm leading-5 text-gray-500">If a comment or reply has been placed on one of your (assigned) tickets</span>
              </div>
            </td>
            <td class="px-4 py-2 whitespace-no-wrap">
              <input @change="updateNotifications()" type="checkbox" class="border-2"
                     v-model="settings.notification_comment_app">
            </td>
            <td class="px-4 py-2 whitespace-no-wrap">
              <input @change="updateNotifications" type="checkbox" class="border-2"
                     v-model="settings.notification_comment_mail">
            </td>
          </tr>
          <tr>
            <td class="px-4 py-2 whitespace-no-wrap">
              <div class="flex flex-col">
                <div>
                  <span class="text-sm leading-5 font-medium text-gray-900">New ticket </span>
                  <span class="text-xs leading-5 font-small text-gray-400">(Teacher and TA only)</span>
                </div>
                <span class="text-sm leading-5 text-gray-500">When a new ticket has been created in a inbox</span>
              </div>
            </td>
            <td class="px-4 py-2 whitespace-no-wrap">
              <input @change="updateNotifications()" type="checkbox" class="border-2"
                     v-model="settings.notification_new_ticket_app">
            </td>
            <td class="px-4 py-2 whitespace-no-wrap">
              <input @change="updateNotifications" type="checkbox" class="border-2"
                     v-model="settings.notification_new_ticket_mail">
            </td>
          </tr>
          <tr>
            <td class="px-4 py-2 whitespace-no-wrap">
              <div class="flex flex-col">
                <div>
                  <span class="text-sm leading-5 font-medium text-gray-900">Assigned </span>
                  <span class="text-xs leading-5 font-small text-gray-400">(Teacher and TA only)</span>
                </div>
                <span class="text-sm leading-5 text-gray-500">If a new ticket is assigned to you</span>
              </div>
            </td>
            <td class="px-4 py-2 whitespace-no-wrap">
              <input @change="updateNotifications()" type="checkbox" class="border-2"
                     v-model="settings.notification_assigned_app">
            </td>
            <td class="px-4 py-2 whitespace-no-wrap">
              <input @change="updateNotifications" type="checkbox" class="border-2"
                     v-model="settings.notification_assigned_mail">
            </td>
          </tr>
          <tr>
            <td class="px-4 py-2 whitespace-no-wrap">
              <div class="flex flex-col">
                <div>
                  <span class="text-sm leading-5 font-medium text-gray-900">Ticket reminder </span>
                  <span class="text-xs leading-5 font-small text-gray-400">(Teacher and TA only)</span>
                </div>
                <span class="text-sm leading-5 text-gray-500">If a ticket assigned to you is unanswered for a certain amount of time</span>
              </div>
            </td>
            <td class="px-4 py-2 whitespace-no-wrap">
              <input @change="updateNotifications()" type="checkbox" class="border-2"
                     v-model="settings.notification_ticket_reminder_app">
            </td>
            <td class="px-4 py-2 whitespace-no-wrap">
              <input @change="updateNotifications" type="checkbox" class="border-2"
                     v-model="settings.notification_ticket_reminder_mail">
            </td>
          </tr>
          <tr>
            <td class="px-4 py-2 whitespace-no-wrap">
              <div class="flex flex-col">
                <div>
                  <span class="text-sm leading-5 font-medium text-gray-900">Mention </span>
                  <span class="text-xs leading-5 font-small text-gray-400">(Teacher and TA only)</span>
                </div>
                <span class="text-sm leading-5 text-gray-500">If a fellow teacher mentions you in a ticket</span>
              </div>
            </td>
            <td class="px-4 py-2 whitespace-no-wrap">
              <input @change="updateNotifications()" type="checkbox" class="border-2"
                     v-model="settings.notification_mention_app">
            </td>
            <td class="px-4 py-2 whitespace-no-wrap">
              <input @change="updateNotifications" type="checkbox" class="border-2"
                     v-model="settings.notification_mention_mail">
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import store from '@/store'

import {
  CollectionIcon,
  GlobeIcon,
  InboxIcon
} from '@heroicons/vue/outline'
import { InformationCircleIcon } from '@heroicons/vue/solid'

export default {
  name: 'Dashboard',
  components: {
    InformationCircleIcon
  },
  data: () => ({
    enabled: false,
    user: store.state.user,
    settings: [],
    stats: [
      { label: 'Inboxes', value: '#', icon: InboxIcon },
      { label: 'Tickets', value: '#', icon: CollectionIcon },
      { label: 'Public tickets', value: '#', icon: GlobeIcon }
    ]
  }),
  mounted () {
    axios.get('/api/me/statistics').then(response => {
      this.stats.find(s => s.label === 'Inboxes').value = response.data.inboxes || 0
      this.stats.find(s => s.label === 'Tickets').value = response.data.tickets || 0
      this.stats.find(s => s.label === 'Public tickets').value = response.data.public_tickets || 0
    })
    axios.get('api/me/settings').then(response => {
      this.settings = response.data
    })
  },
  methods: {
    updateNotifications () {
      axios.put('/api/me/settings', this.settings).then(response => {
        this.settings = response.data
      })
    }
  }
}
</script>
