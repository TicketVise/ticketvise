<template>
    <div class="container divide-y-2 divide-y-m-2 divide-gray-400">
        <notification-card v-for="notification in notifications.results" :key="notification.id"
                           :notification="notification"></notification-card>
        <submit-button v-on:click.native=prevPage() text="Prev" class="m-2"
                       v-if="notifications.previous"></submit-button>
        <submit-button v-on:click.native=nextPage() text="Next" class="m-2" v-if="notifications.next"></submit-button>
    </div>
</template>

<script>
    import axios from "axios";
    import NotificationCard from "./NotificationCard";
    import SubmitButton from "../elements/buttons/SubmitButton";

    export default {
        name: "Notifications",
        components: {SubmitButton, NotificationCard},
        data() {
            return {
                notifications: []
            }
        },
        created() {
            axios.get("/api/notifications").then(response => {
                this.notifications = response.data
            })
        },
        methods: {
            nextPage() {
                if (this.notifications.next) {
                    let page_num = this.notifications.next.substring(this.notifications.next.indexOf("=") + 1);
                    axios.get("/api/notifications", {params: {page: page_num}}).then(response => {
                        this.notifications = response.data
                    })
                }
            },
            prevPage() {
                if (this.notifications.previous) {
                    let page_num = this.notifications.previous.substring(0, this.notifications.previous.indexOf("="));
                    if (!page_num) {
                        axios.get("/api/notifications").then(response => {
                            this.notifications = response.data
                        })
                    } else {
                        axios.get("/api/notifications", {params: {page: page_num}}).then(response => {
                            this.notifications = response.data
                        })
                    }
                }
            }
        }
    }
</script>

<style scoped>

</style>