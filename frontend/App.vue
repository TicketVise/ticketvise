<template>
  <div>
    <navigation v-if="user && isAuthenticated" :user="user">
      <router-view></router-view>
    </navigation>
    <router-view v-else></router-view>
  </div>
</template>

<script>

import Navigation from "./components/Navigation";
import axios from "axios";

export default {
  name: "App",
  components: {Navigation},
  data: () => ({
    user: null,
  }),
  mounted() {
    const params = new URLSearchParams(window.location.search);
    const token = params.get("token")
    if (token) {
      localStorage.setItem("token", token)
    }

    axios.get('/api/me').then(response => {
      this.user = response.data
    })
  },
  computed: {
    isAuthenticated: function () {
      return localStorage.getItem("token") !== null
    }
  }
}
</script>

<style scoped>

</style>