<template>
  <div class="container mx-auto lg:px-4 pb-4">
    <div class="bg-gray-50 px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 border-b-2">
      <dt class="text-sm leading-5 font-medium text-gray-700 flex items-center">
        Name
      </dt>
      <dd class="mt-1 text-sm leading-5 text-gray-900 sm:mt-0 sm:col-span-2">
        <input type="text"
               v-model="inbox.name"
               class="block appearance-none w-full bg-white border px-4 py-2 pr-8 rounded shadow-sm leading-tight focus:outline-none focus:shadow-outline"
               name="name">
        <error v-for="error in errors.name" :key="error" :message="error"></error>
      </dd>
    </div>
    <div class="bg-gray-50 px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 border-b-2">
      <dt class="text-sm leading-5 font-medium text-gray-700 flex items-center">
        Code
      </dt>
      <dd class="mt-1 text-sm leading-5 text-gray-900 sm:mt-0 sm:col-span-2">
        <input type="text"
               v-model="inbox.code"
               class="block appearance-none w-full bg-white border px-4 py-2 pr-8 rounded shadow-sm leading-tight focus:outline-none focus:shadow-outline"
               name="code">
        <error v-for="error in errors.code" :key="error" :message="error"></error>
      </dd>
    </div>
    <div class="bg-gray-50 px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 border-b-2">
      <dt class="text-sm leading-5 font-medium text-gray-700 flex items-center">
        Color
      </dt>
      <dd class="mt-1 text-sm leading-5 text-gray-900 sm:mt-0 sm:col-span-2">
        <input type="color"
               v-model="inbox.color"
               class="block appearance-none w-full bg-white border border-gray-400 hover:border-gray-500 overflow-hidden rounded shadow-sm leading-tight focus:outline-none focus:shadow-outline"
               name="color">
        <error v-for="error in errors.color" :key="error" :message="error"></error>
      </dd>
    </div>
    <div class="bg-gray-50 px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 border-b-2">
      <dt class="text-sm leading-5 font-medium text-gray-700 flex items-center">
        Photo
      </dt>
      <div @dragleave="dragleave" @dragover="dragover" @drop="drop"
           class="bg-contain bg-center bg-no-repeat text-sm border-dashed border-gray-500 border-2 rounded h-36 w-36"
           :style="{ 'background-image': `url(${im_url})` }">
        <input accept="image/*" @change="onChange" class="w-px h-px opacity-0 overflow-hidden absolute" id="attachment"
               name="fields[attachment][]" ref="file" type="file"/>
        <div class="flex w-full h-full opacity-0 hover:opacity-75 hover:bg-gray-300 text-center">
        <label class="m-auto cursor-pointer" for="attachment">
            <span class="underline">Browse</span> or drop your photo here.
        </label>
        </div>
      </div>
      <error v-for="error in errors.attachments" :key="error" :message="error"></error>
    </div>
    <div class="bg-gray-50 px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 border-b-2">
      <label for="show_assignee_to_guest" class="text-sm leading-5 font-medium text-gray-700 flex items-center">
        Assignee visible to students
      </label>
      <dd class="mt-1 text-sm leading-5 text-gray-900 sm:mt-0 sm:col-span-2">
        <input type="checkbox"
               v-model="inbox.show_assignee_to_guest"
               class="block" name="show_assignee_to_guest" id="show_assignee_to_guest">
      </dd>
    </div>
    <h3 class="text-xl mt-4 leading-6 font-medium text-gray-900 p-2 pb-1">
      Tickets
    </h3>
    <div class="bg-gray-50 px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 border-b-2">
      <label for="close_answered_weeks" class="text-sm leading-5 font-medium text-gray-700 flex items-center">
        Close answered ticket automatically after
      </label>
      <dd class="text-sm leading-5 text-gray-900 sm:mt-0 sm:col-span-2">
        <select name="close_answered_weeks" id="close_answered_weeks"
                class="block appearance-none bg-white border border-gray-400 hover:border-gray-500 px-4 py-1 pr-8 rounded shadow-sm leading-tight focus:outline-none focus:shadow-outline"
                v-model="inbox.close_answered_weeks">
          <option value="0">Disabled</option>
          <option value="1"> 1 week</option>
          <option value="2"> 2 weeks</option>
          <option value="3"> 3 weeks</option>
          <option value="4"> 4 weeks</option>
        </select>
      </dd>
    </div>
    <div class="bg-gray-50 px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 border-b-2">
      <label for="alert_coordinator_unanswered_days"
             class="text-sm leading-5 font-medium text-gray-700 flex items-center">
        Send alert of unanswered tickets after
      </label>
      <dd class="text-sm leading-5 text-gray-900 sm:mt-0 sm:col-span-2">
        <select name="alert_coordinator_unanswered_days" id="alert_coordinator_unanswered_days"
                class="block appearance-none bg-white border border-gray-400 hover:border-gray-500 px-4 py-1 pr-8 rounded shadow-sm leading-tight focus:outline-none focus:shadow-outline"
                v-model="inbox.alert_coordinator_unanswered_days">
          <option value="0">Disabled</option>
          <option value="1">1 day</option>
          <option :value="i" v-for="i in [2,3,4,5,6,7]" :key="i">{{ i }} days</option>
        </select>
      </dd>
    </div>
    <div class="bg-gray-50 px-4 py-3 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6 border-b-2">
      <label for="scheduling_algorithm" class="text-sm leading-5 font-medium text-gray-700 flex items-center">
        Scheduling algorithm
      </label>
      <dd class="text-sm leading-5 text-gray-900 sm:mt-0 sm:col-span-2">
        <select name="scheduling_algorithm" id="scheduling_algorithm"
                class="block appearance-none bg-white border border-gray-400 hover:border-gray-500 px-4 py-1 pr-8 rounded shadow-sm leading-tight focus:outline-none focus:shadow-outline"
                v-model="inbox.scheduling_algorithm">
          <option :value="option[0]" v-for="option in scheduling_options" :key="option[0]">
            {{ option[1] }}
          </option>
        </select>
      </dd>
      <label for="fixed_scheduling_assignee"
             class="text-sm leading-5 font-medium text-gray-700 flex items-center">
        Fixed scheduling assignee
      </label>
      <dd class="text-sm leading-5 text-gray-900 sm:mt-0 sm:col-span-2">
        <select name="fixed_scheduling_assignee" id="fixed_scheduling_assignee"
                class="block appearance-none bg-white border border-gray-400 hover:border-gray-500 px-4 py-1 pr-8 rounded shadow-sm leading-tight focus:outline-none focus:shadow-outline"
                v-model="inbox.fixed_scheduling_assignee">
          <option :value="undefined">None</option>
          <option :value="value.id" v-for="value in staff" :key="value.id">
            {{ value.first_name }} {{ value.last_name }}
          </option>
        </select>
      </dd>
    </div>

    <div class="bg-teal-100 border-t-4 border-teal-500 rounded-b text-teal-900 px-4 py-3 shadow-md" role="alert"
         v-if="saved">
      <p class="text-sm ">Settings saved successfully.</p>
    </div>
    <div class="p-2 px-4 sm:pr-0 flex space-x-2 sm:mx-4 justify-end">
      <button type="button" @click="onCancel()"
              class="group inline-flex items-center px-4 py-2 border border-gray-300 text-sm leading-5 font-medium rounded-md text-gray-700 bg-white hover:text-gray-500 focus:outline-none focus:shadow-outline-blue focus:border-blue-300 active:text-gray-800 active:bg-gray-50">
        <span class="left-0 inset-y-0 flex items-center">
          <i class="fa fa-times mr-2"></i>
        </span>
        Cancel
      </button>
      <button type="button" @click="onSave()"
              class="group inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm leading-5 font-medium rounded-md bg-green-200 text-green-700 hover:bg-green-100 focus:outline-none focus:shadow-outline-indigo focus:border-green-700 active:bg-green-700 ">
        <span class="left-0 inset-y-0 flex items-center">
          <i class="fa fa-check mr-2"></i>
        </span>
        Save
      </button>
    </div>
  </div>
