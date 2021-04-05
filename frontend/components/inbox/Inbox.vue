<template>
  <main class="flex-1 relative z-0 focus:outline-none" tabindex="0">
    <div class="items-stretch overflow-y-hidden">
      <getting-started @update="user.give_introduction = false" v-if="is_staff && user && user.give_introduction"></getting-started>
      <div class="flex flex-row flex-grow h-full max-w-full pt-16 -mt-16">
        <div id="scrollable-content" class="flex flex-col w-full overflow-x-hidden overflow-y-auto">
          <router-view></router-view>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
  import axios from "axios";
  import GettingStarted from "../setup/GettingStarted";

  export default {
    name: "Inbox",
    components: {GettingStarted},
    data: () => ({
      userInbox: null,
      side: false,
    }),
    async mounted() {
      const response = await axios.get(`api/me/inboxes/${this.$route.params.inboxId}`);
      this.userInbox = response.data
    },
    computed: {
      user() {
        return this.$store.state.user
      },
      is_staff() {
        if (!this.userInbox) {
          return false
        }

        const role = this.userInbox.role
        return (this.user && this.user.is_superuser) || (role && (role === 'AGENT' || role === 'MANAGER'))
      },
    }
  }
</script>

<style scoped>

</style>
