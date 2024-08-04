<template>
  <component :is="layout">
    <slot />
  </component>

  <GettingStarted
    @update="user.give_introduction = false"
    v-if="onboarding.active && onboarding.popup"
  />
  <DevelopPanel v-if="development" />

  <SearchPopup :show="search" v-on:close="search = false" />
</template>

<script>
import AppLayoutDefault from './AppLayoutDefault.vue'
import AppLayoutAuth from './AppLayoutAuth.vue'
import AppLayoutGeneral from './AppLayoutGeneral.vue'
import AppLayoutInbox from './AppLayoutInbox.vue'
import AppLayoutTicket from './AppLayoutTicket.vue'
import { shallowRef, watch } from 'vue'
import { useRoute } from 'vue-router'
import { mapState, mapActions } from "vuex"
import onboardingStore from "@/store/modules/onboarding"

import GettingStarted from "@/components/onboarding/GettingStarted.vue"
import SearchPopup from "@/layouts/elements/SearchPopup.vue"
import DevelopPanel from "@/components/devpanel/DevelopPanel.vue"

export default {
  name: 'AppLayout',
  components: {
    GettingStarted,
    DevelopPanel,
    SearchPopup
  },
  data: () => ({
    search: false
  }),
  setup () {
    const layout = shallowRef(AppLayoutDefault)
    const route = useRoute()
    watch(
      () => route.meta,
      async meta => {
        switch (meta.layout) {
          case 'AppLayoutAuth':
            layout.value = AppLayoutAuth
            break
          case 'AppLayoutGeneral':
            layout.value = AppLayoutGeneral
            break
          case 'AppLayoutInbox':
            layout.value = AppLayoutInbox
            break
          case 'AppLayoutTicket':
            layout.value = AppLayoutTicket
            break
          case 'AppLayoutDefault':
            layout.value = AppLayoutDefault
            break
          default:
            console.error(`could not find layout: ${meta.layout}, defaulting to AppLayoutDefault`)
            layout.value = AppLayoutDefault
            break
        }
      }
    )
    return { layout }
  },
  methods: {
    checkIntroduction() {
      if (this.user.give_introduction && this.onboarding && typeof this.start === 'function') {
        this.start()
      }
    }
  },
  watch: {
    user: {
      handler() {
        this.checkIntroduction()
      },
      deep: true
    },
    onboarding: {
      handler() {
        this.checkIntroduction()
      },
      deep: true
    }
  },
  computed: {
    ...mapActions('onboarding', ['start']),
    ...mapState({
      user: (state) => state.user,
    }),
    ...mapState('onboarding', {
      onboarding: (state) => state.status
    }),
    development: () => import.meta.env.DEV,
  },
}
</script>
