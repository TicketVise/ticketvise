<template>
  <div>
    <navigation v-if="show_navigation">
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
  mounted() {
    const params = new URLSearchParams(window.location.search);
    const token = params.get("token") || localStorage.getItem("token")
    const inboxId = params.get("inbox_id")
    if (token) {
      localStorage.setItem("token", token)
      this.$store.dispatch("relogin", inboxId)
    }

    // remove parameters from URL
    window.history.replaceState({}, document.title, "/");
  },
  computed: {
    show_navigation() {
      return this.$store.getters.isAuthenticated
    }
  }
}
</script>

<style scoped>

</style>