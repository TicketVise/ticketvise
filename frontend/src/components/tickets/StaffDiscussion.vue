<template>
  <div class="flex flex-column flex-wrap w-full">
    <div class="w-full">
      <div class="text-center mb-8" v-if="ticket?.comments.length === 0">
        <img
          alt="Nothing here"
          class="w-1/2 md:w-1/4 mx-auto mb-8"
          :src="relax"
        />
        <span class="text-sm leading-8 text-gray-500"
          >There are no messages here yet...</span
        >
      </div>
      <!-- <comment :comment="comment" :key="comment.id" :ticket="ticket" v-for="comment in comments"/> -->
      <div class="flow-root">
        <ul class="-mb-8">
          <li v-for="(item, itemIdx) in ticket?.comments" :key="item.id">
            <div class="relative pb-8">
              <span
                v-if="itemIdx !== ticket.comments.length - 1"
                class="absolute top-5 left-5 -ml-px h-full w-0.5 bg-gray-200"
                aria-hidden="true"
              />
              <div class="relative flex items-start space-x-3">
                <div class="relative">
                  <img
                    class="h-10 w-10 rounded-full bg-gray-400 flex items-center justify-center ring-8 ring-white"
                    :src="item?.imageUrl"
                    alt=""
                  />

                  <span
                    class="absolute -bottom-0.5 -right-1 bg-white rounded-tl px-0.5 py-px"
                  >
                    <ChatBubbleLeftEllipsisIcon
                      class="h-5 w-5 text-gray-400"
                      aria-hidden="true"
                    />
                  </span>
                </div>
                <div class="min-w-0 flex-1">
                  <div>
                    <div class="text-sm">
                      <a
                        :href="item?.person?.href"
                        class="font-medium text-gray-900"
                        >{{ item?.person?.name }}</a
                      >
                    </div>
                    <p class="mt-0.5 text-sm text-gray-500">
                      Commented {{ item?.date }}
                    </p>
                  </div>
                  <div class="mt-2 text-sm text-gray-700">
                    <p>
                      <TicketInputViewer v-if="item" :content="item.comment" />
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <div class="w-full">
      <div class="flex space-x-3">
        <div class="flex-shrink-0">
          <div class="relative">
            <img
              class="h-10 w-10 rounded-full bg-gray-400 flex items-center justify-center ring-8 ring-white"
              :src="user.avatar_url"
              alt=""
            />

            <span
              class="absolute -bottom-0.5 -right-1 bg-white rounded-tl px-0.5 py-px"
            >
              <!-- Heroicon name: solid/chat-alt -->
              <svg
                class="h-5 w-5 text-gray-400"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M18 5v8a2 2 0 01-2 2h-5l-5 4v-4H4a2 2 0 01-2-2V5a2 2 0 012-2h12a2 2 0 012 2zM7 8H5v2h2V8zm2 0h2v2H9V8zm6 0h-2v2h2V8z"
                  clip-rule="evenodd"
                />
              </svg>
            </span>
          </div>
        </div>
        <div class="min-w-0 flex-1">
          <form @submit.prevent="submit">
            <div>
              <TicketInput
                v-model="comment"
                ref="commentStaffInput"
                :staff="staff"
              />
              <p class="mt-1 text-sm text-gray-500">
                Type @ to mention a team member
              </p>
            </div>
            <div class="mt-6 flex items-center justify-end space-x-4">
              <button
                type="submit"
                class="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-600"
              >
                Comment
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ChatBubbleLeftEllipsisIcon } from "@heroicons/vue/24/solid";
import TicketInput from "@/components/inputs/TicketInput.vue";
import TicketInputViewer from "@/components/inputs/TicketInputViewer.vue";

import Relax from "@/assets/img/svg/relax.svg";

export default {
  components: {
    ChatBubbleLeftEllipsisIcon,
    TicketInput,
    TicketInputViewer,
  },
  props: {
    ticket: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    relax: Relax,
    comment: "",
    staff: [],
  }),
  mounted() {
    const { inboxId } = this.$route.params;

    axios.get(`/api/inboxes/${inboxId}/staff`).then((response) => {
      this.staff = response.data;
      this.staff.forEach((c) => {
        c.name = c.first_name + " " + c.last_name;
        c.avatar = c.avatar_url;
        c.username = c.username;
      });

      this.$refs.commentStaffInput.registerKeyUp(this.staff);
    });
  },
  methods: {
    submit() {
      const { inboxId, ticketInboxId } = this.$route.params;

      axios
        .post(
          `/api/inboxes/${inboxId}/tickets/${ticketInboxId}/comments/post`,
          { content: this.comment }
        )
        .then(() => {
          this.$emit("post");
          this.comment = "";
          this.$refs.commentStaffInput.setMarkdown("");
        });
    },
  },
  computed: {
    user() {
      return this.$store.state.user;
    },
  },
};
</script>
