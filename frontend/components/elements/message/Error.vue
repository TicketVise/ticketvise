<template>
<div class="text-red-700 p-1 text-sm" role="alert">
  <p>{{message}}</p>
</div>
</template>

<script>
export default {
name: "error",
  props: ["message"]
}
</script>

<style scoped>

</style>