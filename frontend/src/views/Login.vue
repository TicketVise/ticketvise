<template>
  <div class="min-h-screen bg-white dark:bg-gray-800 flex">
    <div class="flex-1 flex flex-col justify-center py-12 px-4 sm:px-6 lg:flex-none lg:px-20 xl:px-24">
      <div class="mx-auto w-full max-w-sm lg:w-96">
        <div>
          <div class="font-ticketvise mx-auto flex items-center">
            <img class="h-8 w-auto" :src="logo" alt="TicketVise" />
            <span class="text-2xl ml-2 text-gray-800 dark:text-white font-bold">Ticket</span><span
                  class="text-2xl text-primary font-bold">Vise</span>
          </div>
          <h2 class="mt-6 text-3xl font-extrabold text-gray-900 dark:text-white">
            Sign in to your account
          </h2>
        </div>

        <div class="mt-4">
          <div class="rounded-md bg-yellow-50 p-4 mb-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <ExclamationIcon class="h-5 w-5 text-yellow-400" aria-hidden="true" />
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-yellow-800">
                  Login is unavailable
                </h3>
                <div class="mt-2 text-sm text-yellow-700">
                  <p>
                    We currently only support login via Canvas, so please go to TicketVise through the course page in Canvas. We are working on a solution to login via SURFconext.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div>
            <div>
              <p class="text-sm font-medium text-gray-700 dark:text-gray-200">
                Sign in with
              </p>

              <div class="mt-1 grid grid-cols-2 gap-3">
                <div>
                  <a href="https://canvas.uva.nl" class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 dark:border-white rounded-md shadow-sm bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 hover:bg-gray-50 dark:hover:bg-gray-700">
                    <span class="sr-only">Go to Canvas</span>
                    <img class="h-6 w-auto dark:filter dark:invert" :src="canvas" alt="Canvas">
                  </a>
                </div>

                <div>
                  <button disabled class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 dark:border-white rounded-md shadow-sm bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 cursor-not-allowed">
                    <span class="sr-only">Sign in with SURFconext</span>
                    <img class="h-6 w-auto filter opacity-20 dark:filter dark:invert" :src="surfconext" alt="SURFconext">
                  </button>
                </div>
              </div>
            </div>

            <div class="mt-6 relative">
              <div class="absolute inset-0 flex items-center" aria-hidden="true">
                <div class="w-full border-t border-gray-300" />
              </div>
              <div class="relative flex justify-center text-sm">
                <span class="px-2 bg-white dark:bg-gray-800 text-gray-500 dark:text-gray-500">
                  Or continue with
                </span>
              </div>
            </div>
          </div>

          <form class="mt-6" method="POST" @submit.prevent="login">
            <div class="space-y-6">
              <div>
                <label for="username" class="block text-sm font-medium text-gray-700 dark:text-white">
                  Username
                </label>
                <div class="mt-1">
                  <input v-model="username" id="username" name="username" type="username" autocomplete="username" required="" class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm dark:bg-gray-700 dark:text-white" />
                </div>
              </div>

              <div class="space-y-1">
                <label for="password" class="block text-sm font-medium text-gray-700 dark:text-white">
                  Password
                </label>
                <div class="mt-1">
                  <input v-model="password" id="password" name="password" type="password" autocomplete="current-password" required="" class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm dark:bg-gray-700 dark:text-white" />
                </div>
              </div>

              <!-- <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <input id="remember_me" name="remember_me" type="checkbox" class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded" />
                  <label for="remember_me" class="ml-2 block text-sm text-gray-900 dark:text-white">
                    Remember me
                  </label>
                </div>

                <div class="text-sm">
                  <a href="#" class="font-medium text-primary-600 hover:text-primary-500">
                    Forgot your password?
                  </a>
                </div>
              </div> -->

              <div>
                <button type="submit" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                  Sign in
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div class="hidden lg:block relative w-0 flex-1">
      <img class="absolute inset-0 h-full w-full object-cover" src="https://images.unsplash.com/photo-1504275107627-0c2ba7a43dba?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=967&q=80" alt="Background image" />
    </div>
  </div>
</template>

<script>
import { ExclamationIcon } from '@heroicons/vue/solid'

import Logo from '@/assets/logo/logo.svg'
import SurfConext from '@/assets/img/ext/surfconext.png'
import Canvas from '@/assets/img/ext/canvas.svg'

export default {
  name: 'Login',
  components: {
    ExclamationIcon
  },
  data: () => ({
    username: '',
    password: '',
    error: '',
    logo: Logo,
    surfconext: SurfConext,
    canvas: Canvas
  }),
  methods: {
    login: function () {
      const payload = {
        username: this.username,
        password: this.password
      }

      this.$store.dispatch('login', payload)
        .then(() => console.log('testt'))
        .catch(_ => (this.error = 'Incorrect username or password.'))
    }
  }
}
</script>
