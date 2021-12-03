<template>
  <div>
    <div>
      <div class="mt-3 sm:mt-5">
        <h3 class="text-lg text-center leading-6 font-medium text-gray-900" id="modal-headline">
          Automation
        </h3>
        <div class="mt-2">
          <p class="text-sm text-gray-500 text-justify">
            We want to assist you with incoming questions as much as possible. Therefore you can automate the assignment of a ticket to a teacher or assistant. Tickets are answered quicker this way. Click the box below to select the algorithm you want to use to assign tickets.
          </p>
          <div class="rounded-md bg-blue-50 p-4 mt-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <InformationCircleIcon class="h-5 w-5 text-blue-400" aria-hidden="true" />
              </div>
              <div class="ml-3 flex-1 md:flex md:justify-between">
                <p class="text-sm text-blue-700">
                  Check out our <a href="https://ticketvise.com/algorithms/" target="_blank" rel="noopener noreferrer" class="underline">Algorithms guide</a> to understand what the different algorithms do.
                </p>
              </div>
            </div>
          </div>

          <AutomationDefault class="my-4" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { InformationCircleIcon } from '@heroicons/vue/solid'
import AutomationDefault from '@/components/automation/AutomationDefault'

export default {
  name: 'SchedulingModal',
  components: {
    AutomationDefault,
    InformationCircleIcon
  }
}
</script>
