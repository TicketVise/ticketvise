<template>
  <div class="flex-1 relative overflow-y-auto focus:outline-none">
    <PublishConfirmation
      @click="requestPublish"
      @cancel="publishConfirmationModal = false"
      v-if="publishConfirmationModal"
    />
    <PrivateConfirmation
      @click="makePrivate"
      @cancel="privateConfirmationModal = false"
      v-if="privateConfirmationModal"
    />
    <div class="py-4 pt-0 md:pt-4">
      <div class="max-w-3xl mx-auto px-4">
        <div class="md:flex md:items-center md:justify-between md:space-x-4">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">
              {{ ticket?.title }}
            </h1>
            <p class="text-sm text-gray-500 flex space-x-2 items-center font-medium">
              <span>
                <span v-if="ticket?.author">
                  {{ ticket?.author?.first_name }}
                  {{ ticket?.author?.last_name }}
                </span>
                <span v-else>Someone in this inbox</span>
              </span>
              <span>&#183;</span>
              <time :datetime="ticket?.date_created">{{ date(ticket?.date_created) }}</time>
            </p>
          </div>
          <!-- <div class="flex space-x-3 md:mt-0">
            <button
              @click="publishConfirmationModal = true"
              v-if="
                isStaff(role, user) &&
                !ticket?.publish_request_created &&
                !ticket?.is_public
              "
              type="button"
              class="inline-flex justify-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
            >
              <CloudIcon
                class="-ml-1 mr-2 h-5 w-5 text-primary-400"
                aria-hidden="true"
              />
              <span>Publish</span>
            </button>
            <button
              @click="privateConfirmationModal = true"
              v-if="isStaff(role, user) && ticket?.is_public"
              type="button"
              class="inline-flex justify-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
            >
              <LockIcon
                class="-ml-1 mr-2 h-5 w-5 text-primary-400"
                aria-hidden="true"
              />
              <span>Private</span>
            </button>
            <button type="button" class="inline-flex justify-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-900">
              <svg class="-ml-1 mr-2 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z" />
              </svg>
              <span>Subscribe</span>
            </button>
          </div> -->
        </div>

        <!-- Status chips -->
        <div class="flex flex-wrap mt-2">
          <Listbox v-if="isStaffOrAuthor" as="span" class="relative block mb-2 mr-2">
            <ListboxButton @click="listboxAlignment('publicListbox')" class="relative flex items-center w-full text-sm font-medium focus:outline-none">
              <span class="flex justify-between items-center rounded-full bg-white border py-1 pl-2 pr-2 text-xs w-full font-medium text-gray-700">
                <div class="flex space-x-1 mr-1">
                  <GlobeEuropeAfricaIcon
                    v-if="ticket?.is_public"
                    class="h-4 w-4 text-green-500"
                    aria-hidden="true"
                  />
                  <LockClosedIcon
                    v-else
                    class="h-4 w-4 text-red-500 ml-1"
                    aria-hidden="true"
                  />
                  <span
                    :class="[
                      ticket?.is_public ? 'text-green-700' : 'text-red-700',
                      'text-xs font-medium',
                    ]"
                  >
                    {{ ticket?.is_public ? "PUBLIC" : "PRIVATE" }}
                  </span>
                </div>
                <ChevronDownIcon class="h-4 w-4 text-gray-400" aria-hidden="true" />
              </span>
            </ListboxButton>
            <transition
              leave-active-class="transition ease-in duration-100"
              leave-from-class="opacity-100"
              leave-to-class="opacity-0"
            >
              <ListboxOptions ref="publicListbox" class="absolute z-10 mt-2 bg-white shadow-xl max-h-56 min-w-max rounded-md py-1 text-xs ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm">
                <ListboxOption as="template" v-slot="{ active }">
                  <li @click="publishConfirmationModal = true" :class="[active ? 'text-white bg-primary' : 'text-gray-900', 'flex space-x-1 items-center cursor-pointer select-none relative py-2 pl-3 pr-4']">
                    <GlobeEuropeAfricaIcon class="h-4 w-4 text-green-500" aria-hidden="true"/>
                    <span class="block text-xs">Make public</span>
                  </li>
                </ListboxOption>
              </ListboxOptions>
            </transition>
          </Listbox>
          <span v-else class="flex space-x-1 items-center rounded-full bg-white border py-1 pl-2 pr-3 text-xs font-medium text-gray-700 mb-2 mr-2">
            <GlobeEuropeAfricaIcon v-if="ticket?.is_public" class="h-4 w-4 text-green-500" aria-hidden="true"/>
            <LockClosedIcon v-else class="h-4 w-4 text-red-500 ml-1" aria-hidden="true"/>
            <span :class="[ticket?.is_public ? 'text-green-700' : 'text-red-700', 'text-xs font-medium']">
              {{ ticket?.is_public ? "PUBLIC" : "PRIVATE" }}
            </span>
          </span>

          <Listbox v-if="ticket?.assignee?.first_name" as="span" class="relative block mb-2 mr-2">
            <ListboxButton @click="listboxAlignment('staffListbox')" class="relative flex items-center w-full text-sm font-medium focus:outline-none">
              <span class="flex justify-between items-center rounded-full bg-white border py-1 pl-3 pr-2 text-xs w-full font-medium text-gray-700">
                <div class="flex space-x-1 mr-1">
                  <img
                    class="h-4 w-4 rounded-full mr-1"
                    :src="ticket?.assignee?.avatar_url"
                    alt=""
                  />
                  <span class="text-gray-900 text-xs font-medium">
                    {{ ticket?.assignee?.first_name + ' ' + ticket?.assignee?.last_name }}
                  </span>
                </div>
                <ChevronDownIcon class="h-4 w-4 text-gray-400" aria-hidden="true" />
              </span>
            </ListboxButton>
            <transition
              leave-active-class="transition ease-in duration-100"
              leave-from-class="opacity-100"
              leave-to-class="opacity-0"
            >
              <ListboxOptions ref="staffListbox" class="absolute z-10 mt-2 bg-white shadow-xl max-h-56 min-w-max rounded-md py-1 text-xs ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm">
                <ListboxOption
                  as="template"
                  v-for="assignee in staff"
                  :key="assignee.id"
                  :value="assignee"
                  v-slot="{ active }"
                >
                  <li
                    @click="updateAssignee(assignee)"
                    :class="[
                      active ? 'text-white bg-primary' : 'text-gray-900',
                      'cursor-pointer select-none relative py-2 pl-3 pr-9',
                    ]"
                  >
                    <div class="flex items-center space-x-2">
                      <div class="flex-shrink-0">
                        <img
                          class="h-4 w-4 rounded-full"
                          :src="assignee.avatar_url"
                          alt=""
                        />
                      </div>
                      <span class="block truncate"
                        >{{ assignee.first_name }}
                        {{ assignee.last_name }}</span
                      >
                    </div>

                    <span
                      v-if="assignee.id === ticket?.assignee.id"
                      :class="[
                        active ? 'text-white' : 'text-primary-600',
                        'absolute inset-y-0 right-0 flex items-center pr-2',
                      ]"
                    >
                      <CheckIcon class="h-5 w-5" aria-hidden="true" />
                    </span>
                  </li>
                </ListboxOption>
              </ListboxOptions>
            </transition>
          </Listbox>
          <button v-else-if="isStaff(user.role, user)" @click="updateAssignee(user)" class="flex space-x-1 items-center rounded-full bg-white border py-1 px-3 text-xs font-medium text-gray-700 mb-2 mr-2">
            <UserCircleIcon class="h-4 w-4 text-primary" aria-hidden="true" />
            <span class="text-primary text-xs font-medium uppercase">Assign Yourself</span>
          </button>
          
          <span class="flex space-x-1 items-center rounded-full bg-white border py-1 px-3 text-xs font-medium text-gray-700 mb-2 mr-2">
            <ClipboardDocumentCheckIcon
              v-if="ticket?.status === 'CLSD'"
              class="h-4 w-4 text-gray-400"
              aria-hidden="true"
            />
            <ClipboardDocumentListIcon
              v-else
              class="h-4 w-4 text-gray-400"
              aria-hidden="true"
            />
            <span v-if="ticket?.status != 'CLSD' && !isStaff(user.role, user)" class="text-gray-900 text-xs font-medium">OPEN</span>
            <span v-else-if="ticket?.status === 'ASGD'" class="text-gray-900 text-xs font-medium">ASSIGNED</span>
            <span v-else-if="ticket?.status === 'ANSD'" class="text-gray-900 text-xs font-medium">AWAITING RESPONSE</span>
            <span v-else-if="ticket?.status === 'PNDG' || !ticket" class="text-gray-900 text-xs font-medium">PENDING</span>
            <span v-else-if="ticket?.status === 'CLSD'" class="text-gray-900 text-xs font-medium">CLOSED</span>
          </span>
          
          <Listbox v-if="isStaffOrAuthor" as="span" class="relative block mb-2 mr-2">
            <ListboxButton @click="listboxAlignment('labelListbox')" class="relative flex items-center w-full text-sm font-medium focus:outline-none">
              <span class="flex justify-between items-center rounded-full bg-white border py-1 pl-3 pr-2 text-xs w-full font-medium text-gray-700">
                <span v-if="ticket?.labels?.[0]" class="flex space-x-1 items-center">
                  <div :style="`background-color: ${ticket?.labels?.[0]?.color}`" class="w-2 h-2 rounded-full flex-col mr-1" v-if="ticket?.labels?.[0]?.color"></div>
                  <span>{{ ticket?.labels?.[0]?.name }}</span>
                </span>
                <button v-else class="flex space-x-1 items-center">
                  <TagIcon class="h-4 w-4 text-primary" aria-hidden="true" />
                  <span class="text-primary text-xs font-medium uppercase">Choose a label</span>
                </button>
                <ChevronDownIcon class="h-4 w-4 text-gray-400 ml-1" aria-hidden="true" />
              </span>
            </ListboxButton>
            <transition
              leave-active-class="transition ease-in duration-100"
              leave-from-class="opacity-100"
              leave-to-class="opacity-0"
            >
              <ListboxOptions ref="labelListbox" class="absolute z-10 mt-2 bg-white shadow-xl max-h-56 min-w-max rounded-md py-1 text-xs ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm">
                <ListboxOption
                  as="template"
                  v-for="label in ticket?.inbox.labels"
                  :key="label.id"
                  :value="label"
                  v-slot="{ active }"
                >
                  <li
                    @click="toggleLabel(label)"
                    :class="[
                      active
                        ? 'text-white bg-primary'
                        : 'text-gray-900',
                      'cursor-pointer select-none relative py-2 pl-3 pr-9',
                    ]"
                  >
                    <div class="flex items-center space-x-3">
                      <div
                        :style="`background-color: ${label.color};`"
                        class="w-2 h-2 rounded-full"
                      ></div>
                      <span
                        :class="[
                          containsObject(ticket?.labels, label.id)
                            ? 'font-semibold'
                            : 'font-normal',
                          'block truncate',
                        ]"
                      >
                        {{ label.name }}
                      </span>
                    </div>

                    <span
                      v-if="containsObject(ticket?.labels, label.id)"
                      :class="[
                        active ? 'text-white' : 'text-primary-600',
                        'absolute inset-y-0 right-0 flex items-center pr-2',
                      ]"
                    >
                      <CheckIcon class="h-5 w-5" aria-hidden="true" />
                    </span>
                  </li>
                </ListboxOption>
              </ListboxOptions>
            </transition>
          </Listbox>
          <span v-else-if="ticket?.labels?.[0]" class="flex space-x-1 items-center rounded-full bg-white border py-1 pl-3 pr-2 text-xs font-medium text-gray-700 mb-2 mr-2">
            <div :style="`background-color: ${ticket?.labels?.[0]?.color}`" class="w-2 h-2 rounded-full flex-col mr-1" v-if="ticket?.labels?.[0]?.color"></div>
            <span>{{ ticket?.labels?.[0]?.name }}</span>
            <ChevronDownIcon class="h-4 w-4 text-gray-400" aria-hidden="true" />
          </span>
        </div>

        <!-- Pending publish request -->
        <div v-if="!ticket?.is_public && ticket?.publish_request_created && isStaff(role, user)" class="rounded-md bg-blue-50 p-4 mt-2">
          <div class="flex">
            <div class="flex-shrink-0">
              <InformationCircleIcon
                class="h-5 w-5 text-blue-400"
                aria-hidden="true"
              />
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-blue-800">
                Publish request pending
              </h3>
              <div class="mt-1 text-sm text-blue-700">
                <p>
                  Just so you know, the request to make this ticket public is still waiting for approval from the author. Once they give the green light, this ticket will be visible to everyone in the inbox. Hang tight!
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Accept publish request as student -->
        <div v-if="!ticket?.is_public && ticket?.publish_request_initiator && ticket?.author.id == user.id" class="rounded-md bg-green-50 p-4 mt-2">
          <div class="flex">
            <div class="">
              <h3 class="text-sm font-medium text-green-800">
                Sharing is caring
              </h3>
              <div class="mt-1 text-sm text-green-700">
                <p class="mb-2 text-justify">
                  Hey, {{ ticket.publish_request_initiator.first_name }}
                  {{ ticket.publish_request_initiator.last_name }} has requested that this ticket be made public for everyone in this inbox to see. Public tickets can be really helpful for others because they can get answers to their questions before they even have to ask.
                </p>
                <div class="relative flex items-start">
                  <div class="flex items-center h-5">
                    <input
                      v-model="ticket.is_anonymous"
                      id="anonymize"
                      aria-describedby="anonymize-description"
                      name="anonymize"
                      type="checkbox"
                      class="focus:ring-green-500 h-4 w-4 text-green-600 border-gray-300 rounded"
                    />
                  </div>
                  <div class="ml-2 text-sm">
                    <label
                      for="anonymize"
                      class="font-medium text-green-700"
                      >Anonymize before publish</label
                    >
                    <p id="comments-description" class="text-green-700">
                      An anonymous ticket does not show the author or its
                      role, but does show the conversation and
                      attachments.
                    </p>
                  </div>
                </div>
              </div>
              <div class="mt-4">
                <div class="-mx-2 -my-1.5 flex">
                  <button
                    @click="publishTicket"
                    type="button"
                    class="bg-green-50 px-2 py-1.5 rounded-md text-sm font-medium text-green-800 hover:bg-green-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-green-50 focus:ring-green-600"
                  >
                    Publish ticket
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- <VueEasyLightbox scrollDisabled moveDisabled :imgs="images?.map((a) => a.file)" :visible="lightbox.visible" :index="lightbox.index" @hide="lightbox.visible = false" />
        <ul role="list" class="grid grid-cols-3 gap-x-4 gap-y-8 sm:grid-cols-3 sm:gap-x-6 md:grid-cols-4 lg:grid-cols-3 xl:grid-cols-4 xl:gap-x-8 mb-4">
          <li v-for="(attachment, index) in images" :key="index">
            <button @click="lightbox.index = index; lightbox.visible = true;" class="group block w-full aspect-w-10 aspect-h-5 rounded-lg bg-gray-100 overflow-hidden">
              <img :src="attachment.file" class="object-cover pointer-events-none" />
              <button type="button" class="absolute inset-0 focus:outline-none">
                <span class="sr-only">View details for {{ attachment.file.substring(attachment.file.lastIndexOf("/") + 1, attachment.file.lastIndexOf(".")) }}</span>
              </button>
            </button>
            <p class="mt-1 block text-xs font-medium text-gray-900 truncate pointer-events-none">
              {{ attachment.file.substring(attachment.file.lastIndexOf("/") + 1) }}
            </p>
            <p class="block text-xs font-medium text-gray-500 pointer-events-none">
              {{ readableBytes(attachment.file_size) }}
            </p>
          </li>
          <fileUpload ref="upload" v-bind:value="files" v-on:input="setFiles" class="w-full" :preview="false" />
        </ul> -->

        <div class="bg-gray-50 rounded-lg px-4 py-1 mt-4">
          <h2 class="sr-only">Description</h2>
          <TicketInputViewer v-if="ticket" :content="ticket.content" />
        </div>
        
        <div class="mt-4">
          <ul role="list" class="grid grid-cols-2 gap-x-4 gap-y-8 sm:grid-cols-3 sm:gap-x-6 lg:grid-cols-4 xl:gap-x-8">
            <li v-for="file in attachments" :key="file" class="relative">
              <div class="group aspect-w-10 aspect-h-7 block w-full overflow-hidden rounded-lg bg-gray-100 focus-within:ring-2 focus-within:ring-primary-500 focus-within:ring-offset-2 focus-within:ring-offset-gray-100">
                <img :src="file.file" alt="" class="pointer-events-none object-cover group-hover:opacity-75" />
                <button type="button" class="absolute inset-0 focus:outline-none">
                  <span class="sr-only">View details for {{ file.title }}</span>
                </button>
              </div>
              <p class="pointer-events-none mt-2 block truncate text-sm font-medium text-gray-900">{{ file.file.substring(file.file.lastIndexOf("/") + 1) }}</p>
              <p class="pointer-events-none block text-sm font-medium text-gray-500">{{ readableBytes(file.file_size) }}</p>
            </li>

            <li class="relative">
              <button type="button" class="relative group aspect-w-10 aspect-h-7 block w-full rounded-lg border-2 border-dashed border-gray-300 text-center hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2">
                <svg class="mx-auto h-12 w-12 text-gray-400" xmlns="http://www.w3.org/2000/svg" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 14v20c0 4.418 7.163 8 16 8 1.381 0 2.721-.087 4-.252M8 14c0 4.418 7.163 8 16 8s16-3.582 16-8M8 14c0-4.418 7.163-8 16-8s16 3.582 16 8m0 0v14m0-4c0 4.418-7.163 8-16 8S8 28.418 8 24m32 10v6m0 0v6m0-6h6m-6 0h-6" />
                </svg>
                <span class="mt-2 block text-sm font-medium text-gray-900">Upload File</span>
              </button>
              <p class="pointer-events-none mt-2 block truncate text-sm font-medium text-gray-900"></p>
              <p class="pointer-events-none block text-sm font-medium text-gray-500"></p>
            </li>
          </ul>
        </div>

        <section aria-labelledby="activity-title" class="mt-8">
          <div>
            <!-- <div class="pb-4">
              <div class="sm:hidden">
                <label for="tabs" class="sr-only">Select a tab</label>
                <select
                  id="tabs"
                  name="tabs"
                  @change="
                    switchTab();
                    tabs.find(
                      (t) => t.name === $event.target.value
                    ).current = true;
                  "
                  class="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm rounded-md"
                >
                  <option
                    v-show="tab.cond ? isStaff(role, user) : true"
                    v-for="tab in tabs"
                    :key="tab.name"
                    :selected="tab.current"
                  >
                    {{ tab.name }}
                  </option>
                </select>
              </div>
              <div class="hidden sm:block">
                <div class="border-b border-gray-200">
                  <nav class="-mb-px flex space-x-8" aria-label="Tabs">
                    <a
                      v-show="tab.cond ? isStaff(role, user) : true"
                      @click="
                        switchTab();
                        tabs.find((t) => t.name === tab.name).current = true;
                      "
                      v-for="tab in tabs"
                      :key="tab.name"
                      href="#"
                      :class="[
                        tab.current
                          ? 'border-primary text-primary-600'
                          : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-200',
                        'whitespace-nowrap flex py-4 px-1 border-b-2 font-medium text-sm',
                      ]"
                      :aria-current="tab.current ? 'page' : undefined"
                    >
                      {{ tab.name }}
                      <span
                        v-if="tab.count !== 0"
                        :class="[
                          tab.current
                            ? 'bg-primary-100 text-primary-600'
                            : 'bg-gray-100 text-gray-900',
                          'hidden ml-3 py-0.5 px-2.5 rounded-full text-xs font-medium md:inline-block',
                        ]"
                        >{{ tab.count }}</span
                      >
                    </a>
                  </nav>
                </div>
              </div>
            </div> -->

            <!-- Activity feed -->
            <activity-feed
              :ticket="ticket"
              :permissions="isStaffOrAuthor"
              v-if="
                tabs.find((t) => t.current).name === 'Activity' && ticket
              "
              v-on:post="loadTicketData"
              v-on:helpful="helpful"
              v-on:unfold="unfold"
            />
            <!-- Staff discussion -->
            <staff-discussion
              :ticket="ticket"
              v-if="tabs.find((t) => t.current).name === 'Staff discussion'"
              v-on:post="loadTicketData"
            />
            <!-- Attachments -->
            <attachments
              :ticket="ticket"
              v-if="tabs.find((t) => t.current).name === 'Attachments'"
              v-on:uploaded="loadTicketData"
            />
          </div>
        </section>

        <!-- <div class="xl:pl-8">
          <h2 class="sr-only">Details</h2>
          <div class="space-y-5">
            <div class="flex items-center space-x-2">
              <LockOpenIcon
                v-if="ticket?.is_public"
                class="h-5 w-5 text-green-500"
                aria-hidden="true"
              />
              <LockClosedIcon
                v-else
                class="h-5 w-5 text-red-500"
                aria-hidden="true"
              />
              <span
                :class="[
                  ticket?.is_public ? 'text-green-700' : 'text-red-700',
                  'text-sm font-medium',
                ]"
              >
                {{ ticket?.is_public ? "Public" : "Private" }}
                Ticket
              </span>
            </div>
            <div class="flex items-center space-x-2">
              <ClipboardDocumentCheckIcon
                v-if="ticket?.status === 'CLSD'"
                class="h-5 w-5 text-gray-400"
                aria-hidden="true"
              />
              <ClipboardDocumentListIcon
                v-else
                class="h-5 w-5 text-gray-400"
                aria-hidden="true"
              />
              <span
                v-if="ticket?.status === 'ASGD'"
                class="text-gray-900 text-sm font-medium"
                >Assigned</span
              >
              <span
                v-if="ticket?.status === 'ANSD'"
                class="text-gray-900 text-sm font-medium"
                >Awaiting response</span
              >
              <span
                v-if="ticket?.status === 'CLSD'"
                class="text-gray-900 text-sm font-medium"
                >Closed</span
              >
              <span
                v-if="ticket?.status === 'PNDG' || !ticket"
                class="text-gray-900 text-sm font-medium"
                >Pending</span
              >
            </div>
            <div class="flex items-center space-x-2">
              <ChatBubbleLeftEllipsisIcon
                class="h-5 w-5 text-gray-400"
                aria-hidden="true"
              />
              <span class="text-gray-900 text-sm font-medium">
                {{ ticket?.replies?.length || 0 }} comment{{
                  ticket?.replies?.length === 1 ? "" : "s"
                }}
              </span>
            </div>
            <div class="flex items-center space-x-2">
              <CalendarIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
              <span class="text-gray-900 text-sm font-medium"
                >Created
                <time :datetime="ticket?.date_created">
                  {{ date(ticket?.date_created) }}</time
                ></span
              >
            </div>
          </div>
          <div class="mt-6 border-t border-gray-200 py-6 space-y-8">
            <div v-if="isStaff(role, user)">
              <Listbox as="span" class="-ml-px relative block">
                <ListboxButton
                  class="relative flex items-center w-full text-sm font-medium focus:outline-none ml-1"
                >
                  <div class="group flex justify-between w-full items-center">
                    <h2
                      class="text-sm font-medium text-gray-500 group-hover:text-gray-800"
                    >
                      Assignee
                    </h2>
                    <Cog6ToothIcon
                      class="h-4 w-4 text-gray-400 group-hover:text-gray-800"
                      aria-hidden="true"
                    />
                  </div>
                </ListboxButton>
                <transition
                  leave-active-class="transition ease-in duration-100"
                  leave-from-class="opacity-100"
                  leave-to-class="opacity-0"
                >
                  <ListboxOptions
                    class="absolute z-10 mt-1 bg-white shadow-lg max-h-56 w-full rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm"
                  >
                    <ListboxOption
                      as="template"
                      v-for="assignee in staff"
                      :key="assignee.id"
                      :value="assignee"
                      v-slot="{ active }"
                    >
                      <li
                        @click="updateAssignee(assignee)"
                        :class="[
                          active ? 'text-white bg-primary' : 'text-gray-900',
                          'cursor-pointer select-none relative py-2 pl-3 pr-9',
                        ]"
                      >
                        <div class="flex items-center space-x-3">
                          <div class="flex-shrink-0">
                            <img
                              class="h-8 w-8 rounded-full"
                              :src="assignee.avatar_url"
                              alt=""
                            />
                          </div>
                          <span class="block truncate"
                            >{{ assignee.first_name }}
                            {{ assignee.last_name }}</span
                          >
                        </div>

                        <span
                          v-if="assignee.id === ticket?.assignee.id"
                          :class="[
                            active ? 'text-white' : 'text-primary-600',
                            'absolute inset-y-0 right-0 flex items-center pr-4',
                          ]"
                        >
                          <CheckIcon class="h-5 w-5" aria-hidden="true" />
                        </span>
                      </li>
                    </ListboxOption>
                  </ListboxOptions>
                </transition>
              </Listbox>
              <div
                class="flex items-center space-x-3 m-2"
                v-if="ticket?.assignee && ticket?.assignee.id"
              >
                <div class="flex-shrink-0">
                  <img
                    class="h-8 w-8 rounded-full"
                    :src="ticket?.assignee.avatar_url"
                    alt=""
                  />
                </div>
                <span class="block truncate"
                  >{{ ticket?.assignee.first_name }}
                  {{ ticket?.assignee.last_name }}</span
                >
              </div>
              <span v-else class="text-gray-400 text-sm ml-3">
                None yet<span v-if="isStaff(role, user)"
                  >—<button
                    @click="assignUser"
                    class="hover:text-primary-600 no-underline"
                  >
                    Assign yourself
                  </button></span
                >
              </span>
            </div>

            <div>
              <div class="relative">
                <h2
                  v-if="!isStaffOrAuthor"
                  class="text-sm font-medium text-gray-500 group-hover:text-gray-800"
                >
                  Labels
                </h2>
                <div v-if="isStaffOrAuthor">
                  <Listbox as="span" class="-ml-px relative block">
                    <ListboxButton
                      class="relative flex items-center w-full text-sm font-medium focus:outline-none ml-1"
                    >
                      <div
                        class="group flex justify-between w-full items-center"
                      >
                        <h2
                          class="text-sm font-medium text-gray-500 group-hover:text-gray-800"
                        >
                          Labels
                        </h2>
                        <Cog6ToothIcon
                          class="h-4 w-4 text-gray-400 group-hover:text-gray-800"
                          aria-hidden="true"
                        />
                      </div>
                    </ListboxButton>
                    <transition
                      leave-active-class="transition ease-in duration-100"
                      leave-from-class="opacity-100"
                      leave-to-class="opacity-0"
                    >
                      <ListboxOptions
                        class="absolute z-10 mt-1 bg-white shadow-lg max-h-56 w-full rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm"
                      >
                        <ListboxOption
                          as="template"
                          v-for="label in ticket?.inbox.labels"
                          :key="label.id"
                          :value="label"
                          v-slot="{ active }"
                        >
                          <li
                            @click="toggleLabel(label)"
                            :class="[
                              active
                                ? 'text-white bg-primary'
                                : 'text-gray-900',
                              'cursor-pointer select-none relative py-2 pl-3 pr-9',
                            ]"
                          >
                            <div class="flex items-center space-x-3">
                              <div
                                :style="`background-color: ${label.color};`"
                                class="w-2 h-2 rounded-full"
                              ></div>
                              <span
                                :class="[
                                  containsObject(ticket?.labels, label.id)
                                    ? 'font-semibold'
                                    : 'font-normal',
                                  'block truncate',
                                ]"
                              >
                                {{ label.name }}
                              </span>
                            </div>

                            <span
                              v-if="containsObject(ticket?.labels, label.id)"
                              :class="[
                                active ? 'text-white' : 'text-primary-600',
                                'absolute inset-y-0 right-0 flex items-center pr-4',
                              ]"
                            >
                              <CheckIcon class="h-5 w-5" aria-hidden="true" />
                            </span>
                          </li>
                        </ListboxOption>
                      </ListboxOptions>
                    </transition>
                  </Listbox>
                </div>
              </div>
              <div
                class="flex flex-wrap mb-2 pt-2"
                v-if="ticket?.labels.length > 0"
              >
                <chip
                  :background="label.color"
                  :key="label.id"
                  class="mr-1 mb-1"
                  v-for="label in ticket?.labels"
                >
                  {{ label.name }}
                </chip>
              </div>
              <span v-else class="text-gray-400 text-sm ml-3">None yet</span>
            </div>
            <div v-if="!ticket?.is_public">
              <h2 class="text-sm font-medium text-gray-500">Shared with</h2>
              <ul class="mt-2 leading-8 divide-y divide-gray-200">
                <li
                  v-for="person in ticket?.shared_with"
                  :key="person.id"
                  class="py-2 flex justify-between items-center"
                >
                  <div class="flex items-center">
                    <img
                      :src="person.avatar_url || person.avatar"
                      alt=""
                      class="w-6 h-6 rounded-full"
                    />
                    <p class="ml-3 text-sm font-medium text-gray-900">
                      {{ person.first_name }} {{ person.last_name }}
                      {{ !person.first_name ? person.name : "" }}
                    </p>
                  </div>
                  <button
                    @click="
                      ticket.shared_with.splice(
                        ticket.shared_with.map((s) => s.id).indexOf(person.id),
                        1
                      );
                      updateSharedWith();
                    "
                    type="button"
                    class="ml-6 bg-white rounded-md text-sm font-medium text-primary-600 hover:text-primary focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
                    v-if="isStaffOrAuthor"
                  >
                    Remove<span class="sr-only"> {{ person.name }}</span>
                  </button>
                </li>
                <li
                  v-if="isStaffOrAuthor"
                  :class="[
                    ticket?.shared_with.length > 0 ? 'py-2' : '',
                    'flex justify-between items-center',
                  ]"
                >
                  <button
                    v-show="!addShare"
                    @click="addShare = true"
                    type="button"
                    class="group -ml-1 bg-white p-1 rounded-md flex items-center focus:outline-none focus:ring-2 focus:ring-primary"
                  >
                    <span
                      class="w-6 h-6 rounded-full border-2 border-dashed border-gray-300 flex items-center justify-center text-gray-400"
                    >
                      <PlusIconSolid class="h-5 w-5" aria-hidden="true" />
                    </span>
                    <span
                      class="ml-3 text-sm font-medium text-primary-600 group-hover:text-primary"
                      >Share</span
                    >
                  </button>
                  <FormTextFieldWithSuggestions
                    v-show="addShare"
                    @add="
                      (data) => {
                        ticket.shared_with.push(data);
                        updateSharedWith();
                        addShare = false;
                      }
                    "
                    :data="guestsFiltered || []"
                    emptyLabel="John Doe"
                  />
                </li>
              </ul>
            </div>
          </div>
        </div> -->
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapState } from "vuex";
import moment from "moment";
import VueEasyLightbox from "vue-easy-lightbox"

