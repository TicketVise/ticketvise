<template>
  <!--  <div class="inline-block relative w-full">-->
  <!--    <select class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded leading-tight focus:outline-none cursor-pointer"-->
  <!--            v-on:input="updateValue($event.target.value)">-->
  <!--      <option :value="null">Choose assignee</option>-->
  <!--      <option :key="item.id" :selected="value != null && value.id === item.id" :value="item.id" v-for="item in values">-->
  <!--        {{item.first_name}} {{item.last_name}}-->
  <!--      </option>-->
  <!--    </select>-->

  <!--    <span class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">-->
  <!--            <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="none"-->
  <!--                 stroke="currentColor">-->
  <!--                <path d="M7 7l3-3 3 3m0 6l-3 3-3-3" stroke-width="1.5" stroke-linecap="round"-->
  <!--                      stroke-linejoin="round"/>-->
  <!--            </svg>-->
  <!--        </span>-->
  <!--  </div>-->
  <div class="space-y-1">
    <div class="relative">
                <span @click="open = !open" class="inline-block w-full rounded-md shadow-sm">
                    <button aria-expanded="true" aria-haspopup="listbox" aria-labelledby="listbox-label"
                            class="cursor-pointer relative w-full rounded-md border border-gray-300 bg-white pl-3 pr-10 py-2 text-left focus:outline-none transition ease-in-out duration-150 sm:text-sm sm:leading-5"
                            tabindex="-1"
                            type="button">
                        <div class="flex items-center space-x-3" v-if="assignee">
                            <avatar :source="assignee.avatar_url" class="w-6 h-6"></avatar>
                            <span class="block truncate">{{ assignee.first_name }} {{ assignee.last_name }}</span>
                        </div>
                        <div class="flex items-center space-x-3" v-else>
                            <span class="block truncate">Select Assignee</span>
                        </div>
                        <span class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
                            <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 20 20">
                                <path d="M7 7l3-3 3 3m0 6l-3 3-3-3" stroke-linecap="round" stroke-linejoin="round"
                                      stroke-width="1.5"/>
                            </svg>
                        </span>
                    </button>
                </span>

      <div class="absolute mt-1 w-full rounded-md bg-white shadow-lg z-50" v-if="open">
        <ul aria-activedescendant="listbox-item-3" aria-labelledby="listbox-label"
            class="max-h-56 rounded-md py-1 text-base leading-6 shadow-xs overflow-auto focus:outline-none sm:text-sm sm:leading-5"
            role="listbox"
            tabindex="-1">
          <li :key="item.id" :value="item.id" @click="submit(item)"
              class="text-gray-900 hover:text-white hover:bg-orange-400 cursor-pointer select-none relative py-2 pl-3 pr-9"
              id="listbox-item-0"
              role="option"
              v-for="item in staff">
            <div class="flex items-center space-x-3">
              <avatar :source="item.avatar_url" class="w-6 h-6 rounded-full"></avatar>
              <span :class="{ 'font-semibold': assignee === item }" class="font-normal block truncate">{{ item.first_name }} {{ item.last_name }}</span>
            </div>
            <span class="absolute inset-y-0 right-0 flex items-center pr-4" v-if="assignee === item">
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                <path clip-rule="evenodd"
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      fill-rule="evenodd"/>
              </svg>
            </span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
  import Avatar from "../Avatar";
  import axios from "axios";

  export default {
    name: "Dropdown",
    components: {Avatar},
    props: ["assignee", "staff"],
    data: () => ({
      open: false,
    }),
    methods: {
      submit(user) {
        this.value = user
        let formData = new FormData();
        formData.append("assignee", this.value.id);

        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

        axios.put("/api" + window.location.pathname + "/assignee", formData)
            .then(_ => {
              this.assignee = this.value
              this.$emit("input", this.assignee)

            });
        this.open = false
      },
    }
  }
</script>

<style scoped>

</style>
