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
      // Remove parameters from URL if LTI launch (in this case token is a query param)
      if (params.get("token")) {
        window.history.replaceState({}, document.title, "/");
      }

      this.$store.dispatch("relogin", {token, inboxId})
    }
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