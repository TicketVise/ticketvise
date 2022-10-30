<template>
  <div
    class="w-full border border-gray-200 rounded pl-3 pr-4 py-3 flex text-sm leading-5 items-center"
  >
    <documentIcon class="w-5 h-5 text-primary group-hover:text-primary-600" />
    <span class="w-full ml-2 flex-1 truncate text-gray-900">
      {{ getFilename(attachment.file)
      }}<span class="text-gray-400">.{{ getExtension(attachment.file) }}</span>
    </span>

    <!-- More menu -->
    <Menu as="div" class="relative inline-block text-left">
      <div>
        <MenuButton
          class="-m-2 p-2 rounded-full flex items-center text-gray-400 hover:text-gray-600"
        >
          <span class="sr-only">Open options</span>
          <EllipsisVerticalIcon class="h-5 w-5" aria-hidden="true" />
        </MenuButton>
      </div>

      <transition
        enter-active-class="transition ease-out duration-100"
        enter-from-class="transform opacity-0 scale-95"
        enter-to-class="transform opacity-100 scale-100"
        leave-active-class="transition ease-in duration-75"
        leave-from-class="transform opacity-100 scale-100"
        leave-to-class="transform opacity-0 scale-95"
      >
        <MenuItems
          class="origin-top-right absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-10"
        >
          <div class="py-1 border-b">
            <MenuItem v-slot="{ active }">
              <a
                :href="attachment.file"
                :download="getFilename(attachment.file)"
                :class="[
                  active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                  'flex px-4 py-2 text-sm',
                ]"
              >
                <DocumentDownloadIcon
                  class="mr-3 h-5 w-5 text-gray-400"
                  aria-hidden="true"
                />
                <span>Download</span>
              </a>
            </MenuItem>
            <MenuItem v-slot="{ active }">
              <a
                target="_blank"
                :href="attachment.file"
                :class="[
                  active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                  'flex px-4 py-2 text-sm',
                ]"
              >
                <EyeIcon
                  class="mr-3 h-5 w-5 text-gray-400"
                  aria-hidden="true"
                />
                <span>View</span>
              </a>
            </MenuItem>
          </div>
          <div v-if="showDelete" class="py-1">
            <MenuItem v-slot="{ active }">
              <button
                @click="remove(attachment)"
                :class="[
                  active ? 'bg-gray-100 text-gray-900' : 'text-gray-700',
                  'flex w-full px-4 py-2 text-sm',
                ]"
              >
                <DocumentRemoveIcon
                  class="mr-3 h-5 w-5 text-gray-400"
                  aria-hidden="true"
                />
                <span>Delete</span>
              </button>
            </MenuItem>
          </div>
        </MenuItems>
      </transition>
    </Menu>
  </div>
</template>

<script>
import axios from "axios";

import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
import { EllipsisVerticalIcon } from "@heroicons/vue/24/solid";

import {
  DocumentIcon,
  DocumentDownloadIcon,
  DocumentRemoveIcon,
  EyeIcon,
} from "@heroicons/vue/24/outline";

export default {
  components: {
    DocumentIcon,
    DocumentDownloadIcon,
    DocumentRemoveIcon,
    EyeIcon,
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    EllipsisVerticalIcon,
  },
  props: {
    attachment: {
      type: Object,
      required: true,
    },
    showDelete: {
      type: Boolean,
      default: true,
    },
  },
  methods: {
    getFilename(url) {
      return url.substring(url.lastIndexOf("/") + 1, url.lastIndexOf("."));
    },
    getExtension(url) {
      return url.substring(url.lastIndexOf(".") + 1);
    },
    remove(attachment) {
      const inboxId = this.$route.params.inboxId;
      const ticketInboxId = this.$route.params.ticketInboxId;
      axios.delete(
        `/api/inboxes/${inboxId}/tickets/${ticketInboxId}/attachments/${attachment.id}`
      );
      this.$emit("remove");
    },
  },
};
</script>
