<template>
  <div class="flex overflow-hidden">
    <img :alt="user.first_name  + ' ' + user.last_name" :key="user.id" :src="user.avatar_url"
         :title="user.first_name + ' ' + user.last_namew" class="inline-block h-8 w-8 rounded-full text-white shadow-solid" v-bind:class="{ '-ml-2': i !== 0}"
         v-for="(user, i) in users">
  </div>
</template>

<script>
  export default {
    props: {
      users: {
        default: []
      }
    }
  }
</script>

<style scoped>

</style>
