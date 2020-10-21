<template>
  <div class="container mx-auto lg:px-4 pb-4">
    <search-bar v-model="query" v-on:input="search" class="flex-grow px-2" />

    <div class="flex flex-col">
      <div class="-my-2 py-2 overflow-x-auto px-2 sm:-mx-6 sm:px-6 lg:-mx-8 lg:px-8">
        <div
            class="align-middle inline-block min-w-full sm:shadow overflow-hidden sm:rounded-lg border-b border-gray-200">
          <table class="min-w-full">
            <thead>
            <tr>
              <th class="px-6 py-3 border-b border-gray-200 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                Name
              </th>
              <th class="px-6 py-3 border-b border-gray-200 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                Username
              </th>
              <th class="px-6 py-3 border-b border-gray-200 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th class="px-6 py-3 border-b border-gray-200 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                Role
              </th>
              <th class="px-6 py-3 border-b border-gray-200 bg-gray-50"></th>
            </tr>
            </thead>
            <tbody class="bg-white">

            <tr v-for="inboxUser in page.results" v-if="page">
              <td class="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10">
                    <img class="h-10 w-10 rounded-full" :src="inboxUser.user.avatar_url" alt=""/>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm leading-5 font-medium text-gray-900">
                      {{ inboxUser.user.get_full_name }}
                    </div>
                    <div class="text-sm leading-5 text-gray-500">{{ inboxUser.user.email }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
                <div class="text-sm leading-5 text-gray-900">@{{ inboxUser.user.username }}</div>
              </td>
              <td class="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
                <span v-if="inboxUser.user.is_active"
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                  Active
                </span>
                <span v-else
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">
                  Inactive
                </span>
              </td>
              <td class="px-6 py-4 whitespace-no-wrap border-b border-gray-200 text-sm leading-5 text-gray-500">
                {{ inboxUser.role }}
              </td>
              <td class="px-6 py-4 whitespace-no-wrap text-right border-b border-gray-200 text-sm leading-5 font-medium">
                <a href="#" class="text-indigo-600 hover:text-indigo-900">Edit</a>
              </td>
            </tr>
            </tbody>
          </table>
<!--          <div class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">-->
<!--            <div class="flex-1 flex items-center justify-between">-->
<!--              <div>-->
<!--                <p class="text-sm leading-5 text-gray-700">-->
<!--                  Showing-->
<!--                  <span class="font-medium">{{ index_start }}</span>-->
<!--                  to-->
<!--                  <span class="font-medium">{{ index_end }}</span>-->
<!--                  of-->
<!--                  <span class="font-medium">{{ total_count }}</span>-->
<!--                  results-->
<!--                </p>-->
<!--              </div>-->
<!--              <div>-->
<!--                <nav class="relative z-0 inline-flex shadow-sm">-->
<!--                  {% if inbox_users.has_previous %}-->
<!--                  <a href="?page=1&q={{ request.GET.q }}"-->
<!--                     class="-ml-px relative inline-flex items-center rounded-l-md px-4 py-2 border border-gray-300 bg-white text-sm leading-5 font-medium text-gray-700 hover:text-gray-500 focus:z-10 focus:outline-none focus:border-blue-300 focus:shadow-outline-blue active:bg-gray-100 active:text-gray-700 transition ease-in-out duration-150">-->
<!--                    1-->
<!--                  </a>-->
<!--                  <span-->
<!--                      class="-ml-px relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm leading-5 font-medium text-gray-700">-->
<!--                    ...-->
<!--                  </span>-->
<!--                  <a href="?page={{ inbox_users.previous_page_number }}&q={{ request.GET.q }}"-->
<!--                     class="-ml-px relative inline-flex items-center {% if not inbox_users.has_previous %} rounded-l-md {% endif %} px-2 py-2 border border-gray-300 bg-white text-sm leading-5 font-medium text-gray-500 hover:text-gray-400 focus:z-10 focus:outline-none focus:border-blue-300 focus:shadow-outline-blue active:bg-gray-100 active:text-gray-500 transition ease-in-out duration-150"-->
<!--                     aria-label="Previous">-->
<!--                    <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">-->
<!--                      <path fill-rule="evenodd"-->
<!--                            d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"-->
<!--                            clip-rule="evenodd"/>-->
<!--                    </svg>-->
<!--                  </a>-->
<!--                  {% endif %}-->
<!--                  <span-->
<!--                      class="-ml-px relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm leading-5 font-medium text-gray-700">-->
<!--                    {{ inbox_users.number }}-->
<!--                  </span>-->
<!--                  {% if inbox_users.has_next %}-->
<!--                  <a href="?page={{ inbox_users.next_page_number }}&q={{ request.GET.q }}"-->
<!--                     class="-ml-px relative inline-flex items-center {% if not inbox_users.has_next %} rounded-r-md {% endif %} px-2 py-2 border border-gray-300 bg-white text-sm leading-5 font-medium text-gray-500 hover:text-gray-400 focus:z-10 focus:outline-none focus:border-blue-300 focus:shadow-outline-blue active:bg-gray-100 active:text-gray-500 transition ease-in-out duration-150"-->
<!--                     aria-label="Next">-->
<!--                    <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">-->
<!--                      <path fill-rule="evenodd"-->
<!--                            d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"-->
<!--                            clip-rule="evenodd"/>-->
<!--                    </svg>-->
<!--                  </a>-->
<!--                  <span-->
<!--                      class="-ml-px relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm leading-5 font-medium text-gray-700">-->
<!--                    ...-->
<!--                  </span>-->
<!--                  <a href="?page={{ inbox_users.paginator.num_pages }}&q={{ request.GET.q }}"-->
<!--                     class="-ml-px relative inline-flex items-center rounded-r-md px-4 py-2 border border-gray-300 bg-white text-sm leading-5 font-medium text-gray-700 hover:text-gray-500 focus:z-10 focus:outline-none focus:border-blue-300 focus:shadow-outline-blue active:bg-gray-100 active:text-gray-700 transition ease-in-out duration-150">-->
<!--                    {{ inbox_users.paginator.num_pages }}-->
<!--                  </a>-->
<!--                  {% endif %}-->
<!--                </nav>-->
<!--              </div>-->
<!--            </div>-->
<!--          </div>-->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SearchBar from "../elements/SearchBar";
import axios from "axios";
import _ from "lodash";

export default {
  name: "Users",
  components: {SearchBar},
    data() {
      return {
        query: "",
        page: null
      }
    },
  mounted() {
    this.performSearch()
  },
  methods: {
    performSearch: function () {
      axios.get(`/api${window.location.pathname}`, {
        params: {
          q: this.query,
        }
      }).then(response => {
        this.page = response.data
      })
    },
    search: _.debounce(this.performSearch, 250),
  }
}
</script>

<style scoped>

</style>