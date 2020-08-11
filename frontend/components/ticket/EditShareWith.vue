<template>
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
</template>

<script>
import SubmitButton from "../elements/buttons/SubmitButton";
import axios from "axios";

export default {
  name: "EditShareWith",
  components: {SubmitButton},
  props: ["inbox_id"],
  data() {
    return {
      username: "",
      shared_with: []
    }
  },
  methods: {
    removeSharedWith: function (index) {
      this.shared_with.splice(index, 1);
    },
    getUsername(username) {
      axios.get("/api/inboxes/" + this.inbox_id + "/users/" + username).then(response => {
        this.errors = []
        // Check if user exists in array
        let index = this.shared_with.findIndex(user => user.id === response.data.id)
        if (index === -1) {
          this.shared_with.push(response.data)
          this.$emit("input", this.shared_with)

        }
        this.username = ""
      }).catch(error => {
            this.errors = error.response.data
          }
      )

    }
  }
}
</script>

<style scoped>

</style>