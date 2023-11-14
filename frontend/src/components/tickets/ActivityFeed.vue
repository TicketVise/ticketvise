<template>
  <div class="flow-root">
    <div class="text-center mb-8" v-if="ticket?.activity.length === 0">
      <img
        alt="Nothing here"
        class="w-1/2 md:w-1/4 mx-auto mb-8"
        :src="relax"
      />
      <span class="text-sm leading-8 text-gray-500"
        >There are no messages here yet...</span
      >
    </div>
    <ul class="relative pb-4">
      <div class="flex w-full justify-end">
        <button @click="showActivity = !showActivity" v-if="isStaff && ticket?.replies.length != 0" class="text-gray-400 flex items-center space-x-2 hover:text-gray-600 cursor-pointer z-10 mb-4">
          <BoltIcon v-if="!showActivity" class="h-4 w-4" aria-hidden="true" />
          <BoltSlashIcon v-else class="h-4 w-4" aria-hidden="true" />
          <span class="text-sm">{{ showActivity ? 'hide activity' : 'show activity' }}</span>
        </button>
      </div>
      <li v-for="(item, itemIdx) in ticket?.activity" :key="item">
        <div v-if="item.type == 'comment' || (['assignment', 'tags', 'status', 'attachment', 'group'].includes(item.type) && (showActivity || ticket?.replies.length == 0))" class="relative pb-2">
          <span
            v-if="itemIdx !== ticket.activity.length - 1"
            class="absolute top-5 left-5 -ml-px h-full w-0.5 bg-gray-200"
            aria-hidden="true"
          />
          <div class="relative flex items-start space-x-3">
            <template v-if="item.type === 'comment'">
              <div class="relative">
                <img
                  class="h-10 w-10 rounded-full bg-gray-400 flex items-center justify-center ring-8 ring-white"
                  :src="item?.imageUrl"
                  alt=""
                />

                <span class="absolute -bottom-0.5 -right-1 bg-white rounded-tl px-0.5 py-px">
                  <ChatBubbleLeftEllipsisIcon class="h-5 w-5 text-gray-400" aria-hidden="true"/>
                </span>
              </div>
              <div class="min-w-0 flex-1">
                <div class="flex justify-between">
                  <div>
                    <div class="text-sm">
                      <span class="font-medium text-gray-900">{{
                        item?.person?.name
                      }}</span>
                    </div>
                    <p class="mt-0.5 text-sm text-gray-500">
                      Commented {{ item?.date }}
                    </p>
                  </div>
                  <div class="flex items-center space-x-4">
                    <div v-if="ticket.is_public && isMostHelpful(item.id)" class="border border-primary-400 rounded-md px-1.5 py-0.5 inline-flex items-center text-sm text-primary font-medium">
                      <ThumbUpSolidIcon class="h-4 w-4 text-primary-400 mr-1" />
                      <span class="hidden sm:flex">Most Helpful</span>
                    </div>
                    <Menu v-if="isStaff" as="div" class="relative inline-block text-left">
                      <div>
                        <MenuButton class="flex items-center rounded-full text-primary hover:text-primary-600 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 focus:ring-offset-primary-100">
                          <span class="sr-only">Open options</span>
                          <EllipsisVerticalIcon class="h-5 w-5" aria-hidden="true" />
                        </MenuButton>
                      </div>

                      <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
                        <MenuItems class="absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                          <div class="py-1">
                            <MenuItem v-slot="{ active }">
                              <a @click="splitTicketPrompt = item; splitTicketPrompt.labels = [...ticket.labels]; splitTicketPrompt.assignYourself = true; splitTicketPromptShow = true" :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'block px-4 py-2 text-sm cursor-pointer']">Split into a new ticket</a>
                            </MenuItem>
                          </div>
                        </MenuItems>
                      </transition>
                    </Menu>
                  </div>
                </div>
                <div class="mt-2 text-sm text-gray-700">
                  <TicketInputViewer v-if="item" :content="item.comment" />
                </div>
                <div
                  v-if="item?.person.username != user.username"
                  class="mt-2 text-sm flex space-x-2 mb-4"
                >
                  <button
                    @click="
                      item?.helpful === 'helpful'
                        ? clearHelpful(item.id)
                        : helpful(item.id)
                    "
                    class="inline-flex items-center px-3 py-0.5 rounded-full text-sm border text-primary"
                    :class="item?.helpful === 'helpful' ? 'font-medium' : ''"
                  >
                    <ThumbUpSolidIcon
                      v-if="item?.helpful === 'helpful'"
                      class="h-4 w-4 text-primary mr-1"
                    />
                    <ThumbUpOutlineIcon
                      v-else
                      class="h-4 w-4 text-primary mr-1"
                    />
                    Helpful
                  </button>
                  <button
                    @click="
                      item?.helpful === 'notHelpful'
                        ? clearHelpful(item.id)
                        : notHelpful(item.id)
                    "
                    class="inline-flex items-center px-3 py-0.5 rounded-full text-sm border text-primary"
                    :class="item?.helpful === 'notHelpful' ? 'font-medium' : ''"
                  >
                    <ThumbDownSolidIcon
                      v-if="item?.helpful === 'notHelpful'"
                      class="h-4 w-4 text-primary mr-1"
                    />
                    <ThumbDownOutlineIcon
                      v-else
                      class="h-4 w-4 text-primary mr-1"
                    />
                    Not Helpful
                  </button>
                </div>
              </div>
            </template>
            <template
              v-else-if="item.type === 'assignment' && (showActivity || ticket?.replies.length == 0)"
            >
              <div>
                <div class="relative px-1">
                  <div
                    class="h-8 w-8 bg-gray-100 rounded-full ring-8 ring-white flex items-center justify-center"
                  >
                    <UserCircleIconSolid
                      class="h-5 w-5 text-gray-500"
                      aria-hidden="true"
                    />
                  </div>
                </div>
              </div>
              <div class="min-w-0 flex-1 py-1.5">
                <div class="text-sm text-gray-500">
                  <span class="font-medium text-gray-900">{{
                    item?.person?.name
                  }}</span>
                  {{ " " }}
                  {{
                    item?.person ? "assigned" : "Ticket has been assigned to"
                  }}
                  {{ " " }}
                  <span class="font-medium text-gray-900">{{
                    item?.assigned?.name
                  }}</span>
                  {{ " " }}
                  <span class="whitespace-nowrap">{{ item?.date }}</span>
                </div>
              </div>
            </template>
            <template
              v-else-if="item.type === 'tags' && (showActivity || ticket?.replies.length == 0)"
            >
              <div>
                <div class="relative px-1">
                  <div
                    class="h-8 w-8 bg-gray-100 rounded-full ring-8 ring-white flex items-center justify-center"
                  >
                    <TagIcon class="h-5 w-5 text-gray-500" aria-hidden="true" />
                  </div>
                </div>
              </div>
              <div class="min-w-0 flex-1 py-0">
                <div class="text-sm leading-8 text-gray-500">
                  <span class="mr-0.5">
                    <span class="font-medium text-gray-900">{{
                      item?.person?.name
                    }}</span>
                    {{ " " }}
                    {{
                      item?.person
                        ? item?.is_added
                          ? "added labels"
                          : "removed labels"
                        : "Ticket got labels"
                    }}
                  </span>
                  {{ " " }}
                  <span class="mr-0.5">
                    <span v-for="tag in item.tags" :key="tag.name">
                      <chip :background="tag.color">
                        {{ tag.name }}
                      </chip>
                      {{ " " }}
                    </span>
                  </span>
                  <span class="whitespace-nowrap">{{ item.date }}</span>
                </div>
              </div>
            </template>
            <template
              v-else-if="item.type === 'status' && (showActivity || ticket?.replies.length == 0)"
            >
              <div>
                <div class="relative px-1">
                  <div class="h-8 w-8 bg-gray-100 rounded-full ring-8 ring-white flex items-center justify-center">
                    <RectangleStackIcon class="h-5 w-5 text-gray-500" aria-hidden="true"/>
                  </div>
                </div>
              </div>
              <div class="min-w-0 flex-1 py-0">
                <div class="text-sm leading-8 text-gray-500">
                  <span class="mr-0.5">
                    <span class="font-medium text-gray-900">{{
                      item?.person?.name
                    }}</span>
                    {{ " " }}
                    {{
                      item?.person
                        ? "changed the status to"
                        : "Status changed to"
                    }}
                  </span>
                  {{ " " }}
                  <span class="mr-0.5">
                    <chip>{{ statusses[item.status].name }}</chip>
                    {{ " " }}
                  </span>
                  <span class="whitespace-nowrap">{{ item.date }}</span>
                </div>
              </div>
            </template>
            <template
              v-else-if="item.type === 'attachment' && (showActivity || ticket?.replies.length == 0)"
            >
              <div>
                <div class="relative px-1">
                  <div
                    class="h-8 w-8 bg-gray-100 rounded-full ring-8 ring-white flex items-center justify-center"
                  >
                    <DocumentIcon
                      class="h-5 w-5 text-gray-500"
                      aria-hidden="true"
                    />
                  </div>
                </div>
              </div>
              <div class="min-w-0 flex-1 py-0">
                <div class="text-sm leading-8 text-gray-500">
                  <span class="mr-0.5">
                    <span class="font-medium text-gray-900">{{
                      item?.person?.name
                    }}</span>
                    {{ " " }}
                    uploaded the following file{{
                      item?.attachment?.length > 1 ? "s" : ""
                    }}
                  </span>
                  {{ " " }}
                  <span
                    class="mr-0.5"
                    v-for="attachment in item.attachment"
                    :key="attachment.name"
                  >
                    <a :href="attachment.href" target="_blank">
                      <chip class="max-w-xs">
                        <span class="truncate leading-4">{{
                          attachment.name + "." + attachment.extension
                        }}</span>
                      </chip>
                    </a>
                    {{ " " }}
                  </span>
                  <span class="whitespace-nowrap">{{ item.date }}</span>
                </div>

                <VueEasyLightbox
                  scrollDisabled
                  moveDisabled
                  :imgs="filterImages(item.attachment).map((a) => a.href)"
                  :visible="item.visible"
                  :index="item.index"
                  @hide="item.visible = false"
                />
                <ul
                  role="list"
                  class="mt-2 grid grid-cols-2 gap-x-4 gap-y-8 sm:grid-cols-3 sm:gap-x-6 md:grid-cols-4 lg:grid-cols-3 xl:grid-cols-4 xl:gap-x-8"
                >
                  <li
                    v-for="(attachment, index) in filterImages(item.attachment)"
                    :key="index"
                  >
                    <button
                      @click="
                        item.index = index;
                        item.visible = true;
                      "
                      class="group block w-full aspect-w-10 aspect-h-7 rounded-lg bg-gray-100 overflow-hidden"
                    >
                      <img
                        :src="attachment.href"
                        class="object-cover pointer-events-none"
                        loading="lazy"
                      />
                      <button
                        type="button"
                        class="absolute inset-0 focus:outline-none"
                      >
                        <span class="sr-only"
                          >View details for {{ attachment.name }}</span
                        >
                      </button>
                    </button>
                    <p
                      class="mt-2 block text-sm font-medium text-gray-900 truncate pointer-events-none"
                    >
                      {{ attachment.name + "." + attachment.extension }}
                    </p>
                    <p
                      class="block text-sm font-medium text-gray-500 pointer-events-none"
                    >
                      {{ readableBytes(attachment.size) }}
                    </p>
                  </li>
                </ul>
              </div>
            </template>
            <template
              v-else-if="item.type === 'group' && (showActivity || ticket?.replies.length == 0)"
            >
              <div>
                <div class="relative px-1">
                  <div
                    class="h-8 w-8 bg-gray-100 rounded-full ring-8 ring-white flex items-center justify-center"
                  >
                    <RectangleStackIcon
                      class="h-5 w-5 text-gray-500"
                      aria-hidden="true"
                    />
                  </div>
                </div>
              </div>
              <div class="min-w-0 flex-1 py-0">
                <div class="text-sm leading-8 text-gray-500">
                  <button
                    @click="$emit('unfold', item)"
                    class="font-medium hover:underline"
                  >
                    View {{ item.activities.length }} grouped changes
                  </button>
                </div>
              </div>
            </template>
          </div>
        </div>
      </li>
    </ul>

    <!-- Box to make a new comment. -->
    <div>
      <div class="flex space-x-3">
        <div class="flex-shrink-0">
          <div class="relative">
            <img
              class="h-10 w-10 rounded-full bg-gray-400 flex items-center justify-center ring-8 ring-white"
              :src="user.avatar_url"
              alt=""
            />

            <span class="absolute -bottom-0.5 -right-1 bg-white rounded-tl px-0.5 py-px">
              <ChatBubbleLeftEllipsisIcon class="h-5 w-5 text-gray-400" aria-hidden="true"/>
            </span>
          </div>
        </div>
        <div class="min-w-0 flex-1">
          <form @submit.prevent="submit">
            <div>
              <label for="comment" class="sr-only">Comment</label>
              <div class="relative">
                <TicketInput v-model="comment" ref="commentInput" />
                <div
                  v-if="errors.content"
                  class="absolute inset-y-0 right-0 top-14 pr-3 flex pointer-events-none"
                >
                  <ExclamationCircleIcon
                    class="h-5 w-5 text-red-500"
                    aria-hidden="true"
                  />
                </div>
              </div>
              <p
                v-if="errors.content"
                class="mt-2 text-sm text-red-600"
                id="email-error"
              >
                {{ errors.content[0] }}
              </p>
            </div>
            <div class="mt-6 flex items-center justify-end space-x-4">
              <button
                type="button"
                @click="closeTicket"
                v-if="ticket.status !== 'CLSD' && permissions"
                class="inline-flex justify-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
              >
                <CheckCircleIcon
                  class="-ml-1 mr-2 h-5 w-5 text-green-500"
                  aria-hidden="true"
                />
                Close ticket
              </button>
              <button
                type="submit"
                class="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
              >
                <span v-if="ticket.status !== 'CLSD'">Comment</span>
                <span v-else>Comment and reopen ticket</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <TransitionRoot as="template" :show="splitTicketPromptShow">
      <Dialog as="div" class="relative z-10" @close="splitTicketPromptShow = false">
        <TransitionChild as="template" enter="ease-out duration-300" enter-from="opacity-0" enter-to="opacity-100" leave="ease-in duration-200" leave-from="opacity-100" leave-to="opacity-0">
          <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
        </TransitionChild>
  
        <div class="fixed inset-0 z-10 overflow-y-auto">
          <div class="flex min-h-full justify-center p-4 text-center items-center sm:p-0">
            <TransitionChild as="template" enter="ease-out duration-300" enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95" enter-to="opacity-100 translate-y-0 sm:scale-100" leave="ease-in duration-200" leave-from="opacity-100 translate-y-0 sm:scale-100" leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95">
              <DialogPanel class="relative transform overflow-visible rounded-lg bg-white px-4 pt-5 pb-4 text-left shadow-xl transition-all sm:my-8 w-full max-w-lg p-6 z-40">
                <div class="absolute top-0 right-0 hidden pt-4 pr-4 sm:block">
                  <button type="button" class="rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2" @click="splitTicketPromptShow = false">
                    <span class="sr-only">Close</span>
                    <XMarkIcon class="h-6 w-6" aria-hidden="true" />
                  </button>
                </div>
                <div class="mt-0 text-left">
                  <DialogTitle as="h2" class="text-lg font-semibold leading-6 text-gray-900">Split ticket</DialogTitle>
                  <p class="text-sm text-gray-600">If this comment is more a new questions on it's own, then you can split it into a new separate ticket.</p>
                  <div class="mt-2">
                    <label for="ticketTitle" class="block text-sm font-medium text-gray-700 sm:mt-px sm:pt-2">Title</label>
                    <div class="mt-1 sm:col-span-2 sm:mt-0">
                      <input v-model="splitTicketPrompt.title" type="text" name="ticketTitle" id="ticketTitle" autocomplete="given-name" class="block w-full rounded-md border-gray-300 focus:border-primary-500 focus:ring-primary-500 sm:text-sm" />
                      <p class="mt-1 text-sm text-gray-500">Create a memorable title</p>
                    </div>
                  </div>
                  <div class="mt-2">
                    <label class="block text-sm font-medium text-gray-700 sm:mt-px sm:pt-2">Content</label>
                    <div class="mt-1 sm:col-span-2 sm:mt-0 bg-gray-100 px-2 py-0.5 rounded-md">
                      <TicketInputViewer v-if="splitTicketPrompt.comment" :content="splitTicketPrompt.comment" />
                    </div>
                  </div>
                  <div class="mt-2">
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Labels
                    </label>
                    <LabelDropdown :selected="splitTicketPrompt.labels" :values="inbox?.labels || []" v-model="splitTicketPrompt.labels" />
                  </div>
                  <ul class="mt-2 divide-y divide-gray-200">
                    <SwitchGroup as="li" class="py-4 flex items-center justify-between space-x-2">
                      <div class="flex flex-col">
                        <SwitchLabel as="p" class="text-sm font-medium text-gray-900" passive>
                          Assignee yourself to new ticket
                        </SwitchLabel>
                        <SwitchDescription class="text-sm text-gray-500">
                          Instead of letting the system assign a staff member
                        </SwitchDescription>
                      </div>
                      <Switch v-model="splitTicketPrompt.assignYourself" :class="[splitTicketPrompt.assignYourself ? 'bg-primary' : 'bg-gray-200', 'ml-4 relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary']">
                        <span aria-hidden="true" :class="[splitTicketPrompt.assignYourself ? 'translate-x-5' : 'translate-x-0', 'inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']" />
                      </Switch>
                    </SwitchGroup>
                    <SwitchGroup as="li" class="py-4 flex items-center justify-between space-x-2">
                      <div class="flex flex-col">
                        <SwitchLabel as="p" class="text-sm font-medium text-gray-900" passive>
                          Create ticket as original user
                        </SwitchLabel>
                        <SwitchDescription class="text-sm text-gray-500">
                          Instead of the user of this comment
                        </SwitchDescription>
                      </div>
                      <Switch v-model="splitTicketPrompt.originalUser" :class="[splitTicketPrompt.originalUser ? 'bg-primary' : 'bg-gray-200', 'ml-4 relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary']">
                        <span aria-hidden="true" :class="[splitTicketPrompt.originalUser ? 'translate-x-5' : 'translate-x-0', 'inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200']" />
                      </Switch>
                    </SwitchGroup>
                  </ul>
                </div>
                <div class="mt-5 sm:mt-4 sm:flex sm:flex-row-reverse">
                  <button type="button" class="inline-flex w-full justify-center rounded-md border border-transparent bg-primary-600 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 sm:ml-3 sm:w-auto sm:text-sm" @click="splitTicket(splitTicketPrompt)">Split ticket</button>
                  <button type="button" class="mt-3 inline-flex w-full justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-base font-medium text-gray-700 shadow-sm hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 sm:mt-0 sm:w-auto sm:text-sm" @click="splitTicketPromptShow = false">Cancel</button>
                </div>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>

