<template>
  <div
    class="py-2 h-16 absolute bottom-0 w-full border-t border-primary flex items-center justify-evenly bg-white"
  >
    <router-link :to="`/inboxes/${$route.params.inboxId}/overview`" exact class="menu-item" active-class="active">
      <HomeIcon class="h-5 w-5" />
      <span>Overview</span>
    </router-link>
    <router-link :to="`/inboxes/${$route.params.inboxId}/tickets`" exact class="menu-item" active-class="active">
      <InboxStackIcon class="h-5 w-5" />
      <span>Tickets</span>
    </router-link>
    <router-link :to="`/inboxes/${$route.params.inboxId}/tickets/new`" exact class="menu-item emphasized">
      <PlusIcon class="h-5 w-5" />
      <span>New</span>
    </router-link>
    <router-link :to="`/inboxes/${$route.params.inboxId}/insights`" exact class="menu-item" active-class="active">
      <ChartBarIcon class="h-5 w-5" />
      <span>Insights</span>
    </router-link>
    <router-link :to="`/inboxes/${$route.params.inboxId}/settings`" exact class="menu-item" active-class="active">
      <Cog8ToothIcon class="h-5 w-5" />
      <span>Settings</span>
    </router-link>
  </div>
</template>

<script>
import { HomeIcon, InboxStackIcon, PlusIcon, Cog8ToothIcon, ChartBarIcon } from "@heroicons/vue/24/outline";

export default {
  name: "MenuBottom",
  components: {
    HomeIcon,
    InboxStackIcon,
    PlusIcon,
    Cog8ToothIcon,
    ChartBarIcon
  },
};
</script>

<style scoped>
.menu-item {
  @apply py-1 px-2 text-xs flex flex-col items-center justify-center rounded-md;
}

.emphasized {
  @apply text-white bg-primary w-14;
}

.active {
  @apply bg-gray-100;
}
</style>
