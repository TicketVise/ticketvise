<template>
  <div class="container mx-auto lg:px-4 pb-4">
    <search-bar v-model="query" v-on:input="search" class="flex-grow px-2 my-2"/>

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
            <tbody class="bg-white" v-if="page">

            <tr v-for="inboxUser in page.results" :key="inboxUser.id">
              <td class="px-6 py-4 whitespace-nowrap border-b border-gray-200">

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
              <td class="px-6 py-4 whitespace-nowrap border-b border-gray-200">
                <div class="text-sm leading-5 text-gray-900">@{{ inboxUser.user.username }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap border-b border-gray-200">
                <span v-if="inboxUser.user.is_active"
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                  Active
                </span>
                <span v-else
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">
                  Inactive
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap border-b border-gray-200 text-sm leading-5 text-gray-500">
                {{ inboxUser.role_label }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right border-b border-gray-200 text-sm leading-5 font-medium">
                <router-link :to="getInboxUserUrl(inboxUser)" class="text-indigo-600 hover:text-indigo-900">
                  Edit
                </router-link>
              </td>
            </tr>
            </tbody>
          </table>
          <div class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
            <pagination v-if="page" :page="page" @go="performSearch"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SearchBar from "../elements/SearchBar";
import axios from "axios";
import {debounce} from "lodash";
import Pagination from "./Pagination";

export default {
  name: "Users",
  components: {Pagination, SearchBar},
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
    performSearch: function (page) {
      const inboxId = this.$route.params.inboxId
      axios.get(`/api/inboxes/${inboxId}/users`, {
        params: {
          q: this.query,
          page: page
        }
      }).then(response => {
        this.page = response.data
      })
    },
    search: debounce(function () {
      this.performSearch()
    }, 250),
    getInboxUserUrl: function (inboxUser) {
      const inboxId = this.$route.params.inboxId
      return `/inboxes/${inboxId}/users/${inboxUser.user.id}`
    }
  }
}
</script>

<style scoped>

</style>
