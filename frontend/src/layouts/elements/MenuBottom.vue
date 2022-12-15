<template>
  <div
    class="py-2 h-16 fixed bottom-0 w-full border-t border-primary grid grid-cols-5 gap-2 px-2 bg-white"
  >
    <router-link :to="`/inboxes/${$route.params.inboxId}/overview`" exact :class="[is_staff ? '' : 'col-span-2', 'menu-item']" active-class="active">
      <HomeIcon class="h-5 w-5" />
      <span>Overview</span>
    </router-link>
    <router-link v-if="is_staff" :to="`/inboxes/${$route.params.inboxId}/tickets`" exact class="menu-item" active-class="active">
      <InboxStackIcon class="h-5 w-5" />
      <span>Tickets</span>
    </router-link>
    <router-link :to="`/inboxes/${$route.params.inboxId}/tickets/new`" exact class="menu-item emphasized">
      <PlusIcon class="h-5 w-5" />
      <span>New</span>
    </router-link>
    <router-link v-if="is_staff" :to="`/inboxes/${$route.params.inboxId}/insights`" exact class="menu-item" active-class="active">
      <ChartBarIcon class="h-5 w-5" />
      <span>Insights</span>
    </router-link>
    <router-link v-if="is_staff" :to="`/inboxes/${$route.params.inboxId}/settings`" exact class="menu-item" active-class="active">
      <Cog8ToothIcon class="h-5 w-5" />
      <span>Settings</span>
    </router-link>
    <router-link v-if="!is_staff" :to="`/inboxes/${$route.params.inboxId}/public`" exact class="menu-item col-span-2" active-class="active">
      <GlobeEuropeAfricaIcon class="h-5 w-5" />
      <span>Public</span>
    </router-link>
  </div>
</template>

<script>
import axios from "axios"
import { mapState } from "vuex"
import { HomeIcon, InboxStackIcon, PlusIcon, Cog8ToothIcon, ChartBarIcon, GlobeEuropeAfricaIcon } from "@heroicons/vue/24/outline";

export default {
  name: "MenuBottom",
  components: {
    HomeIcon,
    InboxStackIcon,
    PlusIcon,
    Cog8ToothIcon,
    ChartBarIcon,
    GlobeEuropeAfricaIcon
  },
  data: () => ({
    inbox: null
  }),
  async mounted() {
    const response = await axios.get(
      `/api/me/inboxes/${this.$route.params.inboxId}`
    )
    this.inbox = response.data
  },
  computed: {
    ...mapState({
      user: (state) => state.user,
    }),
    is_staff() {
      if (!this.inbox) {
        return false
      }

      const role = this.inbox.role
      return (
        (this.user && this.user.is_superuser) ||
        (role && (role === "AGENT" || role === "MANAGER"))
      )
    }
  }
};
</script>

<style scoped>
.menu-item {
  @apply py-1 px-2 text-xs flex flex-col items-center justify-center rounded-md text-gray-500;
}

.emphasized {
  @apply text-white bg-primary;
}

.active {
  @apply bg-gray-100 text-gray-800;
}
</style>
