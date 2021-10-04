<template>
  <EmailStatus />
</template>

<script>

import EmailStatus from './EmailStatus.vue'
import EmailSetup from './EmailSetup.vue'

export default {
  name: 'Email',
  components: {
    EmailStatus,
    EmailSetup
  },
  data: () => ({
    showSetupModal: false
  }),
  props: {
    label: {
      type: String,
      required: false,
      default: ''
    },
    checked: {
      type: Boolean,
      required: false,
      default: false
    }
  }
}
</script>

<style>

</style>
