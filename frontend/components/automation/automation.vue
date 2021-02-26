<template>
  <div class="w-screen max-w-screen-lg mx-auto px-4 mb-4">
    <div class="text-center my-4">
      <span class="text-gray-400 font-medium">Automation</span>
      <h1 class="text-gray-800 text-3xl font-semibold">Enhance ticket assignment</h1>
    </div>

    <!-- Actions header -->
    <div class="mb-1">
      <h2 class="text-gray-700 text-xl font-bold leading-6">Actions</h2>
      <span class="text-gray-400">Perform actions to incoming tickets based on given conditions.</span>
    </div>
    <div class="flex flex-col space-y-2 mb-4">
      <draggable :animation="200" ghost-class="moving-card" :list="items" handle=".handle" class="space-y-2">
        <automation-filter v-for="i of items" :key="i"/>
      </draggable>
      <button @click="items.push(items.length)" class="relative flex items-center space-x-2 text-orange-500 cursor-pointer self-center focus:outline-none">
        <i class="fa fa-plus"></i>
        <span>Add another filter</span>
      </button>
    </div>

    <!-- Default header -->
    <div class="mb-1">
      <h2 class="text-gray-700 text-xl font-bold leading-6">Default</h2>
      <span class="text-gray-400">What to do with a ticket if no action applies.</span>
    </div>
    <!-- Default card -->
    <automation-default></automation-default>
  </div>
</template>

<script>
import Draggable from 'vuedraggable'

export default {
  name: "Automation",
  components: { Draggable },
  data: () => ({
    items: [0]
  })
}
</script>

<style></style>
