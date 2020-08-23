<template>
  <div class="flex-1 border rounded border-gray-700 border-opacity-50 border-t-0 bg-gray-100" :id="title">
    <div class="py-1 text-center border-t-2 bg-white rounded-tl rounded-tr" :style="`border-color: ${color};`">
      <p>{{ title }} (<strong>{{ ticketList.length }}</strong>)</p>

      <div class="is-marginless pretty p-icon p-round select-column" style="display: none;">
        <input
          autocomplete="off"
          type="checkbox"
          name="select-column-checkbox"
          :value="title"
          class="select-column-checkbox"
          :id="`select-column-${title}`"/>
        <div class="state">
          <i class="icon fa fa-check"></i>
          <label></label>
        </div>
      </div>
    </div>

    <div class="border-t border-gray-700 border-opacity-50 overflow-y-auto max-h-screen">
      <div class="p-2 space-y-2" :id="`${title}-tickets`" v-if="title != 'Closed'">
        <ticket-card
          v-for="ticket in ticketList"
          :key="ticket.id"
          :ticket="ticket" />
      </div>
      <div class="p-2 space-y-2" :id="`${title}-tickets`" v-else>
        <ticket-card
          v-for="ticket in ticketList"
          :key="ticket.id"
          :ticket="ticket"
          small />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['title', 'color', 'ticketList']
}
</script>

<style>

</style>
