<template>
  <div class="h-screen items-stretch overflow-y-hidden">
    <div class="flex flex-row flex-grow h-full max-w-full pt-16 -mt-16">
      <!-- Side Menu -->
      <div class="min-w-side max-w-side border-r hidden lg:flex flex-col flex-grow">
        <!-- Account section -->
        <div class="flex items-center px-6 py-4" v-if="user">
          <div class="flex-shrink-0">
            <img class="h-10 w-10 rounded-full" :src="user.avatar_url" alt="Account image">
          </div>
          <div class="ml-3">
            <div class="text-base font-bold leading-none text-gray-900">{{ user.full_name }}</div>
            <div class="mt-1 text-sm leading-none text-gray-600">{{ user.email }}</div>
          </div>
        </div>

        <div class="p-4">
          <router-link to="ticket/new"
             class="inline-flex w-full justify-center items-center px-4 py-2 border border-transparent text-sm leading-5 font-medium rounded-md text-white bg-primary hover:bg-orange-500 focus:outline-none focus:shadow-outline-orange focus:border-orange-700 active:bg-orange-700 transition duration-150 ease-in-out">
            <i class="fa fa-plus mr-2"></i>
            <span>New Ticket</span>
          </router-link>
        </div>

        <!-- Inbox links -->
        <div class="flex flex-col space-y-1 px-4">
          <router-link to="tickets"
             class="grid grid-cols-12 px-3 py-2 rounded items-center space-x-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900">
            <i class="fa fa-home col-span-1 flex justify-center"></i>
            <span class="col-span-11">Overview</span>
          </router-link>
          <router-link to="users" v-if="is_staff"
             class="grid grid-cols-12 px-3 py-2 rounded items-center space-x-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900">
            <i class="fa fa-users col-span-1 flex justify-center"></i>
            <span class="col-span-11">Users</span>
          </router-link>
          <router-link to="labels" v-if="is_staff"
             class="grid grid-cols-12 px-3 py-2 rounded items-center space-x-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900">
            <i class="fa fa-tags col-span-1 flex justify-center"></i>
            <span class="col-span-11">Labels</span>
          </router-link>
          <router-link to="statistics"  v-if="is_staff"
             class="grid grid-cols-12 px-3 py-2 rounded items-center space-x-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900">
            <svg focusable="false" data-prefix="fas"
                 data-icon="chart-line" class="svg-inline--fa fa-chart-line fa-w-16" role="img"
                 xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
              <path fill="currentColor"
                    d="M496 384H64V80c0-8.84-7.16-16-16-16H16C7.16 64 0 71.16 0 80v336c0 17.67 14.33 32 32 32h464c8.84 0 16-7.16 16-16v-32c0-8.84-7.16-16-16-16zM464 96H345.94c-21.38 0-32.09 25.85-16.97 40.97l32.4 32.4L288 242.75l-73.37-73.37c-12.5-12.5-32.76-12.5-45.25 0l-68.69 68.69c-6.25 6.25-6.25 16.38 0 22.63l22.62 22.62c6.25 6.25 16.38 6.25 22.63 0L192 237.25l73.37 73.37c12.5 12.5 32.76 12.5 45.25 0l96-96 32.4 32.4c15.12 15.12 40.97 4.41 40.97-16.97V112c.01-8.84-7.15-16-15.99-16z"></path>
            </svg>
            <span class="col-span-11">Statistics</span>
          </router-link>
          <router-link to="settings" v-if="is_staff"
             class="grid grid-cols-12 px-3 py-2 rounded items-center space-x-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900">
            <i class="fa fa-cog col-span-1 flex justify-center"></i>
            <span class="col-span-11">Settings</span>
          </router-link>
