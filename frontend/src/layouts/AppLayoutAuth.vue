<template>
  <div>
    <slot />

    <develop-panel v-if="development" />
  </div>
</template>

<script>
import DevelopPanel from '@/components/devpanel/DevelopPanel.vue'

export default {
  name: 'AppLayoutAuth',
  components: { DevelopPanel },
  computed: {
    development: () => process.env.NODE_ENV !== 'production'
  }
}
</script>
