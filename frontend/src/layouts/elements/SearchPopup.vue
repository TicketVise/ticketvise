<template>
  <TransitionRoot :show="show" as="template" @after-leave="rawQuery = ''" appear>
    <Dialog as="div" class="relative z-10" @close="$emit('close')">
      <TransitionChild as="template" enter="ease-out duration-300" enter-from="opacity-0" enter-to="opacity-100" leave="ease-in duration-200" leave-from="opacity-100" leave-to="opacity-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-25 transition-opacity" />
      </TransitionChild>

      <div class="fixed inset-0 z-10 overflow-y-auto p-4 sm:p-6 md:p-20">
        <TransitionChild as="template" enter="ease-out duration-300" enter-from="opacity-0 scale-95" enter-to="opacity-100 scale-100" leave="ease-in duration-200" leave-from="opacity-100 scale-100" leave-to="opacity-0 scale-95">
          <DialogPanel class="mx-auto max-w-xl transform divide-y divide-gray-100 overflow-hidden rounded-xl bg-white shadow-2xl ring-1 ring-black ring-opacity-5 transition-all">
            <Combobox @update:modelValue="onSelect">
              <div class="relative">
                <MagnifyingGlassIcon class="pointer-events-none absolute top-3.5 left-4 h-5 w-5 text-gray-400" aria-hidden="true" />
                <ComboboxInput class="h-12 w-full border-0 bg-transparent pl-11 pr-4 text-gray-800 placeholder-gray-400 focus:ring-0 sm:text-sm" placeholder="Search..." @change="rawQuery = $event.target.value" />
              </div>

              <ComboboxOptions v-if="filteredTickets.length > 0 || filteredUsers.length > 0" static class="max-h-80 scroll-py-10 scroll-pb-2 space-y-4 overflow-y-auto p-4 pb-2">
                <li v-if="filteredTickets.length > 0">
                  <h2 class="text-xs font-semibold text-gray-900">Tickets</h2>
                  <ul class="-mx-4 mt-2 text-sm text-gray-700">
                    <ComboboxOption v-for="ticket in filteredTickets" :key="ticket.id" :value="ticket" as="template" v-slot="{ active }">
                      <li :class="['flex cursor-default select-none items-center px-4 py-2', active && 'bg-indigo-600 text-white']">
                        <FolderIcon :class="['h-6 w-6 flex-none', active ? 'text-white' : 'text-gray-400']" aria-hidden="true" />
                        <span class="ml-3 flex-auto truncate">{{ ticket.name }}</span>
                      </li>
                    </ComboboxOption>
                  </ul>
                </li>
                <li v-if="filteredUsers.length > 0">
                  <h2 class="text-xs font-semibold text-gray-900">Users</h2>
                  <ul class="-mx-4 mt-2 text-sm text-gray-700">
                    <ComboboxOption v-for="user in filteredUsers" :key="user.id" :value="user" as="template" v-slot="{ active }">
                      <li :class="['flex cursor-default select-none items-center px-4 py-2', active && 'bg-indigo-600 text-white']">
                        <img :src="user.imageUrl" alt="" class="h-6 w-6 flex-none rounded-full" />
                        <span class="ml-3 flex-auto truncate">{{ user.name }}</span>
                      </li>
                    </ComboboxOption>
                  </ul>
                </li>
              </ComboboxOptions>

              <div v-if="rawQuery === '?'" class="py-14 px-6 text-center text-sm sm:px-14">
                <LifebuoyIcon class="mx-auto h-6 w-6 text-gray-400" aria-hidden="true" />
                <p class="mt-4 font-semibold text-gray-900">Help with searching</p>
                <p class="mt-2 text-gray-500">Use this tool to quickly search for users and projects across our entire platform. You can also use the search modifiers found in the footer below to limit the results to just users or projects.</p>
              </div>

              <div v-if="query !== '' && rawQuery !== '?' && filteredTickets.length === 0 && filteredUsers.length === 0" class="py-14 px-6 text-center text-sm sm:px-14">
                <ExclamationTriangleIcon class="mx-auto h-6 w-6 text-gray-400" aria-hidden="true" />
                <p class="mt-4 font-semibold text-gray-900">No results found</p>
                <p class="mt-2 text-gray-500">We couldn't find anything with that term. Please try again.</p>
              </div>

              <div class="flex flex-wrap items-center bg-gray-50 py-2.5 px-4 text-xs text-gray-700">
                Type
                <kbd :class="['mx-1 flex h-5 w-5 items-center justify-center rounded border bg-white font-semibold sm:mx-2', rawQuery.startsWith('#') ? 'border-indigo-600 text-indigo-600' : 'border-gray-400 text-gray-900']">#</kbd>
                <span class="sm:hidden">for tickets, and</span>
                <span class="hidden sm:inline">to access tickets, and</span>
                <!-- <kbd :class="['mx-1 flex h-5 w-5 items-center justify-center rounded border bg-white font-semibold sm:mx-2', rawQuery.startsWith('>') ? 'border-indigo-600 text-indigo-600' : 'border-gray-400 text-gray-900']">&gt;</kbd>
                for users, and -->
                <kbd :class="['mx-1 flex h-5 w-5 items-center justify-center rounded border bg-white font-semibold sm:mx-2', rawQuery === '?' ? 'border-indigo-600 text-indigo-600' : 'border-gray-400 text-gray-900']">?</kbd>
                for help.
              </div>
            </Combobox>
          </DialogPanel>
        </TransitionChild>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script>