<!--          <a href="{% url 'inbox_automation' inbox.id %}"-->
<!--                           class="grid grid-cols-12 px-3 py-2 rounded items-center space-x-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900">-->
<!--          <svg class="col-span-1 flex justify-center" aria-hidden="true" focusable="false" data-prefix="fas"-->
<!--               data-icon="code-branch" class="svg-inline&#45;&#45;fa fa-code-branch fa-w-12" role="img"-->
<!--               xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512">-->
<!--            <path fill="currentColor"-->
<!--                  d="M384 144c0-44.2-35.8-80-80-80s-80 35.8-80 80c0 36.4 24.3 67.1 57.5 76.8-.6 16.1-4.2 28.5-11 36.9-15.4 19.2-49.3 22.4-85.2 25.7-28.2 2.6-57.4 5.4-81.3 16.9v-144c32.5-10.2 56-40.5 56-76.3 0-44.2-35.8-80-80-80S0 35.8 0 80c0 35.8 23.5 66.1 56 76.3v199.3C23.5 365.9 0 396.2 0 432c0 44.2 35.8 80 80 80s80-35.8 80-80c0-34-21.2-63.1-51.2-74.6 3.1-5.2 7.8-9.8 14.9-13.4 16.2-8.2 40.4-10.4 66.1-12.8 42.2-3.9 90-8.4 118.2-43.4 14-17.4 21.1-39.8 21.6-67.9 31.6-10.8 54.4-40.7 54.4-75.9zM80 64c8.8 0 16 7.2 16 16s-7.2 16-16 16-16-7.2-16-16 7.2-16 16-16zm0 384c-8.8 0-16-7.2-16-16s7.2-16 16-16 16 7.2 16 16-7.2 16-16 16zm224-320c8.8 0 16 7.2 16 16s-7.2 16-16 16-16-7.2-16-16 7.2-16 16-16z"></path>-->
<!--          </svg>-->
<!--          <span class="col-span-11">Automation</span>-->
<!--        </a> -->
        </div>
      </div>
      <div v-if="side" class="lg:hidden fixed inset-0 overflow-hidden z-50">
        <div class="absolute inset-0 overflow-hidden">
          <!-- Background overlay, show/hide based on slide-over state. -->
          <div v-if="side" @click="side = false"
              class="absolute inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
          <section class="absolute inset-y-0 right-0 max-w-full flex">
            <!-- Slide-over panel, show/hide based on slide-over state. -->
            <div v-if="side" class="relative w-screen max-w-side">
              <!-- Close button, show/hide based on slide-over state. -->
              <div v-if="side" class="absolute top-0 left-0 -ml-8 pt-4 pr-2 flex sm:-ml-10 sm:pr-4">
                <button aria-label="Close panel"
                        class="text-gray-300 hover:text-white transition ease-in-out duration-150">
                  <!-- Heroicon name: x -->
                  <svg @click="side = false" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                  </svg>
                </button>
              </div>
              <div class="h-full flex flex-col py-2 bg-white shadow-xl overflow-y-scroll">
                <header class="mx-4 py-2 sm:mx-6 border-b">
                  <a href="/" class="flex items-center">
                    <img class="h-8 w-8" src="/static/img/logo/logo.svg" alt="Logo">
                    <span class="text-2xl ml-2 text-gray-800">Ticket</span>
                    <span class="text-2xl text-primary font-bold">Vise</span>
                  </a>
                </header>
                <div class="relative flex-1 px-4 py-2 sm:px-6" v-if="userInbox">
                  <h2 class="text-lg font-bold leading-6 text-gray-900 truncate">
                    {{ userInbox.inbox.name }}
                  </h2>
                  <div class="flex flex-row flex-wrap space-x-4 sm:space-x-6">
                    <div class="mt-2 flex items-center text-sm leading-5 text-gray-500">
                      <i class="fa fa-code mr-1"></i>
                      {{ userInbox.inbox.code }}
                    </div>
                    <div v-if="userInbox.inbox.coordinator" class="mt-2 flex items-center text-sm leading-5 text-gray-500">
                      <i class="fa fa-user mr-1"></i>
                      {{ userInbox.inbox.coordinator.first_name }} {{ userInbox.inbox.coordinator.last_name }}
                    </div>
                  </div>

                  <div class="py-4">
                    <router-link to="tickets/new"
                       class="inline-flex w-full justify-center items-center px-4 py-2 border border-transparent text-sm
                       leading-5 font-medium rounded-md text-white bg-primary hover:bg-orange-500 focus:outline-none
                       focus:shadow-outline-orange focus:border-orange-700 active:bg-orange-700 transition duration-150
                       ease-in-out">
                      <i class="fa fa-plus mr-2"></i>
                      <span>New Ticket</span>
                    </router-link>
                  </div>

                  <!-- Inbox links -->
                  <div class="flex flex-col space-y-1">
                    <router-link to="tickets"
                       class="grid grid-cols-12 px-3 py-2 rounded items-center space-x-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900">
                      <i class="fa fa-home col-span-1 flex justify-center"></i>
                      <span class="col-span-11">Overview</span>
                    </router-link>
                    <router-link to="tickets" v-if="is_staff"
                       class="grid grid-cols-12 px-3 py-2 rounded items-center space-x-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900">
                      <i class="fa fa-users col-span-1 flex justify-center"></i>
                      <span class="col-span-11">Users</span>
                    </router-link>
                    <router-link to="labels" v-if="is_staff"
                       class="grid grid-cols-12 px-3 py-2 rounded items-center space-x-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900">
                      <i class="fa fa-tags col-span-1 flex justify-center"></i>
                      <span class="col-span-11">Labels</span>
                    </router-link>
                    <router-link to="statistics" v-if="is_staff"
                       class="grid grid-cols-12 px-3 py-2 rounded items-center space-x-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900">
                      <svg focusable="false" data-prefix="fas"
                           data-icon="chart-line" class= "svg-inline--fa fa-chart-line fa-w-16" role="img"
                           xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                        <path fill="currentColor"
                              d="M496 384H64V80c0-8.84-7.16-16-16-16H16C7.16 64 0 71.16 0 80v336c0 17.67 14.33 32 32 32h464c8.84 0 16-7.16 16-16v-32c0-8.84-7.16-16-16-16zM464 96H345.94c-21.38 0-32.09 25.85-16.97 40.97l32.4 32.4L288 242.75l-73.37-73.37c-12.5-12.5-32.76-12.5-45.25 0l-68.69 68.69c-6.25 6.25-6.25 16.38 0 22.63l22.62 22.62c6.25 6.25 16.38 6.25 22.63 0L192 237.25l73.37 73.37c12.5 12.5 32.76 12.5 45.25 0l96-96 32.4 32.4c15.12 15.12 40.97 4.41 40.97-16.97V112c.01-8.84-7.15-16-15.99-16z"></path>
                      </svg>
                      <span class="col-span-11">Statistics</span>
                    </router-link>
                    <router-link to="settings" v-if="is_staff"
                       class="grid grid-cols-12 px-3 py-2 rounded items-center space-x-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900">
                      <i class="fa fa-cog col-span-1 flex justify-center"></i>
                      <span class="col-span-11">Settings</span>
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </div>
      </div>

      <div id="scrollable-content" class="flex flex-col w-full overflow-x-hidden overflow-y-auto">
        <header class="bg-white border-b" v-if="userInbox">
          <div class="relative p-4 pt-2">
            <div class="lg:flex lg:items-center lg:justify-between">
              <div class="flex-1 min-w-0">
                <div class="flex justify-between items-center">
                  <router-link to="/inboxes" class="text-xs text-gray-700 hover:underline cursor-pointer">
                    <i class="fa fa-arrow-left mr-2"></i>
                    Dashboard
                  </router-link>
                </div>
                <button
                    class="absolute top-0 right-2 inline-flex lg:hidden items-center justify-center p-2 m-1 rounded-md text-gray-600 hover:text-white hover:bg-gray-700 focus:outline-none focus:bg-gray-700 focus:text-white transition duration-150 ease-in-out"
                    aria-label="Main menu" aria-expanded="false" @click="side = !side">
                  <i class="fa fa-bars"></i>
                </button>

                <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:leading-9 truncate">
                  {{ userInbox.inbox.name }}
                </h2>
                <div class="flex flex-row flex-wrap space-x-4 sm:space-x-6">
                  <div class="mt-2 flex items-center text-sm leading-5 text-gray-500">
                    <i class="fa fa-code mr-1"></i>
                    {{ userInbox.inbox.code }}
                  </div>
                  <div v-if="userInbox.inbox.coordinator" class="mt-2 flex items-center text-sm leading-5 text-gray-500">
                    <i class="fa fa-user mr-1"></i>
                    {{ userInbox.inbox.coordinator.first_name }} {{ userInbox.inbox.coordinator.last_name }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </header>
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Inbox",
  data: () => ({
    userInbox: null,
    side: false,
  }),
  async mounted() {
    const response = await axios.get(`api/me/inboxes/${this.$route.params.inboxId}`);
    this.userInbox = response.data
  },
  computed: {
    user() {
      return this.$store.state.user
    },
    is_staff() {
      if (!this.userInbox) {
        return false
      }

      const role = this.userInbox.role
      return (this.user && this.user.is_superuser) || (role && (role === 'AGENT' || role === 'MANAGER'))
    }
  }
}
</script>

<style scoped>

</style>