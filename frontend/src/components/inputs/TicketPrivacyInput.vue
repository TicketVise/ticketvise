<!-- This example requires Tailwind CSS v2.0+ -->
<template>
  <RadioGroup v-model="selectedMailingLists">
    <RadioGroupLabel class="text-base font-medium text-gray-900">
      Select a privacy setting
    </RadioGroupLabel>

    <div class="mt-4 grid grid-cols-1 gap-y-6 sm:grid-cols-3 sm:gap-x-4">
      <RadioGroupOption as="template" v-for="mailingList in mailingLists" :key="mailingList.id" :value="mailingList" v-slot="{ checked, active }">
        <div :class="[checked ? 'border-transparent' : 'border-gray-300', active ? 'ring-2 ring-primary-500' : '', 'relative bg-white border rounded-lg p-4 flex cursor-pointer focus:outline-none']">
          <div class="flex-1 flex">
            <div class="flex flex-col">
              <RadioGroupLabel as="span" class="block text-sm font-medium text-gray-900">
                {{ mailingList.title }}
              </RadioGroupLabel>
              <RadioGroupDescription as="span" class="mt-1 flex items-center text-sm text-gray-500">
                {{ mailingList.description }}
              </RadioGroupDescription>
              <!-- <RadioGroupDescription as="span" class="mt-6 text-sm font-medium text-gray-900">
                {{ mailingList.users }}
              </RadioGroupDescription> -->
            </div>
          </div>
          <CheckCircleIcon :class="[!checked ? 'invisible' : '', 'h-5 w-5 text-primary-600']" aria-hidden="true" />
          <div :class="[active ? 'border' : 'border-2', checked ? 'border-primary-500' : 'border-transparent', 'absolute -inset-px rounded-lg pointer-events-none']" aria-hidden="true" />
        </div>
      </RadioGroupOption>
    </div>
  </RadioGroup>
</template>

<script>
import { ref } from 'vue'
import { RadioGroup, RadioGroupDescription, RadioGroupLabel, RadioGroupOption } from '@headlessui/vue'
import { CheckCircleIcon } from '@heroicons/vue/solid'

const mailingLists = [
  { id: 1, title: 'Private', description: 'Only you and the staff team will be able to access this ticket', users: '621 users' },
  { id: 2, title: 'Public', description: 'This ticket will be available to anyone in this inbox', users: '1200 users' },
  { id: 3, title: 'Anonymous Public', description: 'This ticket will be available to anyone in this inbox and we won\'t show you as the author. You are responsible to exclude private information in this ticket\'s content!', users: '2740 users' }
]

export default {
  components: {
    RadioGroup,
    RadioGroupDescription,
    RadioGroupLabel,
    RadioGroupOption,
    CheckCircleIcon
  },
  setup () {
    const selectedMailingLists = ref(mailingLists[0])

    return {
      mailingLists,
      selectedMailingLists
    }
  }
}
</script>
