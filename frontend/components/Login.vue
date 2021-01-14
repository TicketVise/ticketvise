<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full">
      <div>
        <div class="mx-auto flex items-center justify-center">
          <img class="h-8 w-8" src="/static/img/logo/logo.svg" alt="Logo">
          <span class="text-2xl ml-2 text-gray-800">Ticket</span><span
            class="text-2xl text-primary font-bold">Vise</span>
        </div>
        <h2 class="mt-6 text-center text-3xl leading-9 font-extrabold text-gray-900">
          Sign in to your account
        </h2>
      </div>
      <form class="mt-8 bg-white shadow rounded p-6" method="POST" @submit.prevent="login">
        <div class="rounded-md shadow-sm">
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="username">
              Username
            </label>
            <input v-model="username"
                class="appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none"
                id="username" type="text" placeholder="user@example.com" name="username" autofocus>
          </div>
          <div class="mb-6">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="password">
              Password
            </label>
            <input
                class="appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none"
                id="password" type="password" placeholder="••••••••••••••••" name="password" v-model="password">
          </div>
        </div>

        <div class="mt-6">
          <button type="submit"
                  class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm leading-5 font-medium rounded-md text-white bg-primary hover:bg-orange-500 focus:outline-none focus:border-orange-700 focus:shadow-outline-orange active:bg-orange-700 transition duration-150 ease-in-out">
            <span class="absolute left-0 inset-y-0 flex items-center pl-3">
              <svg class="h-5 w-5 text-orange-200 group-hover:text-orange-200 transition ease-in-out duration-150"
                   fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd"
                      d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z"
                      clip-rule="evenodd"/>
              </svg>
            </span>
            Sign in
          </button>
        </div>
      </form>
      <p class="text-center text-gray-500 text-xs mt-2">
        &copy;<span v-text="new Date().getFullYear()"/> TicketVise. All rights reserved.
      </p>
    </div>
  </div>

</template>

<script>
export default {
  name: "Login",
  data: () => ({
    username: "",
    password: ""
  }),
  methods: {
    login: function () {
      const payload = {
        username: this.username,
        password: this.password
      }

      this.$store.dispatch("login", payload)
    }
  }
}
</script>

<style scoped>

</style>