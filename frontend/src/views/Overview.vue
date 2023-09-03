<template>
  <div v-if="false && role == 'MANAGER'">
    <div class="overflow-y-auto p-4">
      <div class="mx-auto flex max-w-3xl flex-col space-y-3">
        <!-- <h2 class="text-xl font-bold leading-6 text-gray-700">Overview</h2> -->

        <div class="grid grid-cols-2 gap-2">
          <div class="overflow-hidden rounded-lg border bg-white">
            <div class="p-2 px-4">
              <div class="flex items-center">
                <div class="hidden flex-shrink-0 sm:flex">
                  <StarIcon class="h-6 w-6 text-gray-400" />
                </div>
                <div class="w-0 flex-1 sm:ml-5">
                  <dl>
                    <dt class="truncate text-sm font-medium text-gray-700">Helpfulness</dt>
                    <dd class="flex items-center justify-between">
                      <div class="text-xl font-medium text-primary">
                        {{ statsData.staff.filter(s => s.amount_of_helpful_comments > 0).reduce(s => s.helpfulness) / statsData.staff.filter(s => s.amount_of_helpful_comments > 0).length }}%
                      </div>

                      <!-- <div :class="['increase' === 'increase' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800', 'inline-flex items-baseline rounded-full px-2.5 py-0.5 text-sm font-medium md:mt-2 lg:mt-0']">
                        <ArrowSmallUpIcon v-if="'up' === 'up'" class="-ml-1 mr-0.5 h-5 w-5 flex-shrink-0 self-center" :class="['increase' === 'increase' ? 'text-green-500' : 'text-red-500']" aria-hidden="true" />
                        <ArrowSmallDownIcon v-else class="-ml-1 mr-0.5 h-5 w-5 flex-shrink-0 self-center" :class="['increase' === 'increase' ? 'text-green-500' : 'text-red-500']" aria-hidden="true" />
                        <span class="sr-only"> {{ 'increase' === 'increase' ? 'Increased' : 'Decreased' }} by </span>
                        33%
                      </div> -->
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="overflow-hidden rounded-lg border bg-white">
            <div class="p-2 px-4">
              <div class="flex items-center">
                <div class="hidden flex-shrink-0 sm:flex">
                  <ClockIcon class="h-6 w-6 text-gray-400" />
                </div>
                <div class="w-0 flex-1 sm:ml-5">
                  <dl>
                    <dt class="truncate text-sm font-medium text-gray-700">Average response time</dt>
                    <dd class="flex items-center justify-between">
                      <div class="text-xl font-medium text-primary">
                        {{ statsData.avg_response_time }}h
                        <!-- <span class="ml-1 hidden text-sm font-medium text-gray-500 lg:inline"> from 6.2h last week </span> -->
                      </div>

                      <!-- <div :class="['decrease' === 'increase' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800', 'inline-flex items-baseline px-2.5 py-0.5 rounded-full text-sm font-medium md:mt-2 lg:mt-0']">
                        <ArrowSmallUpIcon v-if="'up' === 'up'" class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5" :class="['decrease' === 'increase' ? 'text-green-500' : 'text-red-500']" aria-hidden="true" />
                        <ArrowSmallDownIcon v-else class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5" :class="['increase' === 'increase' ? 'text-green-500' : 'text-red-500']" aria-hidden="true" />
                        <span class="sr-only"> {{ 'increase' === 'increase' ? 'Increased' : 'Decreased' }} by </span>
                        27%
                      </div> -->
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div v-if="ticketsFlattened?.length == 0" class="rounded-md bg-blue-50 p-4 col-span-2">
            <div class="flex">
              <div class="flex-shrink-0">
                <InformationCircleIcon class="h-5 w-5 text-blue-400" aria-hidden="true" />
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-blue-700">No questions yet</h3>
                <div class="mt-2 text-sm text-blue-700">
                  <p>The information is limited right now. This is because there are no tickets yet from students. If you need help setting up the inbox, <strong>click here</strong>.</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <h2 class="pt-4 text-lg font-semibold leading-4 text-gray-700">Updates</h2>

        <div v-if="onboarding.active" class="flex rounded-lg border border-primary px-4 py-3">
          <div class="flex flex-col text-gray-800">
            <h2 class="text-xl font-bold text-primary">Hi There! 👋</h2>
            <p class="mt-1 text-justify text-sm">This is the <strong>overview page</strong>. Here you will find the necessary information relevant for you. We will show you important insights about the inbox and show you the tickets that are relevant for you. Like the example ticket you see below!</p>
            <div class="mt-2 flex justify-end text-sm">
              <button @click="nextStep()">
                <span class="font-medium uppercase text-primary">Got it!</span>
              </button>
            </div>
          </div>
        </div>

        <div v-else-if="updates.length == 0" class="flex rounded-lg border p-2">
          <img :src="awesome" class="w-1/3 md:w-1/5" />
          <div class="flex flex-col px-4">
            <h2 class="text-xl font-bold text-primary">All good</h2>
            <p class="text-sm">Right now there are no updates that require your attention</p>
          </div>
        </div>

        <div v-else>
          <div class="rounded-md bg-yellow-50 p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <ExclamationTriangleIcon class="h-5 w-5 text-yellow-400" aria-hidden="true" />
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-yellow-800">Attention needed</h3>
                <div class="mt-2 text-sm text-yellow-700">
                  <p>There are suddenly a lot of tickets about: <strong>Assignment 2</strong></p>
                  <router-link :to="`/inboxes/${$route.params.inboxId}/tickets`" class="mt-1 flex items-center">
                    <span>See tickets</span>
                    <ArrowRightIcon class="ml-1 inline-block h-4 w-4" />
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="onboarding.active">
          <h2 class="pt-4 text-lg font-semibold leading-4 text-gray-700">Tickets</h2>

          <div class="group mt-2 flex flex-col rounded-lg border p-3">
            <div class="mb-1 flex justify-between">
              <div class="flex space-x-2 text-red-600">
                <ExclamationCircleIcon class="h-5 w-5" />
                <span class="text-sm font-medium">HIGH</span>
              </div>
              <span class="inline-flex items-center rounded bg-green-100 px-2 py-0.5 text-xs font-medium text-green-800">Created</span>
            </div>

            <h2 class="text-lg font-semibold leading-6 group-hover:underline">This is an example ticket</h2>

            <div class="flex items-center justify-between">
              <h3 class="text-xs text-gray-500 dark:text-gray-400"><span class="font-medium">John Doe</span>・{{ moment().calendar() }}</h3>
            </div>

            <div class="mt-2 flex select-none items-center space-x-1">
              <chip :background="'#dd6b20'">Lectures</chip>
            </div>
          </div>
        </div>

        <h2 v-if="ticketsFlattened?.filter((t) => t.open)?.length > 0" class="pt-4 text-lg font-semibold leading-4 text-gray-700">Your tickets</h2>

        <div v-if="ticketsFlattened?.filter((t) => t.open)?.length > 0" class="flex flex-col space-y-2">
          <router-link v-for="ticket in ticketsFlattened?.filter((t) => t.open)" :key="ticket.id" :to="`/inboxes/${1}/tickets/${ticket.ticket_inbox_id}`" class="group flex flex-col rounded-lg border p-3">
            <!-- <div class="mb-1 flex justify-between">
              <div class="flex space-x-2 text-orange-600">
                <ExclamationCircleIcon class="h-5 w-5" />
                <span class="text-sm font-medium">MEDIUM</span>
              </div>
              <span class="inline-flex items-center rounded bg-green-100 px-2 py-0.5 text-xs font-medium text-green-800">Response</span>
            </div> -->

            <h2 class="text-lg font-semibold leading-6 group-hover:underline">
              {{ ticket.title }}
            </h2>

            <div class="flex items-center justify-between">
              <h3 class="text-xs text-gray-500 dark:text-gray-400">
                <span class="font-medium">{{ ticket.author.first_name + ' ' + ticket.author.last_name }}</span
                >・{{ moment.parseZone(ticket.date_created).fromNow() }}
              </h3>
            </div>

            <div class="mt-2 flex select-none items-center space-x-1">
              <chip :background="label.color" :key="label.id" v-for="label in ticket.labels.slice(0, 1)">
                {{ label.name }}
              </chip>
              <span v-if="ticket.labels.length > 1" class="text-xs text-gray-600">+{{ ticket.labels.length - 1 }}</span>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </div>

  <div v-else-if="role == 'AGENT' || role == 'MANAGER'">
    <div class="p-4">
      <div class="mx-auto flex max-w-3xl flex-col space-y-2">
        <!-- <div class="mb-1">
          <h2 class="text-xl font-bold leading-6 text-gray-700">Overview</h2>
        </div> -->

        <div class="grid grid-cols-2 gap-2">
          <div class="overflow-hidden rounded-lg border bg-white">
            <div class="p-2 px-4">
              <div class="flex items-center">
                <div class="hidden flex-shrink-0 sm:flex">
                  <InboxStackIcon class="h-6 w-6 text-gray-400" />
                </div>
                <div class="w-0 flex-1 sm:ml-5">
                  <dl>
                    <dt class="truncate text-sm font-medium text-gray-500">Helpfulness</dt>
                    <dd class="flex items-center justify-between">
                      <div class="text-xl font-medium text-primary">
                        {{ statsData?.user?.helpfulness }}%
                        <!-- <span class="ml-1 hidden text-sm font-medium text-gray-500 lg:inline"> from 71% last week </span> -->
                      </div>

                      <!-- <div :class="['increase' === 'increase' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800', 'inline-flex items-baseline rounded-full px-2.5 py-0.5 text-sm font-medium md:mt-2 lg:mt-0']">
                        <ArrowSmallUpIcon v-if="'up' === 'up'" class="-ml-1 mr-0.5 h-5 w-5 flex-shrink-0 self-center" :class="['increase' === 'increase' ? 'text-green-500' : 'text-red-500']" aria-hidden="true" />
                        <ArrowSmallDownIcon v-else class="-ml-1 mr-0.5 h-5 w-5 flex-shrink-0 self-center" :class="['increase' === 'increase' ? 'text-green-500' : 'text-red-500']" aria-hidden="true" />
                        <span class="sr-only"> {{ 'increase' === 'increase' ? 'Increased' : 'Decreased' }} by </span>
                        33%
                      </div> -->
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="overflow-hidden rounded-lg border bg-white">
            <div class="p-2 px-4">
              <div class="flex items-center">
                <div class="hidden flex-shrink-0 sm:flex">
                  <ClockIcon class="h-6 w-6 text-gray-400" />
                </div>
                <div class="w-0 flex-1 sm:ml-5">
                  <dl>
                    <dt class="truncate text-sm font-medium text-gray-500">Your response time</dt>
                    <dd class="flex items-center justify-between">
                      <div class="text-xl font-medium text-primary">
                        {{ statsData?.user?.avg_response_time || '..' }}h
                        <span class="ml-1 hidden text-sm font-medium text-gray-500 lg:inline"> ({{ statsData?.avg_response_time }}h for everyone)</span>
                      </div>

                      <div v-if="statsData?.user?.avg_response_time" :class="[statsData.avg_response_time - statsData.user.avg_response_time > 0 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800', 'inline-flex items-baseline rounded-full px-2.5 py-0.5 text-sm font-medium md:mt-2 lg:mt-0']">
                        <ArrowSmallUpIcon v-if="statsData.avg_response_time - statsData.user.avg_response_time <= 0" class="-ml-1 mr-0.5 h-5 w-5 flex-shrink-0 self-center" :class="[statsData.avg_response_time - statsData.user.avg_response_time > 0 ? 'text-green-500' : 'text-red-500']" aria-hidden="true" />
                        <ArrowSmallDownIcon v-else class="-ml-1 mr-0.5 h-5 w-5 flex-shrink-0 self-center" :class="['increase' === 'increase' ? 'text-green-500' : 'text-red-500']" aria-hidden="true" />
                        <span class="sr-only"> {{ 'increase' === 'increase' ? 'Increased' : 'Decreased' }} by </span>
                        {{ Math.abs(Math.round(((statsData.avg_response_time - statsData.user.avg_response_time) / statsData.avg_response_time) * 100)) }}%
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        <h2 class="pt-4 text-lg font-semibold leading-4 text-gray-700">Insights</h2>

        <div v-if="Object.values(updates).filter(u => u == true).length == 0" class="flex rounded-lg border p-2">
          <img :src="awesome" class="w-1/3 md:w-1/5" />
          <div class="flex flex-col px-4">
            <h2 class="text-xl font-bold text-primary">All good</h2>
            <p class="text-sm">Right now there are no insights that require your attention</p>
          </div>
        </div>

        <template v-else>
          <!-- Response time is high -->
          <div v-if="updates.highResponseTime" class="rounded-md bg-yellow-50 p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <!-- Heroicon name: mini/exclamation-triangle -->
                <svg class="h-5 w-5 text-yellow-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd" d="M8.485 3.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.17 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 3.495zM10 6a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0v-3.5A.75.75 0 0110 6zm0 9a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" />
                </svg>
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-yellow-800">Response time is high</h3>
                <div class="mt-1 text-sm text-yellow-700">
                  <p>Your response time on tickets is <strong>high</strong> in comparison to the other staff members. Try to check your page more often to reduce the response time.</p>
                  <p class="mt-1">You can check the <router-link :to="{ name: 'Insights', params: { inboxId: this.$route.params.inboxId, tab: 'tickets' } }" class="text-medium underline">ticket insights</router-link> to see what some good times are when students often ask questions.</p>
                </div>
              </div>
            </div>
          </div>

          <!-- No feedback yet so helpfulness is 0 -->
          <div v-if="updates.noFeedbackYet" class="rounded-md bg-blue-50 p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <!-- Heroicon name: mini/exclamation-triangle -->
                <InformationCircleIcon class="h-5 w-5 text-blue-400" aria-hidden="true" />
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-blue-700">No feedback yet</h3>
                <div class="mt-1 text-sm text-blue-700">
                  <p class="mb-2">Your <strong>helpfulness</strong> is currently showing 0, but that is because no one gave feedback on your response yet. People can mark your comments as <strong>helpful</strong> or <strong>not helpful</strong> which will display your helpfulness here.</p>
                  <div class="inline-flex items-center px-3 py-0.5 rounded-full text-sm border text-primary bg-white font-medium">
                    <HandThumbUpIcon class="h-4 w-4 text-primary mr-1" />
                    Helpful
                  </div>
                  <div class="inline-flex items-center px-3 py-0.5 rounded-full text-sm border text-primary bg-white">
                    <HandThumbDownIcon class="h-4 w-4 text-primary mr-1" />
                    Not Helpful
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Helpfulness is low -->
          <div v-if="updates.helpfulnessLow" class="rounded-md bg-yellow-50 p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <!-- Heroicon name: mini/exclamation-triangle -->
                <svg class="h-5 w-5 text-yellow-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd" d="M8.485 3.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.17 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 3.495zM10 6a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0v-3.5A.75.75 0 0110 6zm0 9a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" />
                </svg>
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-yellow-800">Helpfulness is low</h3>
                <div class="mt-1 text-sm text-yellow-700">
                  <p>People think your helpfulness is <strong>low</strong>. Try to pay attention to the reponses you give on questions to improve your helpfulness.</p>
                </div>
              </div>
            </div>
          </div>
        </template>

        <div v-if="false" class="rounded-md bg-blue-50 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <ClockIcon class="h-5 w-5 text-blue-400" aria-hidden="true" />
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-blue-700">Good you are here</h3>
              <div class="mt-2 text-sm text-blue-700">
                <p>But most tickets come around <strong>17:00</strong>, so try to come back then to answer tickets quickly</p>
              </div>
            </div>
          </div>
        </div>

        <h2 class="pt-4 text-lg font-semibold leading-4 text-gray-700">Tickets</h2>

        <div v-if="ticketsFlattened?.length == 0" class="flex rounded-lg border p-2">
          <img :src="awesome" class="w-1/3 md:w-1/5" />
          <div class="flex flex-col px-4">
            <h2 class="text-xl font-bold text-primary">Well done!</h2>
            <p class="text-sm">Right now there are no tickets that require your attention</p>
          </div>
        </div>

        <div v-if="ticketsFlattened?.filter((t) => t.open)?.length > 0" class="flex flex-col space-y-2">
          <router-link v-for="ticket in ticketsFlattened?.filter((t) => t.open)" :key="ticket.id" :to="`/inboxes/${1}/tickets/${ticket.ticket_inbox_id}`" class="group flex flex-col rounded-lg border p-3">
            <div v-if="ticket.assignee.id == undefined" class="mb-1 flex justify-between">
              <div class="flex space-x-2 text-red-600">
                <ExclamationCircleIcon class="h-5 w-5" />
                <span class="text-sm font-medium">HIGH</span>
              </div>
              <span class="inline-flex items-center rounded bg-green-100 px-2 py-0.5 text-xs font-medium text-green-800">New ticket</span>
            </div>

            <h2 class="text-lg font-semibold leading-6 group-hover:underline">
              {{ ticket.title }}
            </h2>

            <div class="flex items-center justify-between">
              <h3 class="text-xs text-gray-500 dark:text-gray-400">
                <span class="font-medium">{{ ticket.author.first_name + ' ' + ticket.author.last_name }}</span
                >・{{ moment.parseZone(ticket.date_created).fromNow() }}
              </h3>
            </div>

            <div v-if="ticket.labels.length > 0" class="mt-2 flex select-none items-center space-x-1">
              <chip :background="label.color" :key="label.id" v-for="label in ticket.labels.slice(0, 1)">
                {{ label.name }}
              </chip>
              <span v-if="ticket.labels.length > 1" class="text-xs text-gray-600">+{{ ticket.labels.length - 1 }}</span>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </div>

  <div v-else-if="role == 'STUDENT'">
    <div class="p-4">
      <div class="mx-auto flex max-w-3xl flex-col space-y-4">
        <!-- <div class="mb-1">
          <h2 class="text-xl font-bold leading-6 text-gray-700">Overview</h2>
        </div> -->

        <div class="grid grid-cols-2 gap-2">
          <div class="overflow-hidden rounded-lg border bg-white">
            <div class="p-2 px-4">
              <div class="flex items-center">
                <div class="hidden flex-shrink-0 sm:flex">
                  <ChatBubbleLeftRightIcon class="h-6 w-6 text-gray-400" />
                </div>
                <div class="w-0 flex-1 sm:ml-5">
                  <dl>
                    <dt class="truncate text-sm font-medium text-gray-500">Tickets</dt>
                    <dd class="flex items-center justify-between">
                      <div class="text-xl font-medium text-primary">
                        {{ ticketsFlattened?.length }}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="overflow-hidden rounded-lg border bg-white">
            <div class="p-2 px-4">
              <div class="flex items-center">
                <div class="hidden flex-shrink-0 sm:flex">
                  <ChatBubbleLeftRightIcon class="h-6 w-6 text-gray-400" />
                </div>
                <div class="w-0 flex-1 sm:ml-5">
                  <dl>
                    <dt class="truncate text-sm font-medium text-gray-500">Public tickets</dt>
                    <dd class="flex items-center justify-between">
                      <div class="text-xl font-medium text-primary">
                        {{ ticketsFlattened?.filter(t => t.is_public)?.length }}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="ticketsFlattened?.length == 0" class="rounded-lg border p-2">
          <div class="flex">
            <img :src="relax" class="w-1/3 md:w-1/5" />
            <div class="flex flex-col px-4 w-full">
              <h2 class="text-xl font-bold text-primary">Welcome</h2>
              <p class="text-sm">Looks like you don't have any questions yet. Feel free to ask something!</p>
            </div>
          </div>
          <div class="pt-2 flex justify-end">
            <router-link :to="'/inboxes/' + $route.params.inboxId + '/tickets/new'" exact type="button" class="inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-orange-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
              <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
              </svg>
              New Ticket
            </router-link>
          </div>
        </div>

        <!-- <ul role="list" class="divide-y divide-gray-100">
          <router-link :to="`/inboxes/${$route.params.inboxId}/tickets/${ticket.ticket_inbox_id}`" as="li" v-for="ticket in ticketsFlattened" :key="ticket.id" class="group flex flex-wrap items-center justify-between gap-x-6 gap-y-4 py-5 sm:flex-nowrap">
            <div>
              <p class="text-sm font-semibold leading-6 text-gray-900">
                <a :href="ticket.href" class="group-hover:underline">{{ ticket.title }}</a>
              </p>
              <div class="mt-1 flex items-center gap-x-2 text-xs leading-5 text-gray-500">
                <p>
                  <time :datetime="ticket.date_latest_update">{{ moment(ticket.date_latest_update).calendar() }}</time>
                </p>
                <svg viewBox="0 0 2 2" class="h-0.5 w-0.5 fill-current">
                  <circle cx="1" cy="1" r="1" />
                </svg>
              </div>
            </div>
            <dl class="flex w-full flex-none justify-between gap-x-8 sm:w-auto">
              <div class="flex -space-x-0.5">
                <dt class="sr-only">Commenters</dt>
                <dd v-for="commenter in ticket.commenters" :key="commenter.id">
                  <img class="h-6 w-6 rounded-full bg-gray-50 ring-2 ring-white" :src="commenter.imageUrl" :alt="commenter.name" />
                </dd>
              </div>
              <div class="flex w-16 gap-x-2.5">
                <dt>
                  <span class="sr-only">Total comments</span>
                  <CheckCircleIcon v-if="ticket.status === 'resolved'" class="h-6 w-6 text-gray-400" aria-hidden="true" />
                  <ChatBubbleLeftIcon v-else class="h-6 w-6 text-gray-400" aria-hidden="true" />
                </dt>
                <dd class="text-sm leading-6 text-gray-900">{{ ticket.totalComments }}</dd>
              </div>
            </dl>
          </router-link>
        </ul> -->
      </div>
      <div v-if="ticketsFlattened?.length > 0" class="mx-auto flex max-w-3xl flex-col space-y-2 mt-6">
        <div class="mb-1">
          <h2 class="text-xl font-bold leading-6 text-gray-700">Your tickets</h2>
        </div>

        <div v-if="ticketsFlattened?.filter((t) => t.open)?.length == 0">
          <router-link :to="`/inboxes/${$route.params.inboxId}/tickets/new`" type="button" class="relative block w-full rounded-lg border-2 border-dashed border-gray-300 p-4 text-center hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2">
            <svg class="mx-auto h-12 w-12 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>

            <span class="mt-2 block text-sm font-medium text-gray-900">Create a new ticket</span>
          </router-link>
        </div>

        <div v-else>
          <ul class="divide-y divide-gray-100 border-b border-gray-200">
            <li v-for="ticket in ticketsFlattened?.filter((t) => t.open)" :key="ticket.id">
              <router-link :to="`/inboxes/${$route.params.inboxId}/tickets/${ticket.ticket_inbox_id}`" class="group flex items-center justify-between py-3 hover:bg-gray-50">
                <div class="flex flex-col sm:inline-flex sm:flex-row items-start sm:items-center space-y-1 sm:space-y-0 text-sm font-medium leading-4">
                  <span>{{ ticket.title }}</span>
                  <div class="flex space-x-2">
                    <span v-if="ticket.is_public != null" class="inline-flex sm:ml-3 items-center rounded-full bg-white border py-0.5 px-2 text-xs font-medium text-gray-700">
                      <GlobeEuropeAfricaIcon class="h-4 w-4 text-green-500" aria-hidden="true"/>
                      <span class="text-green-700 text-xs font-bold ml-1">Public</span>
                    </span>
                    <span v-if="ticket.author.id != user.id" class="inline-flex sm:ml-3 items-center rounded-full bg-white border py-0.5 px-2 text-xs font-medium text-gray-700">
                      <ShareIcon class="h-4 w-4 text-primary" aria-hidden="true"/>
                      <span class="text-primary text-xs font-bold ml-1">Shared with you</span>
                    </span>
                  </div>
                </div>
                <ChevronRightIcon class="ml-4 h-5 w-5 text-gray-400 group-hover:text-gray-500" aria-hidden="true" />
              </router-link>
            </li>
          </ul>
        </div>

        <div v-if="ticketsFlattened?.filter((t) => !t.open).length > 0">
          <h2 class="pb-2 pt-4 text-lg font-semibold leading-4 text-gray-700">Closed tickets</h2>

          <ul class="divide-y divide-gray-100 border-b border-gray-200">
            <li v-for="ticket in ticketsFlattened?.filter((t) => !t.open)" :key="ticket.id">
              <router-link :to="`/inboxes/${$route.params.inboxId}/tickets/${ticket.ticket_inbox_id}`" class="group flex items-center justify-between py-3 hover:bg-gray-50">
                <span class="flex items-center space-x-2 truncate">
                  <span class="truncate text-sm font-medium leading-4">
                    {{ ticket.title }}
                  </span>
                </span>
                <ChevronRightIcon class="ml-4 h-5 w-5 text-gray-400 group-hover:text-gray-500" aria-hidden="true" />
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import store from '@/store'
import { mapState, mapActions } from 'vuex'
import moment from 'moment'

