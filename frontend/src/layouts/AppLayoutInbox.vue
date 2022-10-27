<template>
  <div class="h-screen flex flex-col">
    <!-- TicketVise Header -->
    <header class="bg-gray-800 dark:border-b dark:border-white">
      <div class="w-full px-4">
        <div class="relative flex flex-wrap items-center justify-between">
          <div class="flex items-center">
            <!-- Logo -->
            <div class="left-0 py-4 flex-shrink-0">
              <router-link to="/" class="flex items-center">
                <img class="h-8 w-auto" :src="logo" alt="TicketVise"/>
                <span class="text-2xl ml-2 text-white">Ticket</span>
                <span class="text-2xl text-primary font-bold">Vise</span>
              </router-link>
            </div>
            <div class="block ml-4 sm:ml-10">
              <div class="flex space-x-4">
                <router-link
                  to="/dashboard"
                  class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 focus:outline-none focus:text-white focus:bg-gray-700"
                  active-class="text-white bg-gray-900"
                >
                  Dashboard
                </router-link>
                <router-link
                  v-if="user.is_superuser"
                  to="/admin"
                  class="hidden sm:block px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 focus:outline-none focus:text-white focus:bg-gray-700"
                  active-class="text-gray-100 bg-gray-800"
                >
                  Admin
                </router-link>
              </div>
            </div>
          </div>

          <!-- Right section on desktop -->
          <div class="flex lg:ml-4 lg:items-center py-4 pr-0.5">
            <button type="button"
                    class="inline-flex items-center justify-center py-1 px-4 border border-transparent rounded-md shadow-sm text-white bg-primary hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 mr-4 space-x-2"
                    aria-label="Fullscreen" @click="openInTab()" v-if="isFramed()">
                    <span>New Tab</span>
                    <ExternalLinkIcon class="h-5 w-5" />
            </button>

            <router-link
              to="/notifications"
              type="button"
              class="flex-shrink-0 p-1 text-gray-200 rounded-full hover:text-white hover:bg-white hover:bg-opacity-10 focus:outline-none focus:ring-2 focus:ring-white"
            >
              <span class="sr-only">View notifications</span>
              <BellIcon class="h-6 w-6" aria-hidden="true"/>
            </router-link>

            <!-- Profile dropdown -->
            <Menu as="div" class="ml-4 relative flex-shrink-0">
              <div>
                <MenuButton
                  class="bg-white rounded-full flex text-sm ring-2 ring-white ring-opacity-20 focus:outline-none focus:ring-opacity-100"
                >
                  <span class="sr-only">Open user menu</span>
                  <img
                    class="h-8 w-8 rounded-full"
                    :src="user.avatar_url"
                    alt=""
                  />
                </MenuButton>
              </div>
              <transition
                leave-active-class="transition ease-in duration-75"
                leave-from-class="transform opacity-100 scale-100"
                leave-to-class="transform opacity-0 scale-95"
              >
                <MenuItems
                  class="origin-top-right z-40 absolute -right-2 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none"
                >
                  <MenuItem v-slot="{ active }">
                    <router-link to="/account"
                                 :class="[active ? 'bg-gray-100' : '', 'block px-4 py-2 text-sm text-gray-700']">Your
                      profile
                    </router-link>
                  </MenuItem>
                  <MenuItem v-slot="{ active }">
                    <a href="#" @click="logout()"
                       :class="[active ? 'bg-gray-100' : '', 'block px-4 py-2 text-sm text-gray-700']">Sign out</a>
                  </MenuItem>
                </MenuItems>
              </transition>
            </Menu>
          </div>
        </div>
      </div>
    </header>

    <div class="flex overflow-hidden bg-white dark:bg-gray-800 h-full">
      <!-- Static sidebar for desktop -->
      <div class="flex flex-shrink-0">
        <div class="flex flex-col border-r border-gray-200 bg-white dark:bg-gray-900">
          <!-- Sidebar component, swap this element with another sidebar if you like -->
          <div class="flex md:hidden h-full">
            <div class="flex flex-col justify-between">
              <div
                class="flex flex-col w-16 p-2 overflow-y-auto overflow-x-hidden"
              >
                <router-link
                  :to="`/inboxes/${$route.params.inboxId}/tickets`"
                  exact
                  class="text-gray-600 group flex items-center justify-center h-12 w-12 p-3 text-sm font-medium rounded-full focus:ring ring-primary"
                  active-class="bg-gray-100 text-gray-900 dark:bg-gray-800 dark:text-gray-700"
                  :title="is_staff ? 'Overview' : 'Your questions'"
                >
                  <!-- Heroicon name: outline/home -->
                  <svg
                    class="text-gray-400 h-6 w-6"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
                    />
                  </svg>
                </router-link>

                <router-link
                  :to="`/inboxes/${$route.params.inboxId}/public`"
                  exact
                  class="text-gray-600 group flex items-center justify-center h-12 w-12 p-3 text-sm font-medium rounded-full focus:ring ring-primary"
                  active-class="bg-gray-100 text-gray-900 dark:bg-gray-800 dark:text-gray-700"
                  title="Public questions"
                >
                  <!-- Heroicon name: outline/globe -->
                  <svg class="text-gray-400 h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                       stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </router-link>

                <router-link
                  :to="'/inboxes/' + $route.params.inboxId + '/tickets/new'"
                  exact
                  type="button"
                  class="inline-flex w-10 h-10 m-1 items-center justify-center p-2 border border-transparent rounded-full shadow-sm text-white bg-primary hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500"
                >
                  <!-- Heroicon name: solid/plus -->
                  <svg
                    class="w-6 h-6"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                    ></path>
                  </svg>
                </router-link>

                <div v-if="is_staff">
                  <hr
                    class="border-t border-gray-200 my-2 mt-4"
                    aria-hidden="true"
                  />

                  <router-link
                    :to="'/inboxes/' + $route.params.inboxId + '/users'"
                    exact
                    class="text-gray-600 group flex items-center justify-center h-12 w-12 p-3 text-sm font-medium rounded-full focus:ring ring-primary"
                    active-class="bg-gray-100 text-gray-900 dark:bg-gray-800 dark:text-gray-700"
                    title="Users"
                  >
                    <!-- Heroicon name: outline/users -->
                    <svg
                      class="text-gray-400 h-6 w-6"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      aria-hidden="true"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
                      />
                    </svg>
                  </router-link>

                  <router-link
                    :to="'/inboxes/' + $route.params.inboxId + '/labels'"
                    exact
                    class="text-gray-600 group flex items-center justify-center h-12 w-12 p-3 text-sm font-medium rounded-full focus:ring ring-primary"
                    active-class="bg-gray-100 text-gray-900 dark:bg-gray-800 dark:text-gray-700"
                    title="Insights"
                  >
                    <!-- Heroicon name: outline/bookmark -->
                    <svg xmlns="http://www.w3.org/2000/svg" class="text-gray-400 h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                    </svg>
                  </router-link>

                  <router-link
                    :to="'/inboxes/' + $route.params.inboxId + '/insights'"
                    exact
                    class="text-gray-600 group flex items-center justify-center h-12 w-12 p-3 text-sm font-medium rounded-full focus:ring ring-primary"
                    active-class="bg-gray-100 text-gray-900 dark:bg-gray-800 dark:text-gray-700"
                    title="Insights"
                  >
                    <!-- Heroicon name: outline/chart-square-bar -->
                    <svg
                      class="text-gray-400 h-6 w-6"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                      ></path>
                    </svg>
                  </router-link>

                  <router-link
                    :to="'/inboxes/' + $route.params.inboxId + '/automation'"
                    exact
                    class="text-gray-600 group flex items-center justify-center h-12 w-12 p-3 text-sm font-medium rounded-full focus:ring ring-primary"
                    active-class="bg-gray-100 text-gray-900 dark:bg-gray-800 dark:text-gray-700"
                    title="Insights"
                  >
                    <svg
                      class="text-gray-400 h-6 w-6"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
                      ></path>
                    </svg>
                  </router-link>

                  <router-link
                    :to="'/inboxes/' + $route.params.inboxId + '/agents'"
                    exact
                    class="text-gray-600 group flex items-center justify-center h-12 w-12 p-3 text-sm font-medium rounded-full focus:ring ring-primary"
                    active-class="bg-gray-100 text-gray-900 dark:bg-gray-800 dark:text-gray-700"
                    title="Agents"
                  >


                    <svg xmlns="http://www.w3.org/2000/svg" class="text-gray-400 h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                  </router-link>

                  <router-link
                    :to="'/inboxes/' + $route.params.inboxId + '/settings'"
                    exact
                    class="text-gray-600 group flex items-center justify-center h-12 w-12 p-3 text-sm font-medium rounded-full focus:ring ring-primary"
                    active-class="bg-gray-100 text-gray-900 dark:bg-gray-800 dark:text-gray-700"
                    title="Settings"
                  >
                    <!-- Heroicon name: outline/settings -->
                    <svg
                      class="text-gray-400 h-6 w-6"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
                      ></path>
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                      ></path>
                    </svg>
                  </router-link>
                </div>
              </div>
              <div
                class="w-12 mx-auto border-t flex items-center justify-center"
              >
                <div
                  class="flex-shrink-0 flex items-center justify-center py-2"
                >
                  <router-link
                    to="/account"
                    class="flex-shrink-0 w-full group block"
                  >
                    <div class="flex items-center">
                      <img
                        class="inline-block h-10 w-10 rounded-full"
                        :src="user.avatar_url"
                        alt=""
                      />
                    </div>
                  </router-link>
                </div>
              </div>
            </div>
          </div>

          <!-- Static sidebar for desktop -->
          <div class="hidden md:flex h-full dark:bg-gray-900">
            <div class="flex flex-col w-64">
              <!-- Sidebar component, swap this element with another sidebar if you like -->
              <div class="flex flex-col h-0 flex-1">
                <div class="flex-1 flex flex-col py-4 overflow-y-auto">
                  <!-- Inbox Header -->
                  <div class="px-4">
                    <h2
                      v-if="inbox"
                      class="font-bold leading-6 text-gray-900 dark:text-white text-lg truncate"
                    >
                      {{ inbox.inbox.name }}
                    </h2>
                    <div
                      v-else
                      class="h-7 w-full max-w-screen-sm bg-gray-200 rounded"
                    />
                    <div class="mt-1 flex flex-col space-y-1">
                      <div class="flex items-center text-xs text-gray-500 dark:text-gray-200">
                        <!-- Heroicon name: user -->
                        <svg
                          class="w-4 h-4 mr-1"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                          xmlns="http://www.w3.org/2000/svg"
                        >
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                          ></path>
                        </svg>
                        <span class="w-full truncate" v-if="inbox">
                          {{ inbox.inbox.coordinator.first_name }}
                          {{ inbox.inbox.coordinator.last_name }}
                        </span>
                        <div v-else class="h-5 w-24 bg-gray-200 rounded"/>
                      </div>
                      <div class="flex items-center text-xs text-gray-500 dark:text-gray-200">
                        <!-- Heroicon name: code -->
                        <svg
                          class="w-4 h-4 mr-1"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                          xmlns="http://www.w3.org/2000/svg"
                        >
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"
                          ></path>
                        </svg>
                        <span v-if="inbox">{{ inbox.inbox.lti_context_label }}</span>
                        <div v-else class="h-5 w-24 bg-gray-200 rounded"/>
                      </div>
                      <div class="pt-2 w-full">
                        <router-link
                          :to="
                            '/inboxes/' + $route.params.inboxId + '/tickets/new'
                          "
                          exact
                          type="button"
                          class="inline-flex items-center justify-center w-full px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-orange-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
                        >
                          <!-- Heroicon name: add -->
                          <svg
                            class="-ml-1 mr-2 h-5 w-5"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                            xmlns="http://www.w3.org/2000/svg"
                          >
                            <path
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              stroke-width="2"
                              d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                            ></path>
                          </svg>
                          New Ticket
                        </router-link>
                      </div>
                    </div>
                  </div>
                  <hr
                    class="border-t border-gray-200 my-4"
                    aria-hidden="true"
                  />

                  <nav class="flex-1 px-2 bg-white dark:bg-gray-900 space-y-1">
                    <router-link
                      :to="`/inboxes/${$route.params.inboxId}/tickets`"
                      exact
                      class="text-gray-600 hover:bg-gray-50 hover:text-gray-900 dark:hover:bg-gray-700 dark:hover:text-white group flex items-center px-2 py-2 text-sm font-medium rounded-md"
                      active-class="bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white"
                    >
                      <!-- Heroicon name: outline/home -->
                      <svg
                        class="text-gray-400 group-hover:text-gray-500 dark:group-hover:text-gray-400 mr-3 h-6 w-6"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        aria-hidden="true"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
                        />
                      </svg>
                      {{ is_staff ? 'Overview' : 'Your tickets' }}
                    </router-link>

                    <router-link
                      :to="`/inboxes/${$route.params.inboxId}/public`"
                      exact
                      class="text-gray-600 hover:bg-gray-50 hover:text-gray-900 dark:hover:bg-gray-700 dark:hover:text-white group flex items-center px-2 py-2 text-sm font-medium rounded-md"
                      active-class="bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white"
                    >
                      <!-- Heroicon name: outline/globe -->
                      <svg class="text-gray-400 group-hover:text-gray-500 dark:group-hover:text-gray-400 mr-3 h-6 w-6"
                           xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                      Public tickets
                    </router-link>

                    <div v-if="is_staff">
                      <hr
                        class="border-t border-gray-200 my-4"
                        aria-hidden="true"
                      />
                      <h3
                        class="text-gray-600 text-xs pl-4 pb-1 font-bold uppercase"
                      >
                        Staff only
                      </h3>
                      <div class="space-y-1">
                        <router-link
                          :to="'/inboxes/' + $route.params.inboxId + '/users'"
                          exact
                          class="text-gray-600 hover:bg-gray-50 hover:text-gray-900 dark:hover:bg-gray-700 dark:hover:text-white group flex items-center px-2 py-2 text-sm font-medium rounded-md"
                          active-class="bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white"
                        >
                          <!-- Heroicon name: outline/users -->
                          <svg
                            class="text-gray-400 group-hover:text-gray-500 dark:group-hover:text-gray-400 mr-3 h-6 w-6"
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                            aria-hidden="true"
                          >
                            <path
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              stroke-width="2"
                              d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
                            />
                          </svg>
                          Users
                        </router-link>

                        <router-link
                          :to="'/inboxes/' + $route.params.inboxId + '/labels'"
                          exact
                          class="text-gray-600 hover:bg-gray-50 hover:text-gray-900 dark:hover:bg-gray-700 dark:hover:text-white group flex items-center px-2 py-2 text-sm font-medium rounded-md"
                          active-class="bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white"
                        >
                          <!-- Heroicon name: outline/bookmark -->
                          <svg xmlns="http://www.w3.org/2000/svg" class="text-gray-400 group-hover:text-gray-500 dark:group-hover:text-gray-400 mr-3 h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                          </svg>
                          Labels
                        </router-link>

                        <router-link
                          :to="'/inboxes/' + $route.params.inboxId + '/insights'"
                          exact
                          class="text-gray-600 hover:bg-gray-50 hover:text-gray-900 dark:hover:bg-gray-700 dark:hover:text-white group flex items-center px-2 py-2 text-sm font-medium rounded-md"
                          active-class="bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white"
                        >
                          <!-- Heroicon name: outline/chart-square-bar -->
                          <svg
                            class="text-gray-400 group-hover:text-gray-500 dark:group-hover:text-gray-400 mr-3 h-6 w-6"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                            xmlns="http://www.w3.org/2000/svg"
                          >
                            <path
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              stroke-width="2"
                              d="M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                            ></path>
                          </svg>
                          Insights
                        </router-link>

                        <router-link
                          :to="
                            '/inboxes/' + $route.params.inboxId + '/automation'
                          "
                          exact
                          class="text-gray-600 hover:bg-gray-50 hover:text-gray-900 dark:hover:bg-gray-700 dark:hover:text-white group flex items-center px-2 py-2 text-sm font-medium rounded-md"
                          active-class="bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white"
                        >
                          <svg
                            class="text-gray-400 group-hover:text-gray-500 dark:group-hover:text-gray-400 mr-3 h-6 w-6"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                            xmlns="http://www.w3.org/2000/svg"
                          >
                            <path
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              stroke-width="2"
                              d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
                            ></path>
                          </svg>
                          Automation
                        </router-link>

                        <router-link
                          :to="'/inboxes/' + $route.params.inboxId + '/agents'"
                          exact
                          class="text-gray-600 hover:bg-gray-50 hover:text-gray-900 dark:hover:bg-gray-700 dark:hover:text-white group flex items-center px-2 py-2 text-sm font-medium rounded-md"
                          active-class="bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" class="text-gray-400 group-hover:text-gray-500 dark:group-hover:text-gray-400 mr-3 h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                          </svg>
                          Agents
                        </router-link>

                        <router-link
                          :to="'/inboxes/' + $route.params.inboxId + '/settings'"
                          exact
                          class="text-gray-600 hover:bg-gray-50 hover:text-gray-900 dark:hover:bg-gray-700 dark:hover:text-white group flex items-center px-2 py-2 text-sm font-medium rounded-md"
                          active-class="bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white"
                        >
                          <!-- Heroicon name: outline/calendar -->
                          <svg
                            class="text-gray-400 group-hover:text-gray-500 dark:group-hover:text-gray-400 mr-3 h-6 w-6"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                            xmlns="http://www.w3.org/2000/svg"
                          >
                            <path
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              stroke-width="2"
                              d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
                            ></path>
                            <path
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              stroke-width="2"
                              d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                            ></path>
                          </svg>
                          Settings
                        </router-link>
                      </div>
                    </div>
                    <!-- <div>
                      <hr class="border-t border-gray-200 my-4" aria-hidden="true" />
                      <h3 class="text-gray-600 text-xs pl-4 pb-1 font-bold uppercase">
                        Other inboxes
                      </h3>
                      <a
                        v-for="inbox in inboxes"
                        :key="inbox.inbox.id"
                        @click="goto(inbox.inbox.id)"
                        class="text-gray-400 hover:bg-gray-50 hover:text-gray-700 cursor-pointer group flex items-center px-2 py-2 text-sm font-medium rounded-md"
                      >
                        <span class="truncate">{{ inbox.inbox.name }}</span>
                      </a>
                    </div> -->
                  </nav>
                </div>
                <div class="flex-shrink-0 flex border-t border-gray-200 p-4">
                  <router-link
                    to="/account"
                    class="flex-shrink-0 w-full group block"
                  >
                    <div class="flex items-center">
                      <div>
                        <img
                          class="inline-block h-9 w-9 rounded-full"
                          :src="user.avatar_url"
                          alt=""
                        />
                      </div>
                      <div class="ml-3">
                        <p
                          class="text-sm font-medium text-gray-700 dark:text-gray-200 group-hover:text-gray-900 dark:group-hover:text-gray-400"
                        >
                          {{ user.first_name }} {{ user.last_name }}
                        </p>
                        <p
                          class="text-xs font-medium text-gray-500 dark:text-gray-400 group-hover:text-gray-700 dark:group-hover:text-gray-500"
                        >
                          View profile
                        </p>
                      </div>
                    </div>
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main column -->
      <div class="flex flex-col w-0 flex-1 overflow-hidden">
        <div class="flex flex-col md:hidden px-4 pt-2">
          <div class="flex justify-between items-center space-x-2">
            <h2
              v-if="inbox"
              class="font-bold leading-6 text-gray-900 text-lg truncate"
            >
              {{ inbox.inbox.name }}
            </h2>
            <div
              v-else
              class="h-7 w-full max-w-screen-sm bg-gray-200 rounded"
            />
          </div>

          <div class="flex space-x-2 mt-1">
            <div class="flex items-center text-xs text-gray-500">
              <!-- Heroicon name: code -->
              <svg
                class="w-4 h-4 mr-1"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"
                ></path>
              </svg>
              <span v-if="inbox">{{ inbox.inbox.lti_context_label }}</span>
              <div v-else class="h-5 w-24 bg-gray-200 rounded"/>
            </div>
            <div class="flex items-center text-xs text-gray-500">
              <!-- Heroicon name: user -->
              <svg
                class="w-4 h-4 mr-1"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                ></path>
              </svg>
              <span class="w-full truncate" v-if="inbox"
              >{{ inbox.inbox.coordinator.first_name }}
                {{ inbox.inbox.coordinator.last_name }}</span
              >
              <div v-else class="h-5 w-24 bg-gray-200 rounded"/>
            </div>
          </div>
        </div>

        <hr
          class="md:hidden border-t border-gray-200 mt-2"
          aria-hidden="true"
        />

        <main
          class="flex-1 relative overflow-hidden focus:outline-none flex flex-col"
        >
          <slot/>
        </main>
      </div>
    </div>
  </div>

  <getting-started
    @update="user.give_introduction = false"
    v-if="is_staff && user && user.give_introduction"
  />
  <develop-panel v-if="development"/>
