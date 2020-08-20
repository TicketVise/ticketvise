<template>
    <div class="container divide-y-2 divide-y-m-2 divide-gray-400">
        <nav class="m-3">
            <div class="grid grid-cols-3 divide-x divide-gray-400">

            <div @click="toggleAll" class="text-center font-semibold" v-if="read === ''">All</div>
            <a @click="toggleAll" class="text-center" v-else>All</a>

            <div @click="toggleRead" class="text-center font-semibold" v-if="read === 'True'">Read</div>
            <a @click="toggleRead" class="text-center" v-else>Read</a>

            <div @click="toggleUnread" class="text-center font-semibold" v-if="read === 'False'">Unread</div>
            <a @click="toggleUnread" class="text-center" v-else>Unread</a>
            </div>
        </nav>
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
    import SearchBar from "../elements/SearchBar";

    export default {
        name: "Notifications",
        components: {SearchBar, SubmitButton, NotificationCard},
        data() {
            return {
                notifications: [],
                search: "",
                read: "",
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
            },
            getNotifications() {
                axios.get("/api/notifications", {
                    params: {
                        search: this.search,
                        read: this.read
                    }}).then(response => {
                    this.notifications = response.data
                })
            },
            toggleRead(){
                this.read = "True";
                this.getNotifications()
            },
            toggleUnread(){
                this.read = "False";
                this.getNotifications()
            },
            toggleAll(){
                this.read = "";
                this.getNotifications()
            }
        }
    }
</script>

<style scoped>

</style>