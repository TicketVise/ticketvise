<template>
  <div class="rounded-md border hover:border-gray-300">
    <div v-if="!open" @click="open = true" class="py-3 px-4 flex space-x-2 items-center cursor-pointer rounded-md hover:bg-gray-50">
      <i class="h-4 w-4 rounded bg-gray-600"></i>
      <span class="font-medium">{{ selected[1] }}</span>
      <span v-if="selected[0] === 'fixed'" class="flex items-center">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-4 w-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M14 5l7 7m0 0l-7 7m7-7H3"
          />
        </svg>
        <img
          :src="fixed_user?.avatar_url"
          alt=""
          class="mx-2 flex-shrink-0 h-6 w-6 rounded-full"
        />
        <span class="block truncate text-gray-800">{{
          fixed_user?.first_name + " " + fixed_user?.last_name
        }}</span>
      </span>
    </div>
    <div v-else class="py-3 px-4 space-y-2">
      <div class="flex justify-between w-full">
        <span class="font-medium">Default ticket assignment</span>
        <x-icon @click="cancel()" class="h-4 w-4 cursor-pointer" />
      </div>
      <div class="space-y-2">
        <div>
          <label
            id="listbox-label"
            class="block text-sm leading-5 font-medium text-primary"
          >
            Scheduling Algorithm
          </label>
          <div class="relative">
            <span
              class="inline-block w-full rounded-md"
              @click="dropdown_algorithm = !dropdown_algorithm"
            >
              <button
                type="button"
                aria-haspopup="listbox"
                aria-expanded="true"
                aria-labelledby="listbox-label"
                class="cursor-pointer relative w-full rounded-md border border-gray-300 bg-white pl-3 pr-10 py-2 text-left focus:outline-none focus:shadow-outline-primary focus:border-primary-300 transition ease-in-out duration-150 sm:text-sm sm:leading-5"
              >
                <div class="flex items-center space-x-3">
                  <span class="block truncate text-gray-800">{{
                    selected[1]
                  }}</span>
                </div>
                <span
                  class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none"
                >
                  <svg
                    class="h-5 w-5 text-gray-400"
                    viewBox="0 0 20 20"
                    fill="none"
                    stroke="currentColor"
                  >
                    <path
                      d="M7 7l3-3 3 3m0 6l-3 3-3-3"
                      stroke-width="1.5"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                  </svg>
                </span>
              </button>
            </span>

            <!-- Select popover, show/hide based on select state. -->
            <div
              class="absolute mt-1 w-full rounded-md bg-white shadow-lg z-10"
              v-if="dropdown_algorithm"
            >
              <ul
                tabindex="-1"
                role="listbox"
                aria-labelledby="listbox-label"
                aria-activedescendant="listbox-item-3"
                class="max-h-56 rounded-md py-1 text-base leading-6 shadow-xs overflow-auto focus:outline-none sm:text-sm sm:leading-5"
              >
                <li
                  id="listbox-item-0"
                  role="option"
                  v-for="item in scheduling_options"
                  :key="item[0]"
                  class="text-gray-900 cursor-pointer select-none relative py-2 pl-3 pr-9 hover:text-white hover:bg-primary"
                  :class="{ 'bg-orange-200': item[0] == selected[0] }"
                  @click="
                    selected = item;
                    dropdown_algorithm = false;
                  "
                >
                  <div class="flex items-center space-x-3">
                    <span
                      class="font-normal block truncate"
                      :class="{ 'font-semibold': item[0] == selected[0] }"
                      >{{ item[1] }}</span
                    >
                  </div>
                  <span
                    class="absolute inset-y-0 right-0 flex items-center pr-4"
                    v-if="item[0] == selected[0]"
                  >
                    <svg
                      class="h-5 w-5 text-orange-600"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clip-rule="evenodd"
                      />
                    </svg>
                  </span>
                </li>
              </ul>
            </div>

            <label
              v-if="selected[0] === 'fixed'"
              class="block text-sm leading-5 font-medium text-primary mt-2"
            >
              Fixed Assignment User
            </label>
            <!-- Show user dropdown when 'Fixed' is selected -->
            <span
              v-if="selected[0] === 'fixed'"
              class="inline-block w-full rounded-md"
              @click="dropdown_user = !dropdown_user"
            >
              <button
                type="button"
                aria-haspopup="listbox"
                aria-expanded="true"
                class="cursor-pointer relative w-full rounded-md border border-gray-300 bg-white pl-3 pr-10 py-2 text-left focus:outline-none focus:shadow-outline-primary focus:border-primary-300 transition ease-in-out duration-150 sm:text-sm sm:leading-5"
              >
                <div class="flex items-center space-x-3">
                  <img
                    :src="fixed_user?.avatar_url"
                    alt=""
                    class="flex-shrink-0 h-6 w-6 rounded-full"
                  />
                  <span class="block truncate text-gray-800">{{
                    fixed_user?.first_name + " " + fixed_user?.last_name
                  }}</span>
                </div>
                <span
                  class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none"
                >
                  <svg
                    class="h-5 w-5 text-gray-400"
                    viewBox="0 0 20 20"
                    fill="none"
                    stroke="currentColor"
                  >
                    <path
                      d="M7 7l3-3 3 3m0 6l-3 3-3-3"
                      stroke-width="1.5"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                  </svg>
                </span>
              </button>
            </span>

            <!-- Select popover, show/hide based on select state. -->
            <div
              class="absolute mt-1 w-full rounded-md bg-white shadow-lg z-10"
              v-if="dropdown_user && selected[0] === 'fixed'"
            >
              <ul
                tabindex="-1"
                role="listbox"
                aria-labelledby="listbox-label"
                aria-activedescendant="listbox-item-3"
                class="max-h-56 rounded-md py-1 text-base leading-6 shadow-xs overflow-auto focus:outline-none sm:text-sm sm:leading-5"
              >
                <li
                  id="listbox-item-0"
                  role="option"
                  v-for="user in staff"
                  :key="user.id"
                  class="text-gray-900 cursor-pointer select-none relative py-2 pl-3 pr-9 hover:text-white hover:bg-primary"
                  :class="{ 'bg-orange-200': user.id == fixed_user.id }"
                  @click="
                    fixed_user = user;
                    dropdown_user = false;
                  "
                >
                  <div class="flex items-center space-x-3">
                    <img
                      :src="user.avatar_url"
                      alt=""
                      class="flex-shrink-0 h-6 w-6 rounded-full"
                    />
                    <span
                      class="font-normal block truncate"
                      :class="{ 'font-semibold': user.id == fixed_user.id }"
                      >{{ user.first_name + " " + user.last_name }}</span
                    >
                  </div>
                  <span
                    class="absolute inset-y-0 right-0 flex items-center pr-4"
                    v-if="user.id == fixed_user.id"
                  >
                    <svg
                      class="h-5 w-5 text-orange-600"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clip-rule="evenodd"
                      />
                    </svg>
                  </span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Divider -->
        <div class="w-full border-b my-2"></div>

        <!-- Buttons -->
        <div class="flex justify-end space-x-2">
          <button
            @click="cancel"
            class="rounded border px-4 py-2 focus:outline-none hover:bg-gray-100"
          >
            Cancel
          </button>
          <button
            @click="save"
            class="rounded border px-4 py-2 border-green-400 bg-green-300 focus:outline-none hover:bg-green-200"
          >
            Save
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