</template>

<script>
import axios from 'axios'
import store from '@/store'
import { mapState } from 'vuex'

import GettingStarted from '@/components/onboarding/GettingStarted.vue'
import DevelopPanel from '@/components/devpanel/DevelopPanel.vue'

import {
  Menu,
  MenuButton,
  MenuItem,
  MenuItems
} from '@headlessui/vue'
import {
  BellIcon,
  ExternalLinkIcon
} from '@heroicons/vue/outline'

import logo from '@/assets/logo/logo.svg'

export default {
  components: {
    BellIcon,
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    ExternalLinkIcon,
    GettingStarted,
    DevelopPanel
  },
  setup () {
    return {
      logo
    }
  },
  data: () => ({
    inboxes: [],
    inbox: null,
    side: false
  }),
  async mounted () {
    const response = await axios.get(
      `/api/me/inboxes/${ this.$route.params.inboxId }`
    )
    this.inbox = response.data
  },
  methods: {
    async goto (index) {
      this.$router.push('/inboxes/' + index + '/tickets')
      const response = await axios.get(
        `/api/me/inboxes/${ this.$route.params.inboxId }`
      )
      this.inbox = response.data
    },
    logout () {
      this.$store.dispatch('logout')
    },
    isFramed () {
      return window.self !== window.top
    },
    openInTab () {
      const url = new URL(window.location.href)
      url.searchParams.append('token', store.state.token)
      window.open(url.href, '_blank')
    }
  },
  computed: {
    ...mapState({
      user: state => state.user
    }),
    is_staff () {
      if (!this.inbox) {
        return false
      }

      const role = this.inbox.role
      return (
        (this.user && this.user.is_superuser) ||
        (role && (role === 'AGENT' || role === 'MANAGER'))
      )
    },
    development: () => import.meta.env.DEV
  },
  watch: {
    inbox: async function (newVal) {
      const response = await axios.get('/api/me/inboxes')
      this.inboxes = []
      for (const inbox of response.data) {
        if (inbox.inbox.id === newVal.inbox.id) continue
        this.inboxes.push(inbox)
      }
    },
    $route: async function () {
      this.menu = false
    }
  }
}
</script>
