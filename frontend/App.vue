<template>
  <div>
    <!-- <navigation v-if="show_navigation">
      <router-view></router-view>
    </navigation>
    <router-view v-else></router-view> -->
    <component :is="layout">
      <router-view :key="$route.fullPath" />
      <!-- <router-view/> -->
    </component>
  </div>
</template>

<script>
const default_layout = 'default'

export default {
  name: "App",
  computed: {
    // show_navigation() {
    //   return this.$store.getters.isAuthenticated
    // }
    layout() {
      return (this.$route.meta.layout || default_layout) + '-layout'
    }
  }
}
</script>
