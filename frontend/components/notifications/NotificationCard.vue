<template>
    <div class="flex w-full my-1">
        <avatar :source="notification.receiver.avatar_url" class="h-12 m-2"></avatar>
        <div class="flex-grow m-2">
            <div class="flex-row" v-if="notification.read">
                <a :href="notification.get_ticket_url">{{ notification.get_title }}</a> <span class="text-sm">{{ notification.get_author }} - {{ date }}</span>
            </div>
            <div class="flex-row font-semibold" v-else>
                <a :href="notification.get_ticket_url">{{ notification.get_title }}</a> <span class="text-sm">{{ notification.get_author }} - {{ date }}</span>
            </div>
            <div class="flex-row">
                {{ notification.get_content }}
            </div>
        </div>
        <div class="my-2">
            <button class="fa fa-envelope" v-if="!notification.read" @click="flipRead()"></button>
            <button class="fa fa-envelope-open-o" v-if="notification.read" @click="flipRead()"></button>
        </div>
    </div>
</template>

<script>
    import Avatar from "../elements/Avatar";
    import moment from "moment"
    import axios from "axios"

    export default {
        name: "NotificationCard",
        components: {Avatar},
        props: {notification: {type: Object, default: null, required: true}},
        computed: {
            date: function (date_created) {
                return moment.parseZone(date_created).fromNow()
            },
        },
        methods: {
            flipRead() {
                let formData = new FormData;
                formData.append("read", this.notification.read ? "False" : "True");

                axios.defaults.xsrfCookieName = 'csrftoken';
                axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

                axios.put("/api/notifications/" + this.notification.id + "/read", formData).then(response => {
                    this.notification.read = response.data.read
                })
            }
        }
    }
</script>

<style scoped>

</style>