import FileUpload from '@/components/inputs/FileInput.vue'
import ActivityFeed from "@/components/tickets/ActivityFeed.vue";
import StaffDiscussion from "@/components/tickets/StaffDiscussion.vue";
import Attachments from "@/components/tickets/Attachments.vue";
import Chip from "@/components/chip/Chip.vue";
import PublishConfirmation from "@/components/tickets/PublishConfirmation.vue";
import PrivateConfirmation from "@/components/tickets/PrivateConfirmation.vue";
import FormTextFieldWithSuggestions from "@/components/form/FormTextFieldWithSuggestions.vue";
import TicketInputViewer from "@/components/inputs/TicketInputViewer.vue";
import Upload from '@/assets/img/svg/upload.svg'

import { ref } from "vue";
import {
  Listbox,
  ListboxButton,
  ListboxOption,
  ListboxOptions,
} from "@headlessui/vue";

import {
  CalendarIcon,
  ChatBubbleLeftEllipsisIcon,
  CheckIcon,
  Cog6ToothIcon,
  InformationCircleIcon,
  PlusIcon as PlusIconSolid,
  ClipboardDocumentListIcon,
  ClipboardDocumentCheckIcon,
  UserCircleIcon,
  ChevronDownIcon
} from "@heroicons/vue/24/solid";