<script>
import axios from "axios";
import VueEasyLightbox from "vue-easy-lightbox";

import Chip from '@/components/chip/Chip.vue'
import TicketInput from '@/components/inputs/TicketInput.vue'
import TicketInputViewer from '@/components/inputs/TicketInputViewer.vue'
import LabelDropdown from '@/components/dropdown/LabelDropdown.vue'

import relax from '@/assets/img/svg/relax.svg'

import { Menu, MenuButton, MenuItem, MenuItems, Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot, SwitchGroup, SwitchLabel, SwitchDescription, Switch } from '@headlessui/vue'
import { EllipsisVerticalIcon } from '@heroicons/vue/20/solid'
import {
  ChatBubbleLeftEllipsisIcon,
  CheckCircleIcon,
  RectangleStackIcon,
  DocumentIcon,
  TagIcon,
  UserCircleIcon as UserCircleIconSolid,
  ExclamationCircleIcon,
  HandThumbUpIcon as ThumbUpSolidIcon,
  HandThumbDownIcon as ThumbDownSolidIcon
} from '@heroicons/vue/24/solid'
import {
  HandThumbUpIcon as ThumbUpOutlineIcon,
  HandThumbDownIcon as ThumbDownOutlineIcon,
  XMarkIcon,
  BoltIcon,
  BoltSlashIcon
} from '@heroicons/vue/24/outline'

