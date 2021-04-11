<template>
  <div class="min-h-screen">
    <div class="py-10">
      <div class="max-w-5/6 mx-auto sm:px-6 lg:px-8 grid">
        <main class="w-2/3 place-self-center ">
          <div class="px-4 sm:px-0">
            <div class="sm:hidden">
              <label for="question-tabs" class="sr-only">Select a tab</label>
              <select id="question-tabs"
                      class="block w-full rounded-md border-gray-300 text-base font-medium text-gray-900 shadow-sm focus:border-rose-500 focus:ring-rose-500">
                <option value="">Recent</option>
                <option value="">Unread</option>
                <option value="">Bookmarked</option>
              </select>
            </div>
            <div class="hidden sm:block">
              <nav class="relative z-0 rounded-lg shadow flex divide-x divide-gray-200" aria-label="Tabs">
                <a href="" aria-current="page"
                   class="text-gray-900 rounded-l-lg group relative min-w-0 flex-1 overflow-hidden bg-white py-4 px-6 text-sm font-medium text-center hover:bg-gray-50 focus:z-10">
                  <span>Recent</span>
                  <span aria-hidden="true" class="bg-rose-500 absolute inset-x-0 bottom-0 h-0.5"></span>
                </a>

                <a href="" aria-current="false"
                   class="text-gray-500 hover:text-gray-700 group relative min-w-0 flex-1 overflow-hidden bg-white py-4 px-6 text-sm font-medium text-center hover:bg-gray-50 focus:z-10">
                  <span>Unread</span>
                  <span aria-hidden="true" class="bg-transparent absolute inset-x-0 bottom-0 h-0.5"></span>
                </a>

                <a href="" aria-current="false"
                   class="text-gray-500 hover:text-gray-700 rounded-r-lg group relative min-w-0 flex-1 overflow-hidden bg-white py-4 px-6 text-sm font-medium text-center hover:bg-gray-50 focus:z-10">
                  <span>Bookmarked</span>
                  <span aria-hidden="true" class="bg-transparent absolute inset-x-0 bottom-0 h-0.5"></span>
                </a>
              </nav>
            </div>
          </div>
          <div class="py-2">
            <search-bar></search-bar>
          </div>
          <div class="mt-4">
            <h1 class="sr-only">Recent questions</h1>
            <ul class="space-y-4">
              <li class="bg-white px-4 py-6 shadow sm:p-6 sm:rounded-lg">
                <article aria-labelledby="question-title-81614">
                  <div>
                    <div class="flex space-x-3">
                      <div class="flex-shrink-0">
                        <img class="h-10 w-10 rounded-full"
                             src="https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=facearea&amp;facepad=2&amp;w=256&amp;h=256&amp;q=80"
                             alt="">
                      </div>
                      <div class="min-w-0 flex-1">
                        <p class="text-sm font-medium text-gray-900">
                          <a href="#" class="hover:underline">Dries Vincent</a>
                        </p>
                        <p class="text-sm text-gray-500">
                          <a href="#" class="hover:underline">December 9 at 11:43 AM</a>
                        </p>
                      </div>
                      <div class="flex-shrink-0 self-center flex">
                        <div class="relative inline-block text-left">
                          <div>
                            <button type="button"
                                    class="-m-2 p-2 rounded-full flex items-center text-gray-400 hover:text-gray-600"
                                    id="options-menu-0" aria-expanded="false" aria-haspopup="true">
                              <span class="sr-only">Open options</span>
                              <!-- Heroicon name: solid/dots-vertical -->
                              <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"
                                   fill="currentColor" aria-hidden="true">
                                <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
                              </svg>
                            </button>
                          </div>

                          <!--
                            Dropdown menu, show/hide based on menu state.

                            Entering: "transition ease-out duration-100"
                              From: "transform opacity-0 scale-95"
                              To: "transform opacity-100 scale-100"
                            Leaving: "transition ease-in duration-75"
                              From: "transform opacity-100 scale-100"
                              To: "transform opacity-0 scale-95"
                          -->
                          <div class="origin-top-right absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none"
                               role="menu" aria-orientation="vertical" aria-labelledby="options-menu-0">
                            <div class="py-1">
                              <a href="#"
                                 class="flex px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
                                 role="menuitem">
                                <!-- Heroicon name: solid/star -->
                                <svg class="mr-3 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg"
                                     viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                                </svg>
                                <span>Add to favorites</span>
                              </a>
                              <a href="#"
                                 class="flex px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
                                 role="menuitem">
                                <!-- Heroicon name: solid/code -->
                                <svg class="mr-3 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg"
                                     viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                                  <path fill-rule="evenodd"
                                        d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z"
                                        clip-rule="evenodd"/>
                                </svg>
                                <span>Embed</span>
                              </a>
                              <a href="#"
                                 class="flex px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
                                 role="menuitem">
                                <!-- Heroicon name: solid/flag -->
                                <svg class="mr-3 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg"
                                     viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                                  <path fill-rule="evenodd"
                                        d="M3 6a3 3 0 013-3h10a1 1 0 01.8 1.6L14.25 8l2.55 3.4A1 1 0 0116 13H6a1 1 0 00-1 1v3a1 1 0 11-2 0V6z"
                                        clip-rule="evenodd"/>
                                </svg>
                                <span>Report content</span>
                              </a>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <h2 id="question-title-81614" class="mt-4 text-base font-medium text-gray-900">
                      What would you have done differently if you ran Jurassic Park?
                    </h2>
                  </div>
                  <div class="mt-2 text-sm text-gray-700 space-y-4">
                    <p>
                      Jurassic Park was an incredible idea and a magnificent feat of engineering, but poor protocols and
                      a disregard for human safety killed what could have otherwise been one of the best businesses of
                      our generation.
                    </p>
                    <p>
                      Ultimately, I think that if you wanted to run the park successfully and keep visitors safe, the
                      most important thing to prioritize would be&hellip;
                    </p>
                  </div>
                  <div class="mt-6 flex justify-between space-x-8">
                    <div class="flex space-x-6">
                    <span class="inline-flex items-center text-sm">
                      <button class="inline-flex space-x-2 text-gray-400 hover:text-gray-500">
                        <!-- Heroicon name: solid/thumb-up -->
                        <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"
                             aria-hidden="true">
                          <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z"/>
                        </svg>
                        <span class="font-medium text-gray-900">29</span>
                        <span class="sr-only">likes</span>
                      </button>
                    </span>
                      <span class="inline-flex items-center text-sm">
                      <button class="inline-flex space-x-2 text-gray-400 hover:text-gray-500">
                        <!-- Heroicon name: solid/chat-alt -->
                        <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"
                             aria-hidden="true">
                          <path fill-rule="evenodd"
                                d="M18 5v8a2 2 0 01-2 2h-5l-5 4v-4H4a2 2 0 01-2-2V5a2 2 0 012-2h12a2 2 0 012 2zM7 8H5v2h2V8zm2 0h2v2H9V8zm6 0h-2v2h2V8z"
                                clip-rule="evenodd"/>
                        </svg>
                        <span class="font-medium text-gray-900">11</span>
                        <span class="sr-only">replies</span>
                      </button>
                    </span>
                      <span class="inline-flex items-center text-sm">
                      <button class="inline-flex space-x-2 text-gray-400 hover:text-gray-500">
                        <!-- Heroicon name: solid/eye -->
                        <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"
                             aria-hidden="true">
                          <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/>
                          <path fill-rule="evenodd"
                                d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
                                clip-rule="evenodd"/>
                        </svg>
                        <span class="font-medium text-gray-900">2.7k</span>
                        <span class="sr-only">views</span>
                      </button>
                    </span>
                    </div>
                    <div class="flex text-sm">
                    <span class="inline-flex items-center text-sm">
                      <button class="inline-flex space-x-2 text-gray-400 hover:text-gray-500">
                        <!-- Heroicon name: solid/share -->
                        <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"
                             aria-hidden="true">
                          <path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z"/>
                        </svg>
                        <span class="font-medium text-gray-900">Share</span>
                      </button>
                    </span>
                    </div>
                  </div>
                </article>
              </li>

              <li class="bg-white px-4 py-6 shadow sm:p-6 sm:rounded-lg">
                <article aria-labelledby="question-title-89019">
                  <div>
                    <div class="flex space-x-3">
                      <div class="flex-shrink-0">
                        <img class="h-10 w-10 rounded-full"
                             src="https://images.unsplash.com/photo-1517841905240-472988babdf9?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=facearea&amp;facepad=2&amp;w=256&amp;h=256&amp;q=80"
                             alt="">
                      </div>
                      <div class="min-w-0 flex-1">
                        <p class="text-sm font-medium text-gray-900">
                          <a href="#" class="hover:underline">Lindsay Walton</a>
                        </p>
                        <p class="text-sm text-gray-500">
                          <a href="#" class="hover:underline">December 8 at 10:45 PM</a>
                        </p>
                      </div>
                      <div class="flex-shrink-0 self-center flex">
                        <div class="relative inline-block text-left">
                          <div>
                            <button type="button"
                                    class="-m-2 p-2 rounded-full flex items-center text-gray-400 hover:text-gray-600"
                                    id="options-menu-1" aria-expanded="false" aria-haspopup="true">
                              <span class="sr-only">Open options</span>
                              <!-- Heroicon name: solid/dots-vertical -->
                              <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"
                                   fill="currentColor" aria-hidden="true">
                                <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
                              </svg>
                            </button>
                          </div>

                          <!--
                            Dropdown menu, show/hide based on menu state.

                            Entering: "transition ease-out duration-100"
                              From: "transform opacity-0 scale-95"
                              To: "transform opacity-100 scale-100"
                            Leaving: "transition ease-in duration-75"
                              From: "transform opacity-100 scale-100"
                              To: "transform opacity-0 scale-95"
                          -->
                          <div class="origin-top-right absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none"
                               role="menu" aria-orientation="vertical" aria-labelledby="options-menu-1">
                            <div class="py-1">
                              <a href="#"
                                 class="flex px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
                                 role="menuitem">
                                <!-- Heroicon name: solid/star -->
                                <svg class="mr-3 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg"
                                     viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                                </svg>
                                <span>Add to favorites</span>
                              </a>
                              <a href="#"
                                 class="flex px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
                                 role="menuitem">
                                <!-- Heroicon name: solid/code -->
                                <svg class="mr-3 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg"
                                     viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                                  <path fill-rule="evenodd"
                                        d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z"
                                        clip-rule="evenodd"/>
                                </svg>
                                <span>Embed</span>
                              </a>
                              <a href="#"
                                 class="flex px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
                                 role="menuitem">
                                <!-- Heroicon name: solid/flag -->
                                <svg class="mr-3 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg"
                                     viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                                  <path fill-rule="evenodd"
                                        d="M3 6a3 3 0 013-3h10a1 1 0 01.8 1.6L14.25 8l2.55 3.4A1 1 0 0116 13H6a1 1 0 00-1 1v3a1 1 0 11-2 0V6z"
                                        clip-rule="evenodd"/>
                                </svg>
                                <span>Report content</span>
                              </a>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <h2 id="question-title-89019" class="mt-4 text-base font-medium text-gray-900">
                      What&#039;s it like to be a golden retriever?
                    </h2>
                  </div>
                  <div class="mt-2 text-sm text-gray-700 space-y-4">
                    <p>
                      Man I am glad you asked this question. I'm a 6 year old golden retriever and while I still have a
                      few years left to experience, I think I've been around long enough to tell you what it's really
                      like.
                    </p>
                    <p>Most people think being a dog is awesome. You sleep as much as you want, all of your meals are
                      prepared for you, and someone literally picks up your poop you. And yeah, you know what, those
                      parts <em>are</em> pretty awesome. But there's a dark side to being a golden retriever that they
                      don't tell you about&hellip;</p>
                  </div>
                  <div class="mt-6 flex justify-between space-x-8">
                    <div class="flex space-x-6">
                    <span class="inline-flex items-center text-sm">
                      <button class="inline-flex space-x-2 text-gray-400 hover:text-gray-500">
                        <!-- Heroicon name: solid/thumb-up -->
                        <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"
                             aria-hidden="true">
                          <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z"/>
                        </svg>
                        <span class="font-medium text-gray-900">316</span>
                        <span class="sr-only">likes</span>
                      </button>
                    </span>
                      <span class="inline-flex items-center text-sm">
                      <button class="inline-flex space-x-2 text-gray-400 hover:text-gray-500">
                        <!-- Heroicon name: solid/chat-alt -->
                        <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"
                             aria-hidden="true">
                          <path fill-rule="evenodd"
                                d="M18 5v8a2 2 0 01-2 2h-5l-5 4v-4H4a2 2 0 01-2-2V5a2 2 0 012-2h12a2 2 0 012 2zM7 8H5v2h2V8zm2 0h2v2H9V8zm6 0h-2v2h2V8z"
                                clip-rule="evenodd"/>
                        </svg>
                        <span class="font-medium text-gray-900">41</span>
                        <span class="sr-only">replies</span>
                      </button>
                    </span>
                      <span class="inline-flex items-center text-sm">
                      <button class="inline-flex space-x-2 text-gray-400 hover:text-gray-500">
                        <!-- Heroicon name: solid/eye -->
                        <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"
                             aria-hidden="true">
                          <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/>
                          <path fill-rule="evenodd"
                                d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
                                clip-rule="evenodd"/>
                        </svg>
                        <span class="font-medium text-gray-900">11.7k</span>
                        <span class="sr-only">views</span>
                      </button>
                    </span>
                    </div>
                    <div class="flex text-sm">
                    <span class="inline-flex items-center text-sm">
                      <button class="inline-flex space-x-2 text-gray-400 hover:text-gray-500">
                        <!-- Heroicon name: solid/share -->
                        <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"
                             aria-hidden="true">
                          <path d="M15 8a3 3 0 10-2.977-2.63l-4.94 2.47a3 3 0 100 4.319l4.94 2.47a3 3 0 10.895-1.789l-4.94-2.47a3.027 3.027 0 000-.74l4.94-2.47C13.456 7.68 14.19 8 15 8z"/>
                        </svg>
                        <span class="font-medium text-gray-900">Share</span>
                      </button>
                    </span>
                    </div>
                  </div>
                </article>
              </li>
            </ul>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
  import SearchBar from "../elements/SearchBar";
  import axios from "axios";
  import _ from "lodash";

  export default {
    name: "PublicTickets",
    components: {SearchBar},
    data() {
      return {
        inbox: null,
        ticket: null,
        replies: [],
        labels: [],
        comments: [],
        staff: [],
        events: [],
      }
    },
    created() {
      this.getTickets()
      // this.loadTicket()
    },
    methods: {
      getTickets: function () {
        // Call this function by using callDebounceSearch when searching
        let labels_ids = [];
        this.labels.forEach(label => labels_ids.push(label.id));
        const inboxId = this.$route.params.inboxId

        axios.get(`/api/inboxes/${inboxId}/tickets`, {
          params: {
            q: this.search, // Query to search for tickets
            labels: labels_ids, // To filter on labels
            public: true // Defines that public tickets should be loaded
          }
        }).then(response => {
          this.tickets = response.data
        })
      },
      callDebounceSearch: _.debounce(function () {
        this.get_tickets();
      }, 300)
      loadTicket: function () {
        // Load single ticket for in the public ticket page.
        const inboxId = this.$route.params.inboxId
        const ticketInboxId = this.$route.params.ticketInboxId

        axios.get(`/api/inboxes/${inboxId}/public/${ticketInboxId}`).then(response => {
          this.ticket = response.data.ticket;
        });
      },
    }
  }
</script>

<style scoped>

</style>