</template>

<script>
  import axios from "axios";
  import Error from "../elements/message/Error";
  import FileUpload from "../elements/FileUpload";

  export default {
    name: "InboxSettings",
    components: {FileUpload, Error},
    data() {
      return {
        inbox_id: window.location.pathname.split('/')[2],
        inbox: {},
        im_url: "",
        staff: [],
        scheduling_options: [],
        errors: [],
        saved: false
      }
    },
    created() {
      axios.get("/api/inboxes/" + this.inbox_id + "/settings").then(response => {
        this.inbox = response.data.inbox;
        this.staff = response.data.staff;
        this.scheduling_options = response.data.scheduling_options
        this.im_url = this.inbox.image;
      })
    },
    methods: {
      onSave: function () {
        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

        let formData = new FormData();

        for (let key in this.inbox) {
          if (key !== "image") {
            formData.append(key, this.inbox[key]);
          } else if (this.inbox[key] !== this.im_url) {
            formData.append(key, this.inbox[key]);
          }
        }
        const config = {
          headers: {'content-type': 'multipart/form-data'}
        }

        axios.put("/api/inboxes/" + this.inbox_id + "/settings", formData, config).then(response => {
          this.errors = [];
          this.saved = true;
          this.inbox = response.data
        }).catch(error => {
          this.saved = false;
          this.errors = error.response.data
        })
      },
      onCancel: function () {
        window.history.back();
      },

      onChange(event) {
        if (event) {
          this.inbox.image = event.target.files[0];
        }
        let reader = new FileReader;
        reader.onload = e => {
          this.im_url = e.target.result
        };
        reader.readAsDataURL(this.inbox.image)
      },
      dragover(event) {
        event.preventDefault();
        if (!event.currentTarget.classList.contains('bg-orange-300')) {
          event.currentTarget.classList.remove('bg-gray-100');
          event.currentTarget.classList.add('bg-orange-300');
        }
      },
      dragleave(event) {
        event.currentTarget.classList.add('bg-gray-100');
        event.currentTarget.classList.remove('bg-orange-300');
      },
      drop(event) {
        event.preventDefault();
        this.inbox.image = event.dataTransfer.files[0];

        this.onChange();
        this.dragleave(event)
      }
    }
  }
</script>