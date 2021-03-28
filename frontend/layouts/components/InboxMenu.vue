<template>
  <div>
    <div class="flex md:hidden h-full">
      <div class="flex flex-col border-r justify-between">
        <div class="flex flex-col w-16 p-2 overflow-y-auto overflow-x-hidden">
          <router-link
            :to="`/inboxes/${$route.params.inboxId}/tickets`"
            exact
            class="text-gray-600 group flex items-center justify-center h-12 w-12 p-3 text-sm font-medium rounded-full focus:ring ring-primary"
            active-class="bg-gray-100 text-gray-900"
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
            :to="`/inboxes/${$route.params.inboxId}/forum`"
            exact
            class="text-gray-600 group flex items-center justify-center h-12 w-12 p-3 text-sm font-medium rounded-full focus:ring ring-primary"
            active-class="bg-gray-100 text-gray-900"
            title="Public questions"
          >
            <!-- Heroicon name: outline/view-grid -->
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
                d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"
              ></path>
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
            <hr class="border-t border-gray-200 my-2 mt-4" aria-hidden="true" />
            <router-link
              :to="'/inboxes/' + $route.params.inboxId + '/users'"
              exact
              class="text-gray-600 group flex items-center justify-center h-12 w-12 p-3 text-sm font-medium rounded-full focus:ring ring-primary"
              active-class="bg-gray-100 text-gray-900"
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
              :to="'/inboxes/' + $route.params.inboxId + '/statistics'"
              exact
              class="text-gray-600 group flex items-center justify-center h-12 w-12 p-3 text-sm font-medium rounded-full focus:ring ring-primary"
              active-class="bg-gray-100 text-gray-900"
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
              :to="'/inboxes/' + $route.params.inboxId + '/settings'"
              exact
              class="text-gray-600 group flex items-center justify-center h-12 w-12 p-3 text-sm font-medium rounded-full focus:ring ring-primary"
              active-class="bg-gray-100 text-gray-900"
              title="Settings"
            >
              <!-- Heroicon name: outline/calendar -->
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
        <div class="w-12 mx-auto border-t flex items-center justify-center">
          <div
            class="flex-shrink-0 flex items-center justify-center py-2"
          >
            <router-link to="/account" class="flex-shrink-0 w-full group block">
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
    <div class="hidden md:flex h-full">
      <div class="flex flex-col w-64">
        <!-- Sidebar component, swap this element with another sidebar if you like -->
        <div class="flex flex-col h-0 flex-1 border-r border-gray-200 bg-white">
          <div class="flex-1 flex flex-col py-4 overflow-y-auto">
            <!-- Inbox Header -->
            <div class="px-4">
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
              <div class="mt-1 flex flex-col space-y-1">
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
                  <div v-else class="h-5 w-24 bg-gray-200 rounded" />
                </div>
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
                  <span v-if="inbox">{{ inbox.inbox.code }}</span>
                  <div v-else class="h-5 w-24 bg-gray-200 rounded" />
                </div>
                <div class="pt-2 w-full">
                  <router-link
                    :to="'/inboxes/' + $route.params.inboxId + '/tickets/new'"
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
            <hr class="border-t border-gray-200 my-4" aria-hidden="true" />

            <nav class="flex-1 px-2 bg-white space-y-1">
              <router-link
                :to="`/inboxes/${$route.params.inboxId}/tickets`"
                exact
                class="text-gray-600 hover:bg-gray-50 hover:text-gray-900 group flex items-center px-2 py-2 text-sm font-medium rounded-md"
                active-class="bg-gray-100 text-gray-900"
              >
                <!-- Heroicon name: outline/home -->
                <svg
                  class="text-gray-400 mr-3 h-6 w-6"
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
                {{ is_staff ? "Overview" : "Your questions" }}
              </router-link>

              <router-link
                :to="`/inboxes/${$route.params.inboxId}/forum`"
                exact
                class="text-gray-600 hover:bg-gray-50 hover:text-gray-900 group flex items-center px-2 py-2 text-sm font-medium rounded-md"
                active-class="bg-gray-100 text-gray-900"
              >
                <!-- Heroicon name: outline/view-grid -->
                <svg
                  class="text-gray-400 mr-3 h-6 w-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"
                  ></path>
                </svg>
                Public questions
              </router-link>

              <div v-if="is_staff">
                <hr class="border-t border-gray-200 my-4" aria-hidden="true" />
                <h3 class="text-gray-600 text-xs pl-4 pb-1 font-bold uppercase">
                  Staff only
                </h3>
                <router-link
                  :to="'/inboxes/' + $route.params.inboxId + '/users'"
                  exact
                  class="text-gray-600 hover:bg-gray-50 hover:text-gray-900 group flex items-center px-2 py-2 text-sm font-medium rounded-md"
                  active-class="bg-gray-100 text-gray-900"
                >
                  <!-- Heroicon name: outline/users -->
                  <svg
                    class="text-gray-400 group-hover:text-gray-500 mr-3 h-6 w-6"
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
                  :to="'/inboxes/' + $route.params.inboxId + '/statistics'"
                  exact
                  class="text-gray-600 hover:bg-gray-50 hover:text-gray-900 group flex items-center px-2 py-2 text-sm font-medium rounded-md"
                  active-class="bg-gray-100 text-gray-900"
                >
                  <!-- Heroicon name: outline/chart-square-bar -->
                  <svg
                    class="text-gray-400 group-hover:text-gray-500 mr-3 h-6 w-6"
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
                  :to="'/inboxes/' + $route.params.inboxId + '/settings'"
                  exact
                  class="text-gray-600 hover:bg-gray-50 hover:text-gray-900 group flex items-center px-2 py-2 text-sm font-medium rounded-md"
                  active-class="bg-gray-100 text-gray-900"
                >
                  <!-- Heroicon name: outline/calendar -->
                  <svg
                    class="text-gray-400 group-hover:text-gray-500 mr-3 h-6 w-6"
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
              <div>
                <hr class="border-t border-gray-200 my-4" aria-hidden="true" />
                <h3 class="text-gray-600 text-xs pl-4 pb-1 font-bold uppercase">
                  Other inboxes
                </h3>
                <a
                  v-for="inbox in inboxes"
                  :key="inbox.inbox.id"
                  @click="$emit('goto', inbox.inbox.id)"
                  class="text-gray-400 hover:bg-gray-50 hover:text-gray-700 cursor-pointer group flex items-center px-2 py-2 text-sm font-medium rounded-md"
                >
                  <span class="truncate">{{ inbox.inbox.name }}</span>
                </a>
              </div>
            </nav>
          </div>
          <div class="flex-shrink-0 flex border-t border-gray-200 p-4">
            <router-link to="/account" class="flex-shrink-0 w-full group block">
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
                    class="text-sm font-medium text-gray-700 group-hover:text-gray-900"
                  >
                    {{ user.first_name }} {{ user.last_name }}
                  </p>
                  <p
                    class="text-xs font-medium text-gray-500 group-hover:text-gray-700"
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
</template>

<script>
import axios from "axios";

export default {
  name: "InboxMenu",
  props: {
    inbox: {
      required: false,
      type: Object,
    },
  },
  data: () => ({
    inboxes: []
  }),
  computed: {
    user() {
      return this.$store.state.user;
    },
    is_staff() {
      if (!this.inbox) {
        return false;
      }

      const role = this.inbox.role;
      return (
        (this.user && this.user.is_superuser) ||
        (role && (role === "AGENT" || role === "MANAGER"))
      );
    },
  },
  watch: {
    inbox: async function (newVal, oldVal) {
      const response = await axios.get("/api/me/inboxes");
      this.inboxes = [];
      for (let inbox of response.data) {
        if (inbox.inbox.id == newVal.inbox.id) continue;
        this.inboxes.push(inbox);
      }
    },
    $route: async function () {
      this.menu = false;
    },
  },
};
</script>
