<template>
    <card outlined>
        <div class="flex items-center border-b border-gray-400 p-3">
            <avatar :source="author.avatar_url" class="h-16 w-16"></avatar>
            <div class="px-4">
                <div class="font-semibold text-gray-800 mb-1">{{ author.first_name }} {{ author.last_name }}</div>
                <span v-if="role" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-200 text-gray-800">
                    {{role.label}}
                </span>
            </div>
        </div>
        <div class="p-3">
            <h4 class="font-semibold text-gray-800 mb-2">Recent questions</h4>
            <ul class="list-none">
                <li v-for="ticket in tickets" :key="ticket.id">
                    <a class="block my-1 px-2 py-1 bg-gray-100 rounded hover:bg-gray-200 text-sm"
                       :href="'/inboxes/' + inbox_id + '/tickets/' + ticket.ticket_inbox_id">
                        <span class="font-semibold mr-2">#{{ticket.ticket_inbox_id}}</span>{{ticket.title}}
                    </a>
                </li>
            </ul>
        </div>
    </card>
</template>

<script>
    import Avatar from "../elements/Avatar";
    import Card from "../elements/card/Card";

    import axios from "axios";

    export default {
        name: "AuthorCard",
        components: {Card, Avatar},
        props: ["author", "inbox_id"],
        data() {
            return {
                tickets: null,
                role: null,
            }
        },
        mounted() {
            axios.get("/api/inboxes/" + this.inbox_id + "/users/" + this.author.id + "/tickets/recent").then(response => {
                this.tickets = response.data;
            });
            axios.get("/api/inboxes/" + this.inbox_id + "/users/" + this.author.id + "/roles").then(response => {
                this.role = response.data;
            })
        }
    }
</script>

<style scoped>

</style>
