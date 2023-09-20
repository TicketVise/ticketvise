<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:max-w-7xl lg:px-8">
    <h1 class="sr-only">Profile</h1>
    <!-- Main 3 column grid -->
    <div class="grid grid-cols-1 gap-4 items-start">
      <!-- Welcome panel -->
      <section aria-labelledby="profile-overview-title">
        <div class="rounded-lg bg-white overflow-hidden shadow">
          <h2 class="sr-only" id="profile-overview-title">Profile Overview</h2>
          <div class="bg-white p-6">
            <div class="sm:flex sm:items-center sm:justify-between">
              <div class="sm:flex sm:space-x-5">
                <div class="flex-shrink-0">
                  <img class="mx-auto h-20 w-20 rounded-full" :src="user.avatar_url" alt="" />
                </div>
                <div class="mt-4 text-center sm:mt-0 sm:pt-1 sm:text-left">
                  <p class="text-sm font-medium text-gray-600">Welcome back,</p>
                  <p class="text-xl font-bold text-gray-900 sm:text-2xl">{{ user.first_name }} {{ user.last_name }}</p>
                  <!-- <p class="text-sm font-medium text-gray-600">{{ user.role }}</p> -->
                </div>
              </div>
              <div class="mt-5 flex justify-center sm:mt-0">
                <router-link to="/account" class="flex justify-center items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                  View profile
                </router-link>
              </div>
            </div>
          </div>
          <!-- <div class="border-t border-gray-200 bg-gray-50 grid grid-cols-1 divide-y divide-gray-200 sm:grid-cols-3 sm:divide-y-0 sm:divide-x">
            <div v-for="stat in stats" :key="stat.label" class="px-6 py-5 text-sm font-medium text-center">
              <span class="text-gray-900">{{ stat.value }}</span>
              {{ ' ' }}
              <span class="text-gray-600">{{ stat.label }}</span>
            </div>
          </div> -->
        </div>
      </section>

      <!-- Inboxes grid -->
      <!-- <template v-for="(inboxes, year) in inboxesByYear" :key="year">
        <h2 class="mt-6 text-xl font-medium text-gray-800">{{ year }}</h2> -->
        <div class="sm:px-0 grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <router-link :to="`/inboxes/${inbox.id}/overview`" v-for="inbox in inboxes" :key="inbox.id" class="group bg-white relative rounded-lg">
            <div class="" aria-label="more options">
              <div class="h-64 w-full rounded-lg group-hover:shadow-2xl transition-shadow ease-in-out duration-100 bg-gray-400">
                <img class="h-64 w-full rounded-lg object-cover opacity-75" :src="inbox.image || '/img/default-inbox.png'" :alt="inbox.name">
              </div>
            </div>

            <div class="absolute bottom-0 bg-gray-800 bg-opacity-50 w-full text-white flex flex-col py-2 px-4 rounded-br-lg rounded-bl-lg shadow-lg"
                style="overflow: hidden; text-overflow: ellipsis;">
              <div class="font-bold truncate">{{ inbox.name }}</div>
              <span class="text-sm">{{ inbox.lti_context_label }}</span>
            </div>
          </router-link>
        </div>
      <!-- </template> -->
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
import store from '@/store'

export default {
  name: 'Dashboard',
  async mounted () {
    const inboxes = await this.getInboxes()

    store.commit('update_inboxes', inboxes)
  },
  methods: {
    async getInboxes () {
      if (this.user.is_superuser) {
        const response = await axios.get('/api/inboxes')
        return response.data
      } else {
        const response = await axios.get('/api/me/inboxes')
        return response.data.map(inbox => inbox.inbox)
      }
    }
  },
  computed: {
    ...mapState({
      user: state => state.user,
      inboxes: state => state.inboxes
    }),
    inboxesByYear() {
      let inboxes = [...this.inboxes]

      const unordered = inboxes.reduce((acc, inbox) => {
        const year = new Date(inbox.date_created).getFullYear()
        if (!acc[year]) {
          acc[year] = []
        }
        acc[year].push(inbox)
        return acc
      }, {})
      console.log(unordered)

      const ordered = Object.keys(unordered).sort((a, b) => a > b).reduce(
        (obj, key) => { 
          obj[key] = unordered[key]; 
          return obj;
        }, 
        {}
      );
      console.log(ordered)

      return ordered
    }
  }
}
</script>
