<template>
  <div class="container mx-auto lg:px-4 pb-4">

    <div class="flex w-full p-2 sm:px-0 sm:pb-4 space-x-2">
      <search-bar v-model="query" v-on:input="search" class="flex-grow px-2 my-2"/>
      <a type="button" :href="add_url"
         class="inline-flex items-center px-4 my-2 border border-transparent text-sm leading-5 font-medium rounded-md text-white bg-primary hover:bg-orange-500 focus:outline-none focus:shadow-outline-orange focus:border-orange-700 active:bg-orange-700 transition duration-150 ease-in-out">
        <i class="fa fa-plus mr-2"></i>
        Add
      </a>
    </div>

    <div class="flex flex-col">
      <div class="-my-2 py-2 overflow-x-auto px-2 sm:-mx-6 sm:px-6 lg:-mx-8 lg:px-8">
        <div class="align-middle inline-block min-w-full shadow overflow-hidden sm:rounded-lg border-b border-gray-200">
          <table class="min-w-full">
            <thead>
            <tr>
              <th class="px-6 py-3 border-b border-gray-200 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                Name
              </th>
              <th class="px-6 py-3 border-b border-gray-200 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                Color
              </th>
              <th class="px-6 py-3 border-b border-gray-200 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                Visible to student
              </th>
              <th class="px-6 py-3 border-b border-gray-200 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th class="px-6 py-3 border-b border-gray-200 bg-gray-50"></th>
            </tr>
            </thead>
            <tbody v-if="page" class="bg-white">
              <tr :key="label.name" v-for="label in page.results">
                <td class="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
                  <div class="text-sm leading-5 text-gray-900 font-medium">{{ label.name }}</div>
                </td>
                <td class="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
                  <span class="flex rounded-full shadow uppercase px-2 py-1 text-xs font-bold mr-3"
                        :style="{ background: label.color }"></span>
                  <div class="text-sm leading-5 text-gray-500 uppercase">{{ label.color }}</div>
                </td>
                <td class="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
                  <span v-if="label.is_visible_to_guest"
                        class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                    Visible
                  </span>
                  <span v-else
                        class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800">
                    Invisible
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-no-wrap border-b border-gray-200">
                  <span v-if="label.is_active"
                        class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                    Active
                  </span>
                  <span v-else
                        class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">
                    Inactive
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-no-wrap text-right border-b border-gray-200 text-sm leading-5 font-medium">
                  <a :href="getLabelUrl(label)"
                    class="text-indigo-600 hover:text-indigo-900">Edit</a>
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
  name: "Labels",
  components: {SearchBar, Pagination},
  data() {
    return {
      query: "",
      page: null
    }
  },
  mounted() {
    this.performSearch()
  },
  computed: {
    add_url: function () {
      return window.location.pathname + '/new'
    }
  },
  methods: {
    performSearch: function (page) {
      axios.get(`/api${window.location.pathname}`, {
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
    getLabelUrl: function (label) {
      return window.location.pathname + '/' + label.id
    },
  }
}
</script>

<style scoped>

</style>