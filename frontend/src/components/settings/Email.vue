<template>
  <email-card :connected="connected" />
</template>

<script>

import EmailCard from './EmailCard.vue'

export default {
  name: 'Email',
  components: {
    EmailCard
  },
  props: {
    connected: {
      type: Boolean,
      required: true,
    }
  }
}
</script>

<style>

</style>
