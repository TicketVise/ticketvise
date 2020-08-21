<template>
  <div>
    <h4 class="font-semibold text-gray-800 m-2">Share with</h4>
    <error v-for="error in this.errors.shared_with" :key="error" :message="error"></error>
    <error v-for="error in this.usernameErrors.username" :key="error" :message="error"></error>
    <div class="ml-2">
      <chip class="m-1" v-for="(user, index) in shared_with" :key="user.id">
        {{ user.first_name }} {{ user.last_name }}
        <a class="fa fa-close" @click="removeSharedWith(index)"></a>
      </chip>
      <card class="my-2" outlined>
        <input class="m-1" v-model="username" placeholder="Username">
      </card>
      <submit-button v-on:click.native="username.length ? getUsername(username) : {}" class="bg-green-200"
                     text="Add"></submit-button>
    </div>
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