import Chip from '@/components/chip/Chip.vue'
import TicketCard from '@/components/tickets/TicketCard.vue'

import { BellIcon, ChatBubbleLeftRightIcon, ExclamationCircleIcon, InboxStackIcon, ChatBubbleLeftIcon, CheckCircleIcon, StarIcon, HandThumbDownIcon, ClockIcon } from '@heroicons/vue/24/outline'
import { ArrowSmallDownIcon, ArrowSmallUpIcon, ChevronRightIcon, InformationCircleIcon, HandThumbUpIcon } from '@heroicons/vue/24/solid'
import { ArrowRightIcon, ExclamationTriangleIcon, GlobeEuropeAfricaIcon, ShareIcon } from '@heroicons/vue/20/solid'

import report from '@/assets/img/svg/report.svg'
import awesome from '@/assets/img/svg/awesome.svg'
import relax from '@/assets/img/svg/relax.svg'

const UNLABELLED_LABEL = {
  id: 0,
  name: 'Unlabelled',
  color: '#2D3748'
}

export default {
  name: 'Overview',
  components: {
    ArrowSmallDownIcon,
    ArrowSmallUpIcon,
    BellIcon,
    Chip,
    ClockIcon,
    ExclamationCircleIcon,
    InboxStackIcon,
    ChatBubbleLeftRightIcon,
    ExclamationTriangleIcon,
    ArrowRightIcon,
    ChevronRightIcon,
    TicketCard,
    InformationCircleIcon,
    ChatBubbleLeftIcon,
    CheckCircleIcon,
    StarIcon,
    GlobeEuropeAfricaIcon,
    ShareIcon,
    HandThumbUpIcon,
    HandThumbDownIcon
},
  data: () => ({
    role: 'STUDENT',
    labels: [],
    inbox_labels: [],
    report,
    awesome,
    relax,
    statsData: {}
  }),
  async created() {
    await axios.get(`/api/inboxes/${this.$route.params.inboxId}/labels/all`).then((response) => {
      this.inbox_labels = response.data.concat([UNLABELLED_LABEL])
    })

    await axios.get(`/api/inboxes/${this.$route.params.inboxId}/role`).then((response) => {
      if (response.data.key === 'MANAGER') this.role = 'MANAGER'
      else if (response.data.key === 'AGENT') this.role = 'AGENT'
      else this.role = 'STUDENT'
    })

    this.get_tickets()
  },
  setup() {
    return { moment }
  },
  methods: {
    ...mapActions('onboarding', {
      nextStep: 'next',
      prevStep: 'prev'
    }),
    async get_tickets() {
      // Call this function by using callDebounceGetTickets
      const labelsIds = []
      this.labels.forEach((label) => labelsIds.push(label.id))
      const { inboxId } = this.$route.params

      await axios
        .get(`/api/inboxes/${inboxId}/tickets`, {
          params: {
            q: this.search,
            show_personal: true,
            labels: labelsIds
          }
        })
        .then(async (response) => {
          if (!store.getters.inbox(inboxId)) await store.dispatch('update_inboxes')

          store.commit('update_tickets', {
            inbox: inboxId,
            tickets: response.data
          })
        })

      if (this.role == 'STUDENT') return
      
      /* Gettings general statistics. */
      const statsResponse = await axios.get(`/api/inboxes/${inboxId}/statistics/staff`)
      this.statsData = statsResponse.data
      this.statsData.user = this.statsData.staff.find(s => s.id == this.user.id)
    }
  },
  computed: {
    ticketsFlattened() {
      return this.tickets
        ?.flatMap((c) => {
          for (let i = 0; i < c.tickets.length; i++) c.tickets[i].open = c.label !== 'Closed'

          return c.tickets
        })
        .sort((a, b) => a.date_created < b.date_created)
    },
    updates() {
      if (this.statsData?.user == undefined) return {}
      let updates = {}

      if (Math.round(((this.statsData.avg_response_time - this.statsData.user.avg_response_time) / this.statsData.avg_response_time) * 100) < -25) updates.highResponseTime = true
      else updates.highResponseTime = false

      if (this.statsData.user.amount_of_helpful_comments == 0) updates.noFeedbackYet = true
      else updates.noFeedbackYet = false

      if (this.statsData.user.amount_of_helpful_comments > 0 && this.statsData.user.helpfulness < 50) updates.helpfulnessLow = true
      else updates.helpfulnessLow = false

      return updates
    },
    ...mapState({
      user: (state) => state.user,
      tickets() {
        return store.getters.inbox(this.$route.params.inboxId)?.tickets
      }
    }),
    ...mapState('onboarding', {
      onboarding: (state) => state.status
    })
  }
}
</script>
