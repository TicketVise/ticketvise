<template>
    <div class="flex overflow-hidden">
        <img class="inline-block h-8 w-8 rounded-full text-white shadow-solid" v-for="(user, i) in users" :key="user.id"
             v-bind:class="{ '-ml-2': i !== 0}" :src="user.avatar_url" :alt="user.first_name  + ' ' + user.last_name">
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