import {
  CloudIcon
} from "@heroicons/vue/24/outline";

import {
  GlobeEuropeAfricaIcon,
  LockClosedIcon,
  TagIcon
} from "@heroicons/vue/20/solid"

export default {
  name: "Ticket",
  components: {
    ActivityFeed,
    Attachments,
    CalendarIcon,
    ChatBubbleLeftEllipsisIcon,
    CheckIcon,
    Chip,
    CloudIcon,
    Cog6ToothIcon,
    FormTextFieldWithSuggestions,
    FileUpload,
    InformationCircleIcon,
    GlobeEuropeAfricaIcon,
    LockClosedIcon,
    Listbox,
    ListboxButton,
    ListboxOption,
    ListboxOptions,
    PlusIconSolid,
    PublishConfirmation,
    PrivateConfirmation,
    StaffDiscussion,
    ClipboardDocumentListIcon,
    ClipboardDocumentCheckIcon,
    TicketInputViewer,
    UserCircleIcon,
    ChevronDownIcon,
    TagIcon,
    VueEasyLightbox
  },
  data: () => ({
    publishConfirmationModal: false,
    privateConfirmationModal: false,
    ticket: null,
    staff: [],
    tabs: [
      { name: "Activity", href: "#", count: 0, current: true },
      {
        name: "Staff discussion",
        href: "#",
        count: 0,
        current: false,
        cond: "staff",
      },
      { name: "Attachments", href: "#", count: 0, current: false },
    ],
    role: "",
    addShare: false,
    lightbox: {
      visible: false,
      index: 0
    },
    files: [],
    upload: Upload
  }),
  mounted() {
    this.loadTicketData();
  },
  methods: {
    loadTicketData() {
      const formData = {
        comments: true,
        events: true,
        ticket: true,
        inbox: true,
        me: true,
        replies: true,
        role: true,
        staff: true,
      };

      /* Get every event from this ticket. */
      axios
        .get(
          `/api/inboxes/${this.$route.params.inboxId}/tickets/${this.$route.params.ticketInboxId}`,
          { params: formData }
        )
        .then((response) => {
          this.role = response.data.role;
          this.ticket = response.data.ticket;
          this.ticket.inbox = response.data.inbox;
          this.ticket.replies = response.data.replies;
          this.ticket.comments = [];
          this.staff = [];

          /* Get the guests for this inbox. */
          axios
            .get(`/api/inboxes/${this.$route.params.inboxId}/guests`)
            .then((response) => {
              this.ticket.inbox.guests = response.data.map((g) => ({
                id: g.id,
                name: g.first_name + " " + g.last_name,
                avatar: g.avatar_url,
              }));
            });

          if (this.isStaff(this.role, this.user)) {
            this.ticket.comments = response.data.comments.map((c) => {
              return {
                id: c.id,
                date: this.date(c.date_created),
                person: c.author
                  ? {
                      username: c.author.username,
                      name: c.author.first_name + " " + c.author.last_name,
                      href: "#",
                    }
                  : null,
                imageUrl: c.author.avatar_url,
                comment: c.content,
              };
            });
            this.staff = response.data.staff;
          }

          /* Setup the activities timeline. */
          this.ticket.activity = response.data.events.map((event) => {
            let type = "comment";

            if ("label" in event) type = "tags";
            if ("assignee" in event) type = "assignment";
            if ("new_status" in event) type = "status";

            return {
              id: event.id,
              date: this.date(event.date_created),
              datetime: event.date_created,
              person: event.initiator
                ? {
                    username: event.initiator.username,
                    name:
                      event.initiator.first_name +
                      " " +
                      event.initiator.last_name,
                    href: "#",
                  }
                : null,
              tags:
                type === "tags"
                  ? [
                      {
                        name: event.label.name,
                        href: "#",
                        color: event.label.color,
                      },
                    ]
                  : null,
              is_added: type === "tags" ? event.is_added : null,
              assigned: event.assignee
                ? {
                    username: event.assignee.username,
                    name:
                      event.assignee.first_name +
                      " " +
                      event.assignee.last_name,
                    href: "#",
                  }
                : null,
              status: event.new_status,
              type: type,
            };
          });

          /* Add the replies to the activities timeline. */
          this.ticket.activity.push(
            ...response.data.replies.map((reply) => {
              const helpful = reply.helpful.find(
                (h) => h.user === this.user.id
              );

              return {
                id: reply.id,
                date: this.date(reply.date_created),
                datetime: reply.date_created,
                person: {
                  username: reply.author.username,
                  name: reply.author.first_name + " " + reply.author.last_name,
                  href: "#",
                },
                helpful: helpful
                  ? helpful.is_helpful
                    ? "helpful"
                    : "notHelpful"
                  : undefined,
                imageUrl: reply.author.avatar_url,
                comment: reply.content,
                type: "comment",
              };
            })
          );

          /* Add the attachments to the activities timeline. */
          this.ticket.activity.push(
            ...response.data.ticket.attachments.map((attachment) => {
              return {
                id: attachment.id,
                date: this.date(attachment.date_created),
                datetime: attachment.date_created,
                person: {
                  name:
                    attachment.uploader.first_name +
                    " " +
                    attachment.uploader.last_name,
                  href: "#",
                },
                imageUrl: attachment.uploader.avatar_url,
                attachment: [
                  {
                    name: attachment.file.substring(
                      attachment.file.lastIndexOf("/") + 1,
                      attachment.file.lastIndexOf(".")
                    ),
                    extension: attachment.file.substring(
                      attachment.file.lastIndexOf(".") + 1
                    ),
                    size: attachment.file_size,
                    href: attachment.file,
                  },
                ],
                type: "attachment",
                visible: false,
                index: 0,
              };
            })
          );

          /* Sort the activities on date. */
          this.ticket.activity.sort((a, b) =>
            moment(a.datetime).diff(moment(b.datetime))
          );

          axios
            .get(`/api/inboxes/${this.$route.params.inboxId}/labels/all`)
            .then((response) => {
              this.ticket.inbox.labels = response.data;
            });

          /* Combine the same activities within 5 minutes of each other. */
          this.ticket.activity = this.combineActivities(
            this.ticket.activity,
            5
          );

          /* Update the numbers besides the tabs. */
          this.tabs.find((t) => t.name === "Activity").count =
            this.ticket.activity.filter((a) => a.type === "comment").length;
          this.tabs.find((t) => t.name === "Staff discussion").count =
            this.ticket.comments.length;
          this.tabs.find((t) => t.name === "Attachments").count =
            this.ticket.attachments.length;

          /* Hide too many system messages. Make sure the focus is on the comments. */
          this.ticket.activity = this.crampActivities(this.ticket.activity);

          /* Check list of tags. */
          this.ticket.inbox.labels = this.ticket.inbox.labels.map((l) => {
            if (l.name in this.ticket.labels.map((l) => l.name))
              l.selected = true;
            else l.selected = false;
            return l;
          });
        });
    },
    combineActivities(activities, time) {
      const newActivities = [];
      let lastActivity = null;

      activities.forEach((activity) => {
        if (lastActivity && lastActivity.type !== activity.type) {
          newActivities.push(lastActivity);
          lastActivity = activity;
        } else if (
          lastActivity &&
          moment(lastActivity.datetime).diff(moment(activity.datetime)) < time
        ) {
          if (
            lastActivity.type === "tags" &&
            lastActivity.is_added === activity.is_added &&
            lastActivity.person?.name === activity.person?.name
          )
            lastActivity.tags.push(activity.tags[0]);
          else if (
            lastActivity.type === "attachment" &&
            lastActivity.is_added === activity.is_added &&
            lastActivity.person?.name === activity.person?.name
          )
            lastActivity.attachment.push(activity.attachment[0]);
          else {
            newActivities.push(lastActivity);
            lastActivity = activity;
          }
        } else {
          lastActivity = activity;
        }
      });

      if (lastActivity) newActivities.push(lastActivity);

      return newActivities;
    },
    crampActivities(activities) {
      const newActivities = [];
      let groupActivities = [];

      activities.forEach((activity) => {
        if (activity && activity.type === "comment") {
          if (groupActivities.length === 1) {
            newActivities.push(groupActivities[0]);
            groupActivities = [];
          } else if (groupActivities.length > 1) {
            // newActivities.push({
            //   id: groupActivities[0].id,
            //   type: "group",
            //   activities: groupActivities,
            // });
            groupActivities = [];
          }
          newActivities.push(activity);
        } else {
          // groupActivities.push(activity);
        }
      });

      if (groupActivities.length === 1) {
        newActivities.push(groupActivities[0]);
      } else if (groupActivities.length > 1) {
        newActivities.push({
          id: groupActivities[0].id,
          type: "group",
          activities: groupActivities,
        });
      }

      return newActivities;
    },
    date(date) {
      return moment.parseZone(date).fromNow()
      // return moment.parseZone(date).calendar(null, {
      //   lastDay: "[Yesterday]",
      //   sameDay: "HH:mm",
      //   nextDay: "[Tomorrow]",
      //   lastWeek: "[Last] dddd",
      //   nextWeek: "dddd",
      //   sameElse: "L [at] HH:mm",
      // });
    },
    isStaff(role, user) {
      return (
        (role && (role === "AGENT" || role === "MANAGER")) ||
        (user && user.is_superuser)
      );
    },
    ticketStatus(status) {
      return status === "ASGD" || status === "CLSD" ? "closed" : "open";
    },
    makePrivate() {
      this.privateConfirmationModal = false;
      axios
        .put(
          `/api/inboxes/${this.$route.params.inboxId}/tickets/${this.$route.params.ticketInboxId}/private`
        )
        .then(() => {
          this.ticket.is_public = null;
          this.ticket.is_anonymous = null;
          this.ticket.publish_request_created = null;
          this.ticket.publish_request_initiator = null;
        });
    },
    requestPublish() {
      this.publishConfirmationModal = false;
      axios
        .put(
          `/api/inboxes/${this.$route.params.inboxId}/tickets/${this.$route.params.ticketInboxId}/request-publish`,
          {
            publish_request_initiator: this.user.id,
          }
        )
        .then((response) => {
          this.ticket.publish_request_initiator =
            response.data.publish_request_initiator;
          this.ticket.publish_request_created =
            response.data.publish_request_created;
        });
    },
    publishTicket() {
      axios
        .put(
          `/api/inboxes/${this.$route.params.inboxId}/tickets/${this.$route.params.ticketInboxId}/publish`,
          {
            is_public: moment().format(),
            is_anonymous: this.ticket.is_anonymous,
          }
        )
        .then((response) => {
          this.ticket.is_public = response.data.is_public;
          this.ticket.is_anonymous = response.data.is_anonymous;
        });
    },
    async updateSharedWith() {
      const formData = new FormData();
      this.ticket.shared_with.forEach((user) =>
        formData.append("shared_with", user.id)
      );

      await axios.put(
        `/api/inboxes/${this.$route.params.inboxId}/tickets/${this.$route.params.ticketInboxId}/shared`,
        formData
      );

      this.loadTicketData();
    },
    async updateLabels() {
      await axios.put(
        `/api/inboxes/${this.$route.params.inboxId}/tickets/${this.$route.params.ticketInboxId}/labels`,
        {
          labels: this.ticket.labels.map((label) => label.id),
        }
      );

      this.loadTicketData();
    },
    containsObject(list, id) {
      return list && list.some((e) => e.id === id);
    },
    toggleLabel(value) {
      // if (this.containsObject(this.ticket.labels, value.id)) {
      //   this.ticket.labels.splice(
      //     this.ticket.labels.findIndex((e) => e.id === value.id),
      //     1
      //   );
      // } else {
      //   this.ticket.labels.push(value);
      // }
      
      if (!this.containsObject(this.ticket.labels, value.id)) {
        this.ticket.labels = []
        this.ticket.labels.push(value)
      } else {
        this.ticket.labels = []
      }

      this.updateLabels()
    },
    readableBytes(bytes) {
      const sizes = ["Bytes", "KB", "MB", "GB", "TB"];
      if (bytes === 0) return "0 Byte";
      const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
      return Math.round(bytes / Math.pow(1024, i), 2) + " " + sizes[i];
    },
    submit () {
      const formData = new FormData()
      const { inboxId, ticketInboxId } = this.$route.params

      if (this.files.length == 0) return

      console.log(this.files)

      this.files.forEach(file => formData.append('files', file))

      axios.post(`/api/inboxes/${inboxId}/tickets/${ticketInboxId}/attachments`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then(() => {
        this.$emit('uploaded')
        this.$refs.upload.clear()
      }).catch(error => {
        if (error.response && error.response.status === 413) {
          this.errors = 'Filesize too large, max filesize is 25MB.'
        }
        this.$refs.upload.clear()
      })
    },
    setFiles (files) {
      this.files = files
      this.submit()
    },
    switchTab() {
      this.tabs.forEach((t) => (t.current = false));
    },
    updateAssignee(user) {
      const id =
        this.ticket?.assignee && this.ticket?.assignee.id === user.id
          ? []
          : user.id;
      const formData = new FormData();
      formData.append("assignee", id);
      axios
        .patch(
          `/api/inboxes/${this.$route.params.inboxId}/tickets/${this.$route.params.ticketInboxId}/assignee`,
          formData
        )
        .then((_) => {
          this.ticket.assignee = id === user.id ? user : undefined;
          this.loadTicketData();
        });
    },
    assignUser() {
      this.updateAssignee(this.user);
    },
    helpful(helpful, id) {
      const activity = this.ticket.activity.find((a) => a.id === id);

      const formData = new FormData();
      formData.append("comment", id);
      formData.append("user", this.user.id);
      formData.append("is_helpful", helpful === "helpful" ? true : false);

      if (helpful == undefined) {
        axios
          .delete(
            `/api/inboxes/${this.$route.params.inboxId}/tickets/${this.$route.params.ticketInboxId}/helpful/${id}`,
            formData
          )
          .then((_) => {
            this.loadTicketData();
          });
      } else if (activity.helpful == undefined) {
        axios
          .post(
            `/api/inboxes/${this.$route.params.inboxId}/tickets/${this.$route.params.ticketInboxId}/helpful/${id}`,
            formData
          )
          .then((_) => {
            this.loadTicketData();
          });
      } else {
        axios
          .put(
            `/api/inboxes/${this.$route.params.inboxId}/tickets/${this.$route.params.ticketInboxId}/helpful/${id}`,
            formData
          )
          .then((_) => {
            this.loadTicketData();
          });
      }
    },
    unfold(activity) {
      const index = this.ticket.activity.findIndex((a) => a.id === activity.id);
      this.ticket.activity.splice(index, 1, ...activity.activities);
    },
    listboxAlignment(e) {
      if (this.$refs[e].el == null) return
      
      setTimeout(() => {
        if (this.$refs[e].el == null) return
        if (this.$refs[e].el.getBoundingClientRect().right > window.innerWidth - 16) {
          this.$refs[e].el.style.right = 0
        }
      }, 10)
    }
  },
  computed: {
    ...mapState({
      user: (state) => state.user,
    }),
    guestsFiltered() {
      return this.ticket?.inbox?.guests
        ?.filter((g) => g.id !== this.user?.id)
        .filter(
          (g) => this.ticket?.shared_with.map((s) => s.id).indexOf(g.id) === -1
        );
    },
    isStaffOrAuthor() {
      return (
        this.isStaff(this.role, this.user) ||
        (this.user && this.ticket?.author?.id === this.user.id)
      );
    },
    attachments() {
      return this.ticket?.attachments || []
      // return this.ticket?.attachments?.filter((a) => 
      //   ['jpg', 'jpeg', 'png', 'gif'].includes(a.file.substring(a.file.lastIndexOf(".") + 1).toLowerCase())
      // );
    }
  },
};
</script>
