<template>
    <button class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm leading-5 font-medium rounded-md text-gray-700 bg-white hover:text-gray-500 focus:outline-none focus:shadow-outline-orange focus:border-orange-300 active:text-gray-800 active:bg-gray-50 active:text-gray-800">
        {{text}}
    </button>
</template>

<script>
    export default {
        name: "SubmitButton",
        props: ["text"]
    }
</script>

<style scoped>

</style>