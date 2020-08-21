<template>
    <div class="flex w-full my-1">
        <avatar :source="notification.receiver.avatar_url" class="h-12 m-2"></avatar>
        <div class="flex-grow m-2 pl-2 border-l-4" :style="borderColor">
            <div class="flex-row" v-if="notification.read">
                <a :href="ticketUrl">{{ notification.get_ticket.title }}</a> <span class="text-sm">{{ notification.get_author }} - <span class="whitespace-no-wrap">{{ date }}</span></span>
            </div>
            <div class="flex-row font-semibold" v-else>
                <a :href="ticketUrl">{{ notification.get_ticket.title }}</a> <span class="text-sm">{{ notification.get_author }} - <span class="whitespace-no-wrap">{{ date }}</span></span>
            </div>
            <div class="flex-row">
                {{ notification.get_content }}
            </div>
        </div>
        <div class="py-2">
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
            date: function () {
                return moment.parseZone(this.notification.date_created).fromNow()
            },
            borderColor() {
                return {
                    "border-color": this.notification.get_inbox.color
                }
            },
            ticketUrl() {
                return `/inboxes/${this.notification.get_inbox.id}/tickets/${this.notification.get_ticket.ticket_inbox_id}`
            }
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