<template>
  <div class="sm:px-0 grid md:grid-cols-3 gap-8">
    <inboxes-item :key="userInbox.inbox.id" v-for="userInbox in inboxes" :inbox="userInbox" />
  </div>
</template>

<script>
export default {
  props: {
    inboxes: {
      required: true,
      type: Array
    }
  }
}
</script>