import { XMarkIcon } from "@heroicons/vue/24/solid";

export default {
  components: { XMarkIcon },
  data: () => ({
    open: false,
    dropdown_algorithm: false,
    dropdown_user: false,
    selected: [],
    fixed_user: null,
    inbox: null,
    scheduling_options: [],
    staff: [],
  }),
  async mounted() {
    this.getInbox();
  },
  methods: {
    away() {
      this.dropdown_algorithm = false;
    },
    cancel() {
      this.getInbox();
      this.open = false;
    },
    async getInbox() {
      await axios
        .get(`/api/inboxes/${this.$route.params.inboxId}/settings`)
        .then((response) => {
          this.inbox = response.data.inbox;
          this.scheduling_options = response.data.scheduling_options;
          this.scheduling_options.push(["nothing", "Nothing"]);
          this.selected = this.scheduling_options.find(
            (item) => item[0] === this.inbox.scheduling_algorithm
          );

          if (
            this.inbox.scheduling_algorithm === "fixed" &&
            !this.inbox.fixed_scheduling_assignee
          ) {
            this.selected = ["nothing", "Nothing"];
          }
        });

      await axios
        .get(`/api/inboxes/${this.$route.params.inboxId}/staff`)
        .then((response) => {
          this.staff = response.data;
          this.fixed_user = this.staff[0];

          if (
            this.selected[0] === "fixed" &&
            this.inbox.fixed_scheduling_assignee
          ) {
            this.fixed_user =
              this.staff.find(
                (item) => item.id === this.inbox.fixed_scheduling_assignee
              ) || this.staff[0];
          }
        });
    },
    save() {
      axios.defaults.xsrfCookieName = "csrftoken";
      axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

      const formData = new FormData();
      const config = {
        headers: { "content-type": "multipart/form-data" },
      };

      for (const key in this.inbox) {
        if (key === "scheduling_algorithm") {
          if (this.selected[0] === "nothing") {
            formData.append(key, "fixed");
            formData.append("fixed_scheduling_assignee", null);
            continue;
          }
          formData.append(key, this.selected[0]);

          if (this.selected[0] === "fixed") {
            formData.append("fixed_scheduling_assignee", this.fixed_user.id);
          }
        } else if (key === "image") {
          continue;
        } else if (key !== "fixed_scheduling_assignee") {
          formData.append(key, this.inbox[key]);
        }
      }

      axios
        .put(
          `/api/inboxes/${this.$route.params.inboxId}/settings`,
          formData,
          config
        )
        .then(() => {
          this.open = false;

          this.getInbox();
        });
    },
  },
};
</script>
