<template>
  <div>
    <div>
      <div class="mt-3 sm:mt-5">
        <h3 class="text-lg text-center leading-6 font-medium text-gray-900" id="modal-headline">
          Overview page
        </h3>
        <div class="mt-2">
          <p v-if="!assigned" class="text-sm text-gray-500 text-justify">
            This is the overview page, where you can see all tickets in your inbox. Students will only see their own tickets and tickets that are shared with them. As you can see a new ticket is created and firstly joins the 'Pending' column until it is assigned to someone in your team. Let's see what happens when <button @click="assign" class="text-primary underline">you assign the ticket to yourself</button>.
          </p>

          <p v-if="assigned" class="text-sm text-gray-500 text-justify">
            The ticket has now moved to the next 'Assigned' column. Because this ticket is assigned to you, you will see a orange border around the ticket. In the upper right corner there is a 'My Tickets' button to see only the tickets that are assigned to you.
          </p>
          <p v-if="assigned" class="text-sm text-gray-500 text-justify mt-2">
            When you have <button @click="$store.dispatch('demo_tickets', { inboxId: this.$route.params.inboxId, status: 'awaiting' })" class="text-primary underline">answered the ticket</button> it will move to the 'Awaiting response' column. And if the <button @click="$store.dispatch('demo_tickets', { inboxId: this.$route.params.inboxId, status: 'closed' })" class="text-primary underline">ticket is closed</button>, it will move to the 'Closed' column. This natural flow of tickets is the basis of TicketVise and will help you focus on the tickets that require your attention.
          </p>
          <div v-if="assigned" class="rounded-md bg-blue-50 p-4 mt-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <InformationCircleIcon class="h-5 w-5 text-blue-400" aria-hidden="true" />
              </div>
              <div class="ml-3 flex-1 md:flex md:justify-between">
                <p class="text-sm text-blue-700">
                  You can search for certain keywords or certain labels to show only those tickets.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { InformationCircleIcon } from '@heroicons/vue/solid'

export default {
  name: 'OverviewModal',
  components: {
    InformationCircleIcon
  },
  data: () => ({
    assigned: false
  }),
  methods: {
    assign () {
      this.$store.dispatch('demo_tickets', { inboxId: this.$route.params.inboxId, status: 'assigned' })
      this.assigned = true
    }
  }
}
</script>
