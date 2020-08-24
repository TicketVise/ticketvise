<template>
  <div class="w-full">
    <div class="block text-gray-700 font-semibold mb-2" for="username">
      Share with
    </div>
    <div class="flex flex-wrap mb-2" v-if="shared_with.length > 0">
      <chip v-for="(user, index) in shared_with" :key="user.id" class="my-1 mx-1">
        {{ user.first_name }} {{ user.last_name }}
        <a class="fa fa-close cursor-pointer" @click="removeSharedWith(index)"></a>
      </chip>
    </div>
    <form @submit.prevent="username.length ? getUsername(username) : {}" class="flex space-x-2 w-full mb-2">
      <input
              class="appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none flex-grow focus:border-gray-800"
              id="username" name="username" placeholder="username" type="text" v-model="username">
      <submit-button v-on:click.native="username.length ? getUsername(username) : {}" class="bg-primary text-white"
                     text="Share"></submit-button>
    </form>
    <error v-for="error in this.errors.shared_with" :key="error" :message="error"></error>
    <error v-for="error in this.usernameErrors.username" :key="error" :message="error"></error>
  </div>
</template>

<script>
  import SubmitButton from "../elements/buttons/SubmitButton";
  import axios from "axios";

  export default {
    name: "EditShareWith",
    components: {SubmitButton},
    props: ["inbox_id", "shared_with", "errors"],
    data() {
      return {
        username: "",
        usernameErrors: []
      }
    },
    methods: {
      removeSharedWith: function (index) {
        this.shared_with.splice(index, 1);
        this.$emit("input", this.shared_with)
      },
      getUsername(username) {
        axios.get("/api/inboxes/" + this.inbox_id + "/users/" + username).then(response => {
          this.usernameErrors = []
          // Check if user exists in array
          let index = this.shared_with.findIndex(user => user.id === response.data.id)
          if (index === -1) {
            this.shared_with.push(response.data)
            this.$emit("input", this.shared_with)

          }
          this.username = ""
        }).catch(error => {
              this.usernameErrors = error.response.data
            }
        )

      }
    }
  }
</script>

<style scoped>

</style>
