<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:max-w-7xl lg:px-8">
    <header class="bg-white shadow rounded-lg pb-4 mb-4">
      <div class="max-w-7xl mx-auto p-4">
        <div class="sm:flex sm:items-center sm:justify-between">
          <div class="flex-1 min-w-0">
            <span class="sm:hidden float-right">
              <a
                href="/api/admin/django"
                class="inline-flex items-center py-2 text-sm leading-5 font-medium text-gray-700 hover:text-gray-500 focus:outline-none active:text-gray-800 active:bg-gray-50 transition duration-150 ease-in-out"
              >
                <CogIcon class="mr-3 h-5 w-5 text-gray-400" />
              </a>
            </span>

            <h2
              class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:leading-9 truncate"
            >
              Admin overview
            </h2>
          </div>
          <div class="mt-2 sm:mt-0 sm:ml-4 space-x-4 hidden sm:flex">
            <span class="shadow-sm rounded-md">
              <a
                href="/api/admin/django"
                class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm leading-5 font-medium rounded-md text-gray-700 bg-white hover:text-gray-500 focus:outline-none focus:ring-blue focus:border-blue-300 active:text-gray-800 active:bg-gray-50 transition duration-150 ease-in-out"
              >
                <CogIcon class="mr-3 h-5 w-5 text-gray-400" />
                Django admin
              </a>
            </span>
          </div>
        </div>
      </div>

      <div class="grid md:grid-cols-3 gap-4 mx-4">
        <div
          class="rounded-md border flex-grow py-2 px-4 flex md:flex-col-reverse space-x-2 md:space-x-0 items-center md:items-start"
        >
          <div class="flex items-baseline sm:mt-1">
            <h2 class="text-2xl font-medium text-primary">
              {{ inboxes.length }}
            </h2>
          </div>
          <h3 class="text-lg leading-6 font-medium text-gray-900">Inboxes</h3>
        </div>

        <div
          class="rounded-md border flex-grow py-2 px-4 flex md:flex-col-reverse space-x-2 md:space-x-0 items-center md:items-start"
        >
          <div class="flex items-baseline mt-1">
            <h2 class="text-2xl font-medium text-primary">{{ users }}</h2>
          </div>
          <h3 class="text-lg leading-6 font-medium text-gray-900">Users</h3>
        </div>

        <div
          class="rounded-md border flex-grow py-2 px-4 flex md:flex-col-reverse space-x-2 md:space-x-0 items-center md:items-start"
        >
          <div class="flex items-baseline mt-1">
            <h2 class="text-2xl font-medium text-primary">{{ tickets }}</h2>
          </div>
          <h3 class="text-lg leading-6 font-medium text-gray-900">Tickets</h3>
        </div>
      </div>
    </header>

    <div class="w-full border rounded-lg divide-y bg-white shadow">
      <div class="p-4">
        <SelectInput label="Inbox" :data="inboxes" v-model="selectedInbox" />
      </div>

      <InboxStats v-if="selectedInbox?.name" :key="selectedInbox" :inbox="selectedInbox" />
    </div>

    <div class="w-full border rounded-lg divide-y bg-white shadow mt-4 p-4">
      <div class="sm:flex sm:items-center">
        <div class="sm:flex-auto">
          <h1 class="text-base font-semibold leading-6 text-gray-900">Clients</h1>
          <p class="mt-2 text-sm text-gray-700">A list of all the clients and their deployments.</p>
        </div>
        <div class="mt-4 sm:ml-16 sm:mt-0 sm:flex-none">
          <button type="button" class="block rounded-md bg-primary-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600">Add group</button>
        </div>
      </div>
      <div class="mt-8 flow-root">
        <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
            <table class="min-w-full">
              <thead class="bg-white">
                <tr>
                  <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-3">Name</th>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">ID</th>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Description</th>
                  <th scope="col" class="relative py-3.5 pl-3 pr-4 sm:pr-3">
                    <span class="sr-only">Edit</span>
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white">
                <template v-for="group in configuration" :key="group.url">
                  <tr class="border-t border-gray-200">
                    <th colspan="3" scope="colgroup" class="bg-gray-100 py-2 pl-4 pr-3 text-left text-sm font-semibold text-primary sm:pl-3">{{ group.url }}</th>
                    <th class="bg-gray-100 flex space-x-2 justify-end relative whitespace-nowrap py-2 pl-3 pr-4 text-right text-sm font-medium sm:pr-3">
                      <a href="#" class="text-primary-600 hover:text-primary-700">
                        <PlusIcon class="h-5 w-5" />
                      </a>
                      <a href="#" class="text-gray-600 hover:text-gray-700">
                        <WrenchIcon class="h-5 w-5" />
                      </a>
                    </th>
                  </tr>
                  <template v-for="client in group.clients" :key="client.id">
                    <tr class="border-t border-gray-200">
                      <th scope="colgroup" class="bg-gray-50 py-2 pl-6 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-5">{{ client.name }}</th>
                      <th scope="colgroup" class="bg-gray-50 py-2 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-3">{{ client.id }}</th>
                      <th scope="colgroup" class="bg-gray-50 py-2 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-3">
                        <span v-if="client.default" class="inline-flex items-center rounded-md bg-green-50 px-1.5 py-0.5 text-xs font-medium text-green-700 ring-1 ring-inset ring-green-600/20">Default</span>
                      </th>
                      <th class="bg-gray-50 flex space-x-2 justify-end relative whitespace-nowrap py-2 pl-3 pr-4 text-right text-sm font-medium sm:pr-3">
                        <a href="#" class="text-primary-600 hover:text-primary-700">
                          <PlusIcon class="h-5 w-5" />
                        </a>
                        <a href="#" class="text-gray-600 hover:text-gray-700">
                          <WrenchIcon class="h-5 w-5" />
                        </a>
                      </th>
                    </tr>

                    <tr v-for="(deployment, deploymentIdx) in client.deployments" :key="deployment.email" :class="[deploymentIdx === 0 ? 'border-gray-300' : 'border-gray-200', 'border-t']">
                      <td class="whitespace-nowrap py-4 pl-8 pr-3 text-sm font-medium text-gray-900 sm:pl-7">{{ deployment.name }}</td>
                      <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ deployment.id }}</td>
                      <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ deployment.description }}</td>
                      <td class="relative flex space-x-2 justify-end whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-3">
                        <a href="#" class="text-gray-600 hover:text-gray-900">
                          <Squares2X2Icon class="h-5 w-5" />
                        </a>
                        <a href="#" class="text-gray-600 hover:text-gray-900">
                          <AdjustmentsHorizontalIcon class="h-5 w-5" />
                        </a>
                      </td>
                    </tr>
                  </template>
                </template>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import InboxStats from "@/components/admin/InboxStats.vue";
