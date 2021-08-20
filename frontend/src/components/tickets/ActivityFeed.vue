<template>
  <div class="flow-root">
    <ul class="-mb-8">
      <li v-for="(item, itemIdx) in ticket?.activity" :key="item.id">
        <div class="relative pb-8">
          <span v-if="(itemIdx !== ticket.activity.length - 1)" class="absolute top-5 left-5 -ml-px h-full w-0.5 bg-gray-200" aria-hidden="true" />
          <div class="relative flex items-start space-x-3">
            <template v-if="item.type === 'comment'">
              <div class="relative">
                <img class="h-10 w-10 rounded-full bg-gray-400 flex items-center justify-center ring-8 ring-white" :src="item?.imageUrl" alt="" />

                <span class="absolute -bottom-0.5 -right-1 bg-white rounded-tl px-0.5 py-px">
                  <ChatAltIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                </span>
              </div>
              <div class="min-w-0 flex-1">
                <div>
                  <div class="text-sm">
                    <a :href="item?.person?.href" class="font-medium text-gray-900">{{ item?.person?.name }}</a>
                  </div>
                  <p class="mt-0.5 text-sm text-gray-500">Commented {{ item?.date }}</p>
                </div>
                <div class="mt-2 text-sm text-gray-700">
                  <p>
                    {{ item?.comment }}
                  </p>
                </div>
              </div>
            </template>
            <template v-else-if="item.type === 'assignment'" condition="item.type === 'assignment'">
              <div>
                <div class="relative px-1">
                  <div class="h-8 w-8 bg-gray-100 rounded-full ring-8 ring-white flex items-center justify-center">
                    <UserCircleIconSolid class="h-5 w-5 text-gray-500" aria-hidden="true" />
                  </div>
                </div>
              </div>
              <div class="min-w-0 flex-1 py-1.5">
                <div class="text-sm text-gray-500">
                  <a :href="item?.person?.href" class="font-medium text-gray-900">{{ item?.person?.name }}</a>
                  {{ ' ' }}
                  {{ item?.person ? 'assigned' : 'Ticket has been assigned to' }}
                  {{ ' ' }}
                  <a :href="item?.assigned?.href" class="font-medium text-gray-900">{{ item?.assigned?.name }}</a>
                  {{ ' ' }}
                  <span class="whitespace-nowrap">{{ item?.date }}</span>
                </div>
              </div>
            </template>
            <template v-else-if="item.type === 'tags'" condition="item.type === 'tags'">
              <div>
                <div class="relative px-1">
                  <div class="h-8 w-8 bg-gray-100 rounded-full ring-8 ring-white flex items-center justify-center">
                    <TagIcon class="h-5 w-5 text-gray-500" aria-hidden="true" />
                  </div>
                </div>
              </div>
              <div class="min-w-0 flex-1 py-0">
                <div class="text-sm leading-8 text-gray-500">
                  <span class="mr-0.5">
                    <a :href="item?.person?.href" class="font-medium text-gray-900">{{ item?.person?.name }}</a>
                    {{ ' ' }}
                    {{ item?.person ? 'added tags' : 'Ticket got tags' }}
                  </span>
                  {{ ' ' }}
                  <span class="mr-0.5">
                    <span v-for="tag in item.tags" :key="tag.name">
                      <chip :background="tag.color">
                        {{ tag.name }}
                      </chip>
                      {{ ' ' }}
                    </span>
                  </span>
                  <span class="whitespace-nowrap">{{ item.date }}</span>
                </div>
              </div>
            </template>
            <template v-else-if="item.type === 'status'" condition="item.type === 'status'">
              <div>
                <div class="relative px-1">
                  <div class="h-8 w-8 bg-gray-100 rounded-full ring-8 ring-white flex items-center justify-center">
                    <CollectionIcon class="h-5 w-5 text-gray-500" aria-hidden="true" />
                  </div>
                </div>
              </div>
              <div class="min-w-0 flex-1 py-0">
                <div class="text-sm leading-8 text-gray-500">
                  <span class="mr-0.5">
                    <a :href="item?.person?.href" class="font-medium text-gray-900">{{ item?.person?.name }}</a>
                    {{ ' ' }}
                    {{ item?.person ? 'changed the status to' : 'Status changed to' }}
                  </span>
                  {{ ' ' }}
                  <span class="mr-0.5">
                    <chip>{{ statusses[item.status].name }}</chip>
                    {{ ' ' }}
                  </span>
                  <span class="whitespace-nowrap">{{ item.date }}</span>
                </div>
              </div>
            </template>
          </div>
        </div>
      </li>
    </ul>

    <!-- Box to make a new comment. -->
    <div class="mt-6">
      <div class="flex space-x-3">
        <div class="flex-shrink-0">
          <div class="relative">
            <img class="h-10 w-10 rounded-full bg-gray-400 flex items-center justify-center ring-8 ring-white" :src="user.avatar_url" alt="" />

            <span class="absolute -bottom-0.5 -right-1 bg-white rounded-tl px-0.5 py-px">
              <ChatAltIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
            </span>
          </div>
        </div>
        <div class="min-w-0 flex-1">
          <form @submit.prevent="submit">
            <div>
              <label for="comment" class="sr-only">Comment</label>
              <textarea v-model="comment" id="comment" name="comment" rows="3" class="block w-full focus:ring-gray-900 focus:border-gray-900 sm:text-sm border border-gray-300 rounded-md" placeholder="Leave a comment" />
            </div>
            <div class="mt-6 flex items-center justify-end space-x-4">
              <button type="button" class="inline-flex justify-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-900">
                <CheckCircleIcon class="-ml-1 mr-2 h-5 w-5 text-green-500" aria-hidden="true" />
                <span>Close issue</span>
              </button>
              <button type="submit" class="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-900">
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
import axios from 'axios'
import Chip from '@/components/chip/Chip'

import {
  ChatAltIcon,
  CheckCircleIcon,
  CollectionIcon,
  TagIcon,
  UserCircleIcon as UserCircleIconSolid
} from '@heroicons/vue/solid'

const statusses = {
  PNDG: {
    name: 'Pending',
    color: '#e76f51'
  },
  ASGD: {
    name: 'Assigned',
    color: '#e9c46a'
  },
  ANSD: {
    name: 'Awaiting response',
    color: '#2a9d8f'
  },
  CLSD: {
    name: 'Closed',
    color: '#264653'
  }
}

export default {
  components: {
    ChatAltIcon,
    CheckCircleIcon,
    Chip,
    CollectionIcon,
    TagIcon,
    UserCircleIconSolid
  },
  props: {
    ticket: {
      type: Object,
      required: false
    }
  },
  data: () => ({
    comment: ''
  }),
  setup () {
    return { statusses }
  },
  methods: {
    submit () {
      const inboxId = this.$route.params.inboxId
      const ticketInboxId = this.$route.params.ticketInboxId

      axios.post(`/api/inboxes/${inboxId}/tickets/${ticketInboxId}/replies/post`, { content: this.comment })
        .then(() => {
          this.$emit('post')
          this.comment = ''
        })
    }
  },
  computed: {
    user () {
      return this.$store.state.user
    }
  }
}
</script>