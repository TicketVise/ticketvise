<template>
    <div class="container">
        <notification-card v-for="notification in notifications" :key="notification.id"
                           :notification="notification"></notification-card>
    </div>
</template>

<script>
    import axios from "axios";
    import NotificationCard from "./NotificationCard";

    export default {
        name: "Notifications",
        components: {NotificationCard},
        data() {
            return {
                notifications: null
            }
        },
        created() {
            axios.get("/api/notifications").then(response => {
                this.notifications = response.data
            })
        }
    }
</script>

<style scoped>

</style>