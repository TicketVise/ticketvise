<template>
  <editor :isViewer="true" :initialValue="initialValue" />
</template>

<script>

import Editor from "./Editor";

export default {
  name: "Viewer",
  props: ["initialValue"],
  components: {Editor},
  comments: {
    Editor
  }
}
</script>

<style scoped>

</style>