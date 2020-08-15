<template>
    <img :src="source" alt="Profile picture" class="object-center object-cover rounded-full" :class="size">
</template>

<script>
    export default {
        props: ["source", "size"],
    }
</script>

<style scoped>

</style>