<template>
    <card outlined class="flex w-full mt-3">
        <avatar :source="notification.receiver.avatar_url" class="h-12 m-2"></avatar>
        <div>
            {{ notification.get_title }}
        </div>
    </card>
</template>

<script>
    import Avatar from "../elements/Avatar";

    export default {
        name: "NotificationCard",
        components: {Avatar},
        props: {notification: {type: Object, default: null, required: true}}
    }
</script>

<style scoped>

</style>