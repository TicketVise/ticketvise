<template>
    <vue-tribute :options="options">
        <slot></slot>
    </vue-tribute>
</template>

<script>
    import VueTribute from 'vue-tribute';
    import axios from "axios";

    export default {
        components: {
            VueTribute
        }, name: "Mention",
        props: {
            users: {
                default: [],
                required: true
            },
            ticket: {
                required: true
            }
        },
        data() {
            const component = this

            const userConfig = {
                trigger: "@",
                containerClass: 'absolute mt-1 rounded-md bg-white shadow-lg overflow-hidden',
                itemClass: 'text-gray-900 cursor-default select-none relative py-2 pl-3 pr-9',
                selectClass: 'bg-gray-300',
                menuItemTemplate: function (item) {
                    const user = item.original
                    const full_name = user.first_name + " " + user.last_name

                    return `<div class="flex items-center space-x-3">
                                <img src="${user.avatar_url}" alt="Avatar of ${full_name}"
                                    class="flex-shrink-0 h-6 w-6 rounded-full">
                                <span class="font-normal block truncate">
                                    ${full_name}<span class="ml-1 text-xs font-bold">${user.username}</span>
                                </span>
                            </div>`
                },
                values: function(text, cb) {
                    cb(component.users)
                },
                lookup: function (user, mentionText) {
                    return JSON.stringify(user)
                },
                selectTemplate: function (item) {
                    return '@' + item.original.username;
                }

            }

            const ticketConfig = {
                trigger: "#",
                containerClass: 'absolute mt-1 rounded-md bg-white shadow-lg overflow-hidden',
                itemClass: 'text-gray-900 cursor-default select-none relative py-2 pl-3 pr-9',
                selectClass: 'bg-gray-300',
                menuItemTemplate: function (item) {
                    const ticket = item.original;

                    return `<div class="flex items-center space-x-3">
                                <span class="font-bold">${ticket.ticket_inbox_id}</span>
                                <span class="text-sm block truncate ml-1">${ticket.title}</span>
                            </div>`
                },
                values: function (text, cb) {
                    const ticket = component.ticket
                    if (!ticket) {
                        cb([])
                        return
                    }

                    axios.get("/api/inboxes/" + ticket.inbox + "/tickets", {
                        params: {
                            q: text
                        }
                    }).then(response => {
                        cb(response.data);
                    })
                },
                lookup: function (ticket, mentionText) {
                    return JSON.stringify(ticket)
                },
                selectTemplate: function (item) {
                    return "#" + item.original.ticket_inbox_id;
                }
            }

            return {
                options: {
                    collection: [ticketConfig, userConfig]
                }
            }
        }
    }
</script>

<style scoped>

</style>