const statusses = {
  PNDG: {
    name: "Pending",
    color: "#e76f51",
  },
  ASGD: {
    name: "Assigned",
    color: "#e9c46a",
  },
  ANSD: {
    name: "Awaiting response",
    color: "#2a9d8f",
  },
  CLSD: {
    name: "Closed",
    color: "#264653",
  },
};

export default {
  components: {
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    Dialog,
    DialogPanel,
    DialogTitle,
    TransitionChild,
    TransitionRoot,
    EllipsisVerticalIcon,
    ChatBubbleLeftEllipsisIcon,
    CheckCircleIcon,
    Chip,
    LabelDropdown,
    RectangleStackIcon,
    DocumentIcon,
    TagIcon,
    UserCircleIconSolid,
    ExclamationCircleIcon,
    TicketInput,
    TicketInputViewer,
    VueEasyLightbox,
    ThumbUpSolidIcon,
    ThumbDownSolidIcon,
    ThumbUpOutlineIcon,
    ThumbDownOutlineIcon,
    SwitchGroup,
    SwitchLabel,
    SwitchDescription,
    Switch,
    XMarkIcon,
    BoltIcon,
    BoltSlashIcon
},
  props: {
    ticket: {
      type: Object,
      required: true,
    },
    permissions: {
      type: Boolean,
      required: false,
      default: false
    },
    staff: {
      type: Boolean,
      required: false,
      default: false
    }
  },
  data: () => ({
    relax,
    inbox: {
      labels: []
    },
    comment: '',
    errors: [],
    splitTicketPromptShow: false,
    splitTicketPrompt: {
      assignYourself: true,
      originalUser: false
    },
    role: null,
    showActivity: false
  }),
  setup() {
    return { statusses };
  },
  mounted() {
    axios.get(`/api/me/inboxes/${this.$route.params.inboxId}`).then((response) => {
      this.role = response.data.role;
    })
    
    axios.get(`/api/inboxes/${this.$route.params.inboxId}/labels/all`)
    .then((response) => {
      this.inbox.labels = response.data
    })
  },
  methods: {
    submit() {
      const inboxId = this.$route.params.inboxId;
      const ticketInboxId = this.$route.params.ticketInboxId;

      axios
        .post(`/api/inboxes/${inboxId}/tickets/${ticketInboxId}/replies/post`, {
          content: this.comment,
        })
        .then(() => {
          this.$emit("post");
          this.comment = "";
          this.$refs.commentInput.setMarkdown("");
          this.errors = [];
        })
        .catch((error) => {
          this.errors = error.response.data;
        });
    },
    closeTicket() {
      const inboxId = this.$route.params.inboxId;
      const ticketInboxId = this.$route.params.ticketInboxId;

      axios
        .patch(`/api/inboxes/${inboxId}/tickets/${ticketInboxId}/status/close`)
        .then(() => {
          this.$emit("post");
        });
    },
    readableBytes(bytes) {
      const sizes = ["Bytes", "KB", "MB", "GB", "TB"];
      if (bytes === 0) return "0 Byte";
      const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
      return Math.round(bytes / Math.pow(1024, i), 2) + " " + sizes[i];
    },
    filterImages(files) {
      return files.filter((file) =>
        ["jpg", "png"].includes(file.extension.toLowerCase())
      );
    },
    helpful(id) {
      this.$emit("helpful", "helpful", id);
    },
    notHelpful(id) {
      this.$emit("helpful", "notHelpful", id);
    },
    clearHelpful(id) {
      this.$emit("helpful", undefined, id);
    },
    helpfulScore(helpful) {
      if (!helpful) return 0;
      return helpful.reduce(
        (sum, helpful) => sum + (helpful.is_helpful ? 1 : -1),
        0
      );
    },
    isMostHelpful(id) {
      if (!this.ticket.is_public) return false;
      const replies = this.ticket.replies;
      const mostHelpfulReply = replies.reduce((mostHelpful, reply) => {
        if (!mostHelpful) return reply;

        if (
          this.helpfulScore(reply.helpful) >
          this.helpfulScore(mostHelpful.helpful)
        ) {
          return reply;
        }

        return mostHelpful;
      }, undefined);

      return mostHelpfulReply.helpful.length == 0 || this.helpfulScore(mostHelpfulReply.helpful) <= 0 ? false : mostHelpfulReply.id === id
    },
    splitTicket (item) {
      const { inboxId, ticketInboxId } = this.$route.params

      axios.delete(`/api/inboxes/${ inboxId }/tickets/${ ticketInboxId }/comments/${item.id}/split`, {
        data: {
          title: item.title,
          author: this.splitTicketPrompt.originalUser ? this.ticket.author : item.person,
          content: item.comment,
          labels: item.labels,
          assignee: this.splitTicketPrompt.assignYourself ? this.user : null
        }
      }).then(async (response) => {
        await this.$router.push("/inboxes/" + inboxId + "/tickets/" + response.data.ticket_id)
        this.splitTicketPromptShow = false
        document.location.reload()
      })
    }
  },
  computed: {
    user() {
      return this.$store.state.user;
    },
    isStaff() {
      return (
        (this.role && (this.role === "AGENT" || this.role === "MANAGER")) ||
        (this.user && this.user.is_superuser)
      );
    }
  },
};
</script>
