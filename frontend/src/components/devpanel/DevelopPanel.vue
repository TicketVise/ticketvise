<template>
  <!-- Global notification live region, render this permanently at the end of the document -->
  <div aria-live="assertive" class="pointer-events-none fixed top-0 right-0 flex items-start px-8 py-12 opacity-20 transition-opacity duration-100 ease-in-out hover:opacity-100">
    <div class="flex w-full flex-col items-end space-y-4">
      <!-- Notification panel, dynamically insert this into the live region when it needs to be displayed -->
      <transition enter-active-class="transform ease-out duration-300 transition" enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2" enter-to-class="translate-y-0 opacity-100 sm:translate-x-0" leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100" leave-to-class="opacity-0">
        <div v-if="show" class="pointer-events-auto rounded-lg bg-white shadow-xl ring-1 ring-black ring-opacity-5">
          <div class="p-3">
            <div class="flex items-center divide-x">
              <div class="flex space-x-2 p-2">
                <!-- Select useraccount -->
                <Menu as="button" class="relative inline-block items-center text-left">
                  <div>
                    <MenuButton class="flex items-center text-gray-400 outline-none hover:text-gray-500">
                      <UserIcon class="h-5 w-5 flex-shrink-0" aria-hidden="true" />
                      <span class="sr-only">User</span>
                      <ChevronDownIcon class="h-5 w-5 flex-shrink-0" aria-hidden="true" />
                    </MenuButton>
                  </div>

                  <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
                    <MenuItems class="absolute right-0 mt-2 w-36 origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                      <div class="py-1">
                        <MenuItem v-slot="{ active }">
                          <button @click="selectAdmin()" :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'group flex w-full items-center px-4 py-2 text-sm']">
                            <UserIcon class="mr-3 h-5 w-5 text-gray-400 group-hover:text-gray-500" aria-hidden="true" />
                            Admin
                          </button>
                        </MenuItem>
                        <MenuItem v-slot="{ active }">
                          <button @click="selectCoordinator()" :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'group flex w-full items-center px-4 py-2 text-sm']">
                            <UsersIcon class="mr-3 h-5 w-5 text-gray-400 group-hover:text-gray-500" aria-hidden="true" />
                            Coordinator
                          </button>
                        </MenuItem>
                        <MenuItem v-slot="{ active }">
                          <button @click="selectAssistant()" :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'group flex w-full items-center px-4 py-2 text-sm']">
                            <UsersIcon class="mr-3 h-5 w-5 text-gray-400 group-hover:text-gray-500" aria-hidden="true" />
                            Assistant
                          </button>
                        </MenuItem>
                        <MenuItem v-slot="{ active }">
                          <button @click="selectStudent()" :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'group flex w-full items-center px-4 py-2 text-sm']">
                            <UserGroupIcon class="mr-3 h-5 w-5 text-gray-400 group-hover:text-gray-500" aria-hidden="true" />
                            Student
                          </button>
                        </MenuItem>
                      </div>
                      <div class="py-1">
                        <MenuItem v-slot="{ active }">
                          <button @click="logout()" :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'group flex w-full items-center px-4 py-2 text-sm']">
                            <ArrowLeftOnRectangleIcon class="mr-3 h-5 w-5 text-gray-400 group-hover:text-gray-500" aria-hidden="true" />
                            Logout
                          </button>
                        </MenuItem>
                      </div>
                    </MenuItems>
                  </transition>
                </Menu>

                <!-- Select dark mode -->
                <!-- <Menu as="button" class="relative inline-block items-center text-left">
                  <div>
                    <MenuButton class="flex items-center text-gray-400 outline-none hover:text-gray-500">
                      <SunIcon v-if="darkmode == 'light'" class="h-5 w-5 flex-shrink-0" aria-hidden="true" />
                      <MoonIcon v-else-if="darkmode == 'dark'" class="h-5 w-5 flex-shrink-0" aria-hidden="true" />
                      <ComputerDesktopIcon v-else-if="darkmode == 'media'" class="h-5 w-5 flex-shrink-0" aria-hidden="true" />
                      <ChevronDownIcon class="h-5 w-5 flex-shrink-0" aria-hidden="true" />
                    </MenuButton>
                  </div>

                  <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
                    <MenuItems class="absolute right-0 mt-2 w-32 origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                      <div class="py-1">
                        <MenuItem v-slot="{ active }">
                          <button @click="selectLightMode()" :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'group flex w-full items-center px-4 py-2 text-sm']">
                            <SunIcon class="mr-3 h-5 w-5 text-gray-400 group-hover:text-gray-500" aria-hidden="true" />
                            Light
                          </button>
                        </MenuItem>
                        <MenuItem v-slot="{ active }">
                          <button @click="selectDarkMode()" :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'group flex w-full items-center px-4 py-2 text-sm']">
                            <MoonIcon class="mr-3 h-5 w-5 text-gray-400 group-hover:text-gray-500" aria-hidden="true" />
                            Dark
                          </button>
                        </MenuItem>
                        <MenuItem v-slot="{ active }">
                          <button @click="selectMediaMode()" :class="[active ? 'bg-gray-100 text-gray-900' : 'text-gray-700', 'group flex w-full items-center px-4 py-2 text-sm']">
                            <ComputerDesktopIcon class="mr-3 h-5 w-5 text-gray-400 group-hover:text-gray-500" aria-hidden="true" />
                            Media
                          </button>
                        </MenuItem>
                      </div>
                    </MenuItems>
                  </transition>
                </Menu> -->

                <!-- <button @click="startintroduction()" class="flex items-center text-gray-400 outline-none hover:text-gray-500">
                  <SparklesIcon class="h-5 w-5 flex-shrink-0" aria-hidden="true" />
                </button> -->
              </div>

              <!-- <div class="pl-4 pr-2">
                <button type="button" class="inline-flex items-center rounded-full border border-transparent bg-primary-600 p-1 text-white shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2">
                  <PlusIcon class="h-5 w-5" aria-hidden="true" />
                </button>
              </div> -->
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'
import router from '@/router'
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { ChevronDownIcon, SunIcon, MoonIcon, ComputerDesktopIcon, UserGroupIcon, UsersIcon, UserIcon, ArrowLeftOnRectangleIcon, PlusIcon, SparklesIcon } from '@heroicons/vue/24/outline'