import SelectInput from "@/components/inputs/SelectInput.vue";
import axios from "axios";

import { AdjustmentsHorizontalIcon, CogIcon, Squares2X2Icon, PlusIcon, WrenchIcon } from "@heroicons/vue/24/outline";

const configuration = [
  {
    url: 'https://lti-ri.imsglobal.org',
    clients: [{
      name: 'LTI test link IMS Global',
      id: '123456789',
      default: true,
      deployments: [
        { name: 'Test tool', id: '1', description: 'Test tool from ims global' },
      ],
    }]
  },
  {
    url: 'https://canvas.instructure.com',
    clients: [{
      name: 'Canvas Test deployment',
      id: '10000000000003',
      default: true,
      deployments: [
        { name: 'Test deployment', id: '2:8865aa05b4b79b64a91a86042e43af5ea8ae79eb', description: 'Selfhosted digitalocean' },
      ],
    }]
  },
  {
    url: 'https://canvas.uva.nl',
    clients: [{
      name: 'Universiteit van Amsterdam',
      id: '654987321',
      default: true,
      deployments: [
        { name: 'Faculteit der Natuurwetenschappen, Wiskunde en Informatica', id: '65465138463219865463', description: 'Gehele FNWI' },
        { name: 'Faculteit der Rechtgeleerdheid', id: '186413843', description: 'Extra faculteit' },
      ],
    }]
  },
]

export default {
  components: {
    CogIcon,
    InboxStats,
    SelectInput,
    AdjustmentsHorizontalIcon,
    Squares2X2Icon,
    PlusIcon,
    WrenchIcon,
  },
  data: () => ({
    inboxes: [],
    users: 0,
    tickets: 0,
    selectedInbox: null,
    configuration
  }),
  async mounted() {
    axios.get("/api/inboxes").then((response) => {
      this.inboxes = response.data;
      this.selectedInbox = this.inboxes[0];
    });
    
    axios.get("/api/admin/statistics/users/count").then((response) => {
      this.users = response.data.users;
    });

    await axios.get("/api/admin/statistics/tickets/count").then((response) => {
      this.tickets = response.data.tickets;
    });
  },
};
</script>
