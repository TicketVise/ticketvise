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

export default {
  name: "App",
  components: {Navigation},
  computed: {
    show_navigation() {
      return this.$store.getters.isAuthenticated
    }
  }
}
</script>

<style scoped>

</style>