export default {
  name: 'DevelopPanel',
  components: {
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    UserIcon,
    UserGroupIcon,
    UsersIcon,
    ChevronDownIcon,
    SunIcon,
    MoonIcon,
    ComputerDesktopIcon,
    ArrowLeftOnRectangleIcon,
    PlusIcon,
    SparklesIcon
  },
  data: () => ({
    inbox: router.getRoutes()
  }),
  setup() {
    const show = ref(true)
    let darkmode = localStorage?.theme
    if (!darkmode) darkmode = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'media' : 'light'

    return { show, darkmode }
  },
  methods: {
    selectLightMode() {
      localStorage.theme = 'light'
      this.darkmode = 'light'
      this.darkMode()
    },
    selectDarkMode() {
      localStorage.theme = 'dark'
      this.darkmode = 'dark'
      this.darkMode()
    },
    selectMediaMode() {
      localStorage.removeItem('theme')
      this.darkmode = 'media'
      this.darkMode()
    },
    darkMode() {
      if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    },
    selectAdmin() {
      const payload = {
        username: 'admin',
        password: 'admin193'
      }

      this.$store.dispatch('login', payload).catch((_) => (this.error = 'Incorrect username or password.'))
    },
    selectCoordinator() {
      const payload = {
        username: 'c.mcauliffe',
        password: 'admin193'
      }

      this.$store.dispatch('login', payload).catch((_) => (this.error = 'Incorrect username or password.'))
    },
    selectAssistant() {
      const payload = {
        username: 'jelleassistant',
        password: 'admin193'
      }

      this.$store.dispatch('login', payload).catch((_) => (this.error = 'Incorrect username or password.'))
    },
    selectStudent() {
      const payload = {
        username: 'e.dijkstra',
        password: 'admin193'
      }

      this.$store.dispatch('login', payload).catch((_) => (this.error = 'Incorrect username or password.'))
    },
    logout() {
      this.$store.dispatch('logout')
    },
    startintroduction() {
      axios.put('/api/me/introduction', { introduction: true })
    }
  }
}
</script>