export default {
  name: 'SearchPopup',
  props: {
    show: {
      type: Boolean,
      required: true,
    }
  }
}
</script>

<script setup>
import { computed, ref } from 'vue'
import { MagnifyingGlassIcon } from '@heroicons/vue/20/solid'
import { ExclamationTriangleIcon, FolderIcon, LifebuoyIcon } from '@heroicons/vue/24/outline'
import {
  Combobox,
  ComboboxInput,
  ComboboxOptions,
  ComboboxOption,
  Dialog,
  DialogPanel,
  TransitionChild,
  TransitionRoot,
} from '@headlessui/vue'

const tickets = [
  { id: 1, name: 'When is the next SWEBOK panel?', category: 'Tickets', url: '/inboxes/1/tickets/3' },
  { id: 2, name: 'Discord does not work on my laptop!', category: 'Tickets', url: '/inboxes/1/tickets/7' },
  { id: 3, name: 'What should be the content of the demo?', category: 'Tickets', url: '/inboxes/1/tickets/6' },
  { id: 4, name: 'Should I mention the testing coverage in my report?', category: 'Tickets', url: '/inboxes/1/tickets/18' },
  { id: 5, name: 'E-Journal does not work', category: 'Tickets', url: '/inboxes/1/tickets/4' },
  { id: 6, name: 'The SWEBOK panel dates do not specify the group', category: 'Tickets', url: '/inboxes/1/tickets/20' },
  { id: 7, name: 'Is there a minimum grade for my individual report?', category: 'Tickets', url: '/inboxes/1/tickets/12' },
  // More projects...
]

const users = [
  {
    id: 1,
    name: 'Christa ',
    url: '#',
    imageUrl:
      'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
  },
  {
    id: 2,
    name: 'Edgar W. Dijkstra ',
    url: '#',
    imageUrl:
      'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
  },
  // More users...
]

const rawQuery = ref('')
const query = computed(() => rawQuery.value.toLowerCase().replace(/^[#>]/, ''))
const filteredTickets = computed(() =>
  rawQuery.value === '#'
    ? tickets
    : query.value === '' || rawQuery.value.startsWith('>')
    ? []
    : tickets.filter((ticket) => ticket.name.toLowerCase().includes(query.value))
)
const filteredUsers = computed(() =>
  rawQuery.value === '>'
    ? users
    : query.value === '' || rawQuery.value.startsWith('#')
    ? []
    : users.filter((user) => user.name.toLowerCase().includes(query.value))
)

function onSelect(item) {
  window.location = item.url
}
</script>
