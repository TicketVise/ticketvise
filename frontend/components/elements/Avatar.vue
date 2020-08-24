<template>
  <img :class="size" :src="source" alt="Profile picture" class="object-center object-cover rounded-full">
</template>

<script>
  export default {
    props: ["source", "size"],
  }
</script>

<style scoped>

</style>