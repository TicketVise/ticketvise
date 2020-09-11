<template>
  <img :src="source" alt="Profile picture" class="object-center object-cover rounded-full flex-shrink-0">
</template>

<script>
  export default {
    props: ["source"],
  }
</script>

<style scoped>

</style>