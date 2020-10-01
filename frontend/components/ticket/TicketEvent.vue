<template>
  <div class="flex w-full">
    <div class="w-12 m-3 flex-shrink-0"/>
    <div class="ml-3 flex text-sm">
      <div class="flex flex-col ">
        <div class="flex flex-shrink-0 w-6 h-6 bg-gray-100 rounded-full mr-2 items-center justify-center text-gray-500">
          <i class="fa" v-bind:class="{
                  'fa-user': event.hasOwnProperty('assignee'),
                  'fa-tag': event.hasOwnProperty('label'),
                  'fa-bolt': event.hasOwnProperty('new_status'),
                  'fa-file text-xs': event.hasOwnProperty('file')}"/>
        </div>
        <div class="ml-3 h-full border-l border-gray-400 w-1"/>
      </div>

      <div class="flex pb-6 items-center">
        <div v-if="event.initiator" class="flex flex-row font-medium items-center mr-1">
          <avatar :source="event.initiator.avatar_url" class="w-5 h-5 mr-2"/>
          {{ full_name(event.initiator) }}
        </div>

        <div v-if="event.labels">
          <span v-if="event.initiator">has <span v-if="event.is_added">added</span><span v-else>removed</span>
            the</span>
          <span v-else>The label<span v-if="event.labels.length > 1">s</span></span>
          <chip :background="label.color" :key="`label-${label.id}`"
                v-bind:class="{'mr-1' : i !== event.labels.length - 1 }"
                v-for="(label, i) in event.labels">
            {{ label.name }}
          </chip>
          <span v-if="event.initiator">label<span v-if="event.labels.length > 1">s</span></span>
          <span v-else>has been <span v-if="event.is_added">added</span><span v-else>removed</span></span>
          <span class="lowercase">{{ date(event.date_created) }}</span>
        </div>

        <div v-else-if="event.assignee" class="flex flex-row items-center">
          <span v-if="event.initiator">has assigned the ticket to</span>
          <span v-else>The ticket has been assigned to</span>
          <chip class="ml-1">
            <avatar :source="event.assignee.avatar_url" class="w-4 h-4"/>
            <span class="ml-2">{{ full_name(event.assignee) }}</span>
          </chip>
          <span class="ml-1 lowercase">{{ date(event.date_created) }}</span>
        </div>

        <div v-else-if="event.new_status" class="flex flex-row items-center">
          <span v-if="event.initiator">has changed the status to</span>
          <span v-else>The status has been changed to </span>
          <chip class="ml-1">{{ status[event.new_status] }}</chip>
          <span class="ml-1 lowercase">{{ date(event.date_created) }}</span>

        </div>

        <div v-else-if="event.attachments" class="flex flex-col ">
          <div class="flex flex-row mb-2">
            <avatar :source="event.uploader.avatar_url" class="w-5 h-5 mr-2"/>
            <span class="font-medium mr-1">{{ full_name(event.uploader) }}</span> uploaded
            <span v-if="event.attachments.length > 1" class="mx-1">{{ event.attachments.length }}</span>
            <span v-else class="mx-1">a</span>
            attachment<span v-if="event.attachments.length > 1" >s</span>
            <span class="ml-1 lowercase">{{ date(event.date_created) }}</span>
          </div>
          <div class="w-full grid sm:grid-cols-2 xl:grid-cols-3 gap-4">
            <attachment v-for="(attachment, index) in event.attachments" :key="`label-${attachment.id}`"
                        class="mr-1" :attachment="attachment" @remove="event.attachments.splice(index, 1)"/>
          </div>
        </div>
      </div>

    </div>

  </div>
</template>

<script>
import Avatar from "../elements/Avatar";
import Chip from "../elements/chip/Chip";
import {calendarDate} from "../../utils";
import Attachment from "./Attachment";

export default {
  name: "TicketEvent",
  props: ["event"],
  components: {
    Attachment,
    Avatar,
    Chip,
  },
  data() {
    return {
      date: calendarDate,
      status: {
        PNDG: 'Pending',
        ASGD: 'Assigned',
        ANSD: 'Awaiting response',
        CLSD: 'Closed'
      }
    }
  },
  methods: {
    full_name: function (user) {
      return `${user.first_name} ${user.last_name}`
    }
  },

}
</script>

<style scoped>

</style>