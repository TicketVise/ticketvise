<template>
  <div id="app">
    <AppLayout>
      <router-view :key="$route.fullPath" />
    </AppLayout>
  </div>
</template>

<script>
export default {
  name: 'App',
  mounted () {
    // if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    //   document.documentElement.classList.add('dark')
    // } else {
    //   document.documentElement.classList.remove('dark')
    // }
    document.documentElement.classList.remove('dark')
  }
}
</script>
