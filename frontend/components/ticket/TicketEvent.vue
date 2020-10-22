<template>
  <div class="flex w-full">
    <div class="w-12 m-3 flex-shrink-0 mb-2"/>
    <div class="ml-3 flex text-sm flex-grow"
         :class="{'border-gray-400 border-b-2 mb-4': ticket_event.new_status === `CLSD`}">
      <div class="flex flex-col">
        <div class="flex flex-shrink-0 w-6 h-6 bg-gray-100 rounded-full mr-2 items-center justify-center text-gray-500"
          :class="{'bg-red-500': ticket_event.new_status === 'CLSD', 'bg-green-500': ticket_event.old_status === 'CLSD'}">
          <i class="fa" v-bind:class="{
                  'fa-user': ticket_event.hasOwnProperty('assignee'),
                  'fa-tag': ticket_event.hasOwnProperty('label'),
                  'fa-share-alt': ticket_event.hasOwnProperty('shared_with_users'),
                  'fa-circle text-xs': ticket_event.hasOwnProperty('new_status'),
                  'fa-file text-xs': ticket_event.hasOwnProperty('file'),
                  'text-white': ticket_event.new_status === 'CLSD' || ticket_event.old_status === 'CLSD'}"/>
        </div>
        <div class="ml-3 h-full border-l border-gray-400 w-1"/>
      </div>

      <div class="flex items-center flex-grow" :class="{
        'pb-4': ticket_event.new_status === 'CLSD',
        'pb-6': ticket_event.new_status !== 'CLSD'
      }">

        <div v-if="ticket_event.labels" class="inline-block" >
          <avatar v-if="ticket_event.initiator" :source="ticket_event.initiator.avatar_url" class="inline-block w-5 h-5 mr-1"/>
          <span class="font-medium">{{ full_name(ticket_event.initiator) }}</span>
          <span v-if="ticket_event.initiator">has <span v-if="ticket_event.is_added">added</span><span
              v-else>removed</span>
            the</span>
          <span v-else>The label<span v-if="ticket_event.labels.length > 1">s</span></span>
          <chip :background="label.color" :key="`label-${label.id}`"
                v-bind:class="{'mr-1' : i !== ticket_event.labels.length - 1 }"
                v-for="(label, i) in ticket_event.labels">
            {{ label.name }}
          </chip>
          <span v-if="ticket_event.initiator">label<span v-if="ticket_event.labels.length > 1">s</span></span>
          <span v-else>has been <span v-if="ticket_event.is_added">added</span><span v-else>removed</span></span>
          <span class="lowercase">{{ date(ticket_event.date_created) }}</span>
        </div>

        <div v-else-if="ticket_event.assignee" class="inline-block">
          <avatar v-if="ticket_event.initiator" :source="ticket_event.initiator.avatar_url" class="inline-block w-5 h-5 mr-1"/>
          <span class="font-medium">{{ full_name(ticket_event.initiator) }}</span>
          <span v-if="ticket_event.initiator">has assigned the ticket to</span>
          <span v-else>The ticket has been assigned to</span>
          <chip class="ml-1">
            <avatar :source="ticket_event.assignee.avatar_url" class="w-3 h-3"/>
            <span class="ml-2">{{ full_name(ticket_event.assignee) }}</span>
          </chip>
          <span class="ml-1 lowercase">{{ date(ticket_event.date_created) }}</span>
        </div>

        <div v-else-if="ticket_event.new_status" class="inline-block">
          <avatar v-if="ticket_event.initiator" :source="ticket_event.initiator.avatar_url" class="inline-block w-5 h-5 mr-1"/>
          <span class="font-medium">{{ full_name(ticket_event.initiator) }}</span>
          <span v-if="ticket_event.initiator">has changed the status to</span>
          <span v-else>The status has been changed to </span>
          <chip class="ml-1">{{ status[ticket_event.new_status] }}</chip>
          <span class="ml-1 lowercase">{{ date(ticket_event.date_created) }}</span>
        </div>

        <div v-else-if="ticket_event.attachments" class="flex flex-col flex-grow">
          <div class="inline-block mb-2">
            <avatar :source="ticket_event.uploader.avatar_url" class="inline-block w-5 h-5 mr-1"/>
            <span class="font-medium">{{ full_name(ticket_event.uploader) }}</span> uploaded
            <span v-if="ticket_event.attachments.length > 1">{{ ticket_event.attachments.length }}</span>
            <span v-else>a</span>
            attachment<span v-if="ticket_event.attachments.length > 1">s</span>
            <span class="lowercase">{{ date(ticket_event.date_created) }}</span>
          </div>
          <div class="w-full grid sm:grid-cols-2 xl:grid-cols-3 gap-4">
            <attachment v-for="attachment in ticket_event.attachments" :key="`attachment-${attachment.id}`"
                        class="mr-1" :attachment="attachment" :show-delete="false"/>
          </div>
        </div>

        <div v-else-if="ticket_event.shared_with_users" class="inline-block">
          <avatar v-if="ticket_event.sharer" :source="ticket_event.sharer.avatar_url"
                  class="inline-block w-5 h-5 mr-1"/>
          <span v-if="ticket_event.sharer" class="font-medium">{{ full_name(ticket_event.sharer) }}</span>
          <span v-if="ticket_event.sharer">has shared the ticket with</span>
          <span v-else>The ticket has been shared with</span>
          <chip :key="`shared-with-${user.id}`"
                v-bind:class="{'mr-1' : i !== ticket_event.shared_with_users.length - 1 }"
                v-for="(user, i) in ticket_event.shared_with_users">
            <avatar :source="user.avatar_url" class="w-3 h-3"/>
            <span class="ml-2">{{ full_name(user) }}</span>
          </chip>
          <span class="ml-1 lowercase">{{ date(ticket_event.date_created) }}</span>
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
  props: ["ticket_event"],
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
    },
  }
}
</script>

<style scoped>

</style>