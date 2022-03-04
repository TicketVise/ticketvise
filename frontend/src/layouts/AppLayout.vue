<template>
  <component :is="layout">
    <slot />
  </component>
</template>

<script>
import AppLayoutDefault from './AppLayoutDefault.vue'
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
        try {
          const component = await require(`@/layouts/${meta.layout}.vue`)
          console.log(component)
          layout.value = component?.default || AppLayoutDefault
        } catch (e) {
          console.log(e)
          layout.value = AppLayoutDefault
        }
      }
    )
    return { layout }
  }
}
</script>
