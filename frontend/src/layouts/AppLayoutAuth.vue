<template>
  <div>
    <slot />
    <develop-panel v-if="true || development" />
  </div>
</template>

<script>
import DevelopPanel from '@/components/devpanel/DevelopPanel.vue'

export default {
  name: 'AppLayoutAuth',
  components: { DevelopPanel },
  computed: {
    development: () => import.meta.env.DEV
  }
}
</script>
