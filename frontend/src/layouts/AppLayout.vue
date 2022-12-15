<template>
  <component :is="layout">
    <slot />
  </component>
</template>

<script>
import AppLayoutDefault from './AppLayoutDefault.vue'
import AppLayoutAuth from './AppLayoutAuth.vue'
import AppLayoutGeneral from './AppLayoutGeneral.vue'
import AppLayoutInbox from './AppLayoutInbox.vue'
import AppLayoutTicket from './AppLayoutTicket.vue'
import { shallowRef, watch } from 'vue'
import { useRoute } from 'vue-router'

export default {
  name: 'AppLayout',
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
  }
}
</script>
