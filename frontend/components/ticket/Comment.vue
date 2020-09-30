<template>
  <div class="flex w-full">
    <avatar :source="comment.author.avatar_url" class="w-12 h-12 m-3"/>
    <div class="flex flex-col flex-grow">
      <card class="flex-grow w-full" outlined>
        <div class="flex bg-gray-100 pl-2 pr-1 py-1 border-b border-gray-400 items-center">
          <span class="font-semibold text-sm">
            {{ comment.author.first_name }} {{ comment.author.last_name }}
          </span>
          <span class="text-xs ml-1 hidden md:block">
            @{{ comment.author.username }}
          </span>
          <span class="text-xs flex-grow ml-1">· {{ date(comment.date_created) }}</span>
          <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-200 text-gray-800">
            {{ comment.role.label }}
          </span>
        </div>
        <viewer :initialValue="content" class="px-2"></viewer>
      </card>
      <div class="h-6 border-l border-gray-400 w-1 mx-6"/>
    </div>
  </div>
</template>

<script>
import Card from '../../components/elements/card/Card';
import Viewer from "../elements/markdown/Viewer";
import {calendarDate} from "../../utils";

export default {
  name: "comment",
  props: ["comment", "reply", "ticket", "connected"],
  components: {
    Card,
    Viewer
  },
  methods: {
    date: calendarDate
  },
  computed: {
    content: function () {
      if (!this.comment) {
        return ""
      }

      var content = this.comment.content
      const matches = content.match(/\B(#\d+\b)(?!;)/g)
      if (matches) {
        for (const match of matches) {
          const url = `/inboxes/${this.ticket.inbox}/tickets/${match.substring(1)}`
          content = content.replace(match, `[${match}](${url})`)
        }
      }

      return content
    }
  }
}

</script>

<style scoped>

</style>
