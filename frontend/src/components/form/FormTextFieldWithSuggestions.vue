<!-- This example requires Tailwind CSS v2.0+ -->
<template>
  <div class="flex w-full">
    <div class="flex-grow">
      <div class="relative flex items-stretch flex-grow focus-within:z-10">
        <div class="relative w-full">
          <div
            class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
          >
            <UsersIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
          </div>
          <input
            @focus="open = true"
            @blur="open = false"
            v-model="inputField"
            type="text"
            name="user"
            id="user"
            class="focus:ring-primary focus:border-primary block w-full rounded-md pl-10 sm:text-sm border-gray-300"
            placeholder="John Doe"
            autocomplete="off"
          />
          <div
            v-show="open || selectedUser"
            class="absolute inset-y-0 right-0 pr-3 flex items-center"
          >
            <XMarkIcon
              @click="
                selectedUser = null;
                inputField = '';
              "
              class="h-5 w-5 text-gray-500"
              aria-hidden="true"
            />
          </div>
        </div>

        <ul
          v-show="open"
          class="absolute z-10 mt-10 w-full bg-white shadow-lg max-h-60 rounded-md py-1 text-base ring-1 ring-black ring-opacity-5 overflow-auto focus:outline-none sm:text-sm"
        >
          <li
            @mousedown.prevent
            @click="
              open = false;
              selectedUser = user;
              inputField = user.name;
            "
            v-for="user in dataFiltered.slice(0, 5)"
            :key="user.id"
            class="cursor-pointer flex items-center select-none relative py-2 pl-3 text-gray-900 hover:bg-gray-100 hover:text-gray-800"
          >
            <img
              :src="user.avatar"
              class="flex-shrink-0 h-6 w-6 rounded-full mr-3"
            />
            <span class="font-normal block truncate">{{ user.name }}</span>
          </li>
          <li
            v-if="dataFiltered?.length === 0"
            class="flex items-center select-none relative py-2 pl-3 text-gray-700"
          >
            <span class="font-normal block">No users found</span>
          </li>
        </ul>
      </div>
    </div>
    <span class="ml-3 flex">
      <button
        :disabled="!selectedUser"
        @click="
          $emit('add', selectedUser);
          selectedUser = null;
          inputField = '';
        "
        type="button"
        class="bg-white inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
      >
        <PlusIcon class="-ml-2 mr-1 h-5 w-5 text-gray-400" aria-hidden="true" />
        <span>Add</span>
      </button>
    </span>
  </div>
</template>

<script>
import { PlusIcon, XMarkIcon } from "@heroicons/vue/24/solid";
import { UsersIcon } from "@heroicons/vue/24/outline";

export default {
  components: {
    UsersIcon,
    PlusIcon,
    XMarkIcon,
  },
  props: {
    data: {
      required: true,
      type: Array,
    },
    emptyLabel: {
      required: false,
      type: String,
    },
  },
  data: () => ({
    open: false,
    inputField: "",
    selectedUser: null,
  }),
  computed: {
    dataFiltered() {
      if (this.inputField) {
        return this.data.filter(
          (user) =>
            user.name?.toLowerCase().indexOf(this.inputField?.toLowerCase()) >
            -1
        );
      }

      return this.data;
    },
  },
};
</script>
