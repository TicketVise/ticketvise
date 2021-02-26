<template>
  <div class="w-full">
    <div class="block text-gray-700 font-semibold mb-2" for="user_to_share">
      Shared with
    </div>
    <div class="flex flex-wrap mb-2" v-if="shared_with.length > 0">
      <chip v-for="(user, index) in shared_with" :key="user.id" class="my-1 mx-1">
        {{ user.first_name }} {{ user.last_name }}
        <a class="fa fa-close cursor-pointer ml-1" @click="removeSharedWith(index)" v-if="can_share"></a>
      </chip>
    </div>
    <form @submit.prevent="shareWithUser" class="flex space-x-2 w-full mb-2"
          v-if="can_share">
      <div class="space-y-1 flex-grow" v-on-clickaway="away">
        <div class="relative">
          <input class="appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none flex-grow focus:border-gray-800"
                 type="text" @focus="open=true" v-model="query" @keyup="filterGuests()" placeholder="Search user">
          <div class="absolute mt-1 w-full rounded-md bg-white shadow-lg z-50" v-if="open">
            <ul aria-activedescendant="listbox-item-3" aria-labelledby="listbox-label"
                class="max-h-56 rounded-md py-1 text-base leading-6 shadow-xs overflow-auto focus:outline-none sm:text-sm sm:leading-5"
                role="listbox"
                tabindex="-1">
              <li :key="item.id" :value="item.id" @click="selectUserToShare(item)"
                  class="text-gray-900 hover:text-white hover:bg-orange-400 cursor-pointer select-none relative py-2 pl-3 pr-9"
                  id="listbox-item-0"
                  role="option"
                  v-for="item in guestsWithoutAuthorAndSharedUsers">
                <div class="flex items-center space-x-3">
                  <avatar :source="item.avatar_url" class="w-6 h-6 rounded-full"></avatar>
                  <span class="font-normal block truncate">{{ item.first_name }} {{ item.last_name }}</span>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <submit-button v-on:click.native="shareWithUser"
                     class="bg-primary hover:bg-orange-500 text-white"
                     text="Share"></submit-button>
    </form>
    <error v-for="error in this.errors.shared_with" :key="error" :message="error"></error>
  </div>
</template>

<script>
  import SubmitButton from "../elements/buttons/SubmitButton"
  import axios from "axios"
  import {mixin as clickaway} from 'vue-clickaway'

  export default {
    name: "EditShareWith",
    components: {SubmitButton},
    mixins: [clickaway],
    props: ["inbox_id", "shared_with", "errors", "author", "can_share"],
    data() {
      return {
        user_to_share: null,
        open: false,
        query: "",
        guests: [],
      }
    },
    created() {
      axios.get("/api/inboxes/" + this.inbox_id + "/guests").then(response => {
        this.guests = response.data;
      })
    },
    methods: {
      removeSharedWith: function (index) {
        this.shared_with.splice(index, 1);
        this.$emit("input", this.shared_with)
      },
      shareWithUser() {
        // Check if user is already in shared_with
        if (!this.user_to_share) {
          return
        }
        let index = this.shared_with.indexOf(this.user_to_share)
        if (index === -1) {
          // User not in share_with, push it to parent
          this.shared_with.push(this.user_to_share)
          this.$emit("input", this.shared_with)
        }
        // Clear search
        this.user_to_share = null;
        this.query = "";
        this.filterGuests()
      },
      selectUserToShare(user) {
        // Assign selected user from dropdown to user_to_share
        this.user_to_share = user;
        this.query = user.first_name + " " + user.last_name;
        this.open = false
      },
      filterGuests() {
        axios.get("/api/inboxes/" + this.inbox_id + "/guests", {
          params: {
            "q": this.query,
            "size": 5
          }
        }).then(response => {
          this.guests = response.data;
        })
      },
      away() {
        this.open = false
      },
    },
    computed: {
      guestsWithoutAuthorAndSharedUsers: function () {
        // Remove author from list
        let guests = this.guests;
        if (this.author) {
          guests = guests.filter(obj => {
            return obj.id !== this.author.id
          })
        }

        // Remove shared users from list
        this.shared_with.forEach(shared_user =>
          guests = guests.filter(obj => {
            return obj.id !== shared_user.id
          })
        )

        return guests
      }
    }
  }
</script>

<style scoped>

</style>
