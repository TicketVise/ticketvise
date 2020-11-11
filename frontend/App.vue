<template>
  <div>
    <h1>Test</h1>
    <router-link to="/">inboxes</router-link>
    <router-view></router-view>
  </div>
</template>

<script>

export default {
  name: "App",
  mounted() {
    const params = new URLSearchParams(window.location.search);
    const token = params.get("token")
    if (token) {
      localStorage.setItem("token", token)
    }
  }
}
</script>

<style scoped>

</style>