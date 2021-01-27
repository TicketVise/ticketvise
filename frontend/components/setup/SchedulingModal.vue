<template>
  <div>
    <div>
      <div class="mt-3 text-center sm:mt-5">
        <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-headline">
          Scheduling
        </h3>
        <div class="mt-2">
          <p class="text-sm text-gray-500">
            New tickets can automatically be assigned to teachers and assistants. This can be configured in the settings of
            the inbox. To prevent tickets to be assigned to teachers or assistants, you need to go to the Users tab. Here you
            can edit the user and change if they should be included in the scheduling. For users to be shown in the users
            tab, they first need to visit TicketVise from Canvas.
          </p>
        </div>
      </div>
    </div>
<!--    <fieldset>-->
<!--      <legend class="sr-only">Scheduling Algorithm</legend>-->
<!--      <div class="bg-white rounded-md -space-y-px">-->
<!--        <div class="relative border rounded-tl-md rounded-tr-md p-4 flex border-gray-200"-->
<!--             :class="bg-orange-50 border-orange-200 z-10': selected === 0, 'border-gray-200': selected !== 0 }">-->
<!--          <div class="flex items-center h-5"><input value="0" id="settings-option-0"-->
<!--                                                    name="privacy_setting" type="radio"-->
<!--                                                    class="focus:ring-primary h-4 w-4 text-orange-600 cursor-pointer border-gray-300">-->
<!--          </div>-->
<!--          <label for="settings-option-0" class="ml-3 flex flex-col cursor-pointer"><span-->
<!--                  class="block text-sm font-medium text-gray-900"-->
<!--                  :class="['text-orange-900': selected === 0, 'text-gray-900': selected !== 0 ]">Round Robin</span>-->
<!--            <span class="block text-sm text-gray-500"-->
<!--                  :class="{ 'text-orange-700': selected === 0, 'text-gray-500': selected !== 0 }">Go around the group and assign everyone a question</span></label>-->
<!--        </div>-->
<!--        &lt;!&ndash;  <div class="relative border p-4 flex border-gray-200" :class="{ 'bg-orange-50 border-orange-200 z-10': selected == 1, 'border-gray-200': selected != 1 }"><div class="flex items-center h-5"><input x-model="selected" value="1" id="settings-option-1" name="privacy_setting" type="radio" class="focus:ring-primary h-4 w-4 text-orange-600 cursor-pointer border-gray-300"></div><label for="settings-option-1" class="ml-3 flex flex-col cursor-pointer"><span class="block text-sm font-medium text-gray-900" :class="{ 'text-orange-900': selected == 1, 'text-gray-900': selected != 1 }">Least Assigned First</span>&ndash;&gt;-->
<!--        &lt;!&ndash;<span class="block text-sm text-gray-500" :class="{ 'text-orange-700': selected == 1, 'text-gray-500': selected != 1 }">Assign the question to the assistant with the least questions currently active</span></label></div><div class="relative border rounded-br-md p-4 flex border-gray-200" :class="{ 'bg-orange-50 border-orange-200 z-10': selected == 2, 'border-gray-200': selected != 2 }"><div class="flex items-center h-5"><input x-model="selected" value="2" id="settings-option-2" name="privacy_setting" type="radio" class="focus:ring-primary h-4 w-4 text-orange-600 cursor-pointer border-gray-300"></div><label for="settings-option-2" class="ml-3 flex flex-col cursor-pointer"><span class="block text-sm font-medium text-gray-900" :class="{ 'text-orange-900': selected == 2, 'text-gray-900': selected != 2 }">Workgroup / Section</span>&ndash;&gt;-->
<!--        &lt;!&ndash;<span class="block text-sm text-gray-500" :class="{ 'text-orange-700': selected == 2, 'text-gray-500': selected != 2 }">Assign the question to the corresponding workgroup assistant</span></label></div><div class="relative border rounded-bl-md rounded-br-md p-4 flex bg-orange-50 border-orange-200 z-10" :class="{ 'bg-orange-50 border-orange-200 z-10': selected == 3, 'border-gray-200': selected != 3 }"><div class="flex items-center h-5"><input x-model="selected" value="3" id="settings-option-3" name="privacy_setting" type="radio" class="focus:ring-primary h-4 w-4 text-orange-600 cursor-pointer border-gray-300"></div><label for="settings-option-3" class="ml-3 flex flex-col cursor-pointer"><span class="block text-sm font-medium text-orange-900" :class="{ 'text-orange-900': selected == 3, 'text-gray-900': selected != 3 }">Manual</span>&ndash;&gt;-->
<!--        &lt;!&ndash;<span class="block text-sm text-orange-700" :class="{ 'text-orange-700': selected == 3, 'text-gray-500': selected != 3 }">Don't assign anyone and let the assistant pick up questions themselfs.</span></label></div></div></fieldset>&ndash;&gt;-->

        <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
          <button type="button" @click="$emit('click')"
                  class="w-full inline-flex justify-center rounded-md px-4 py-2 bg-primary text-base font-medium text-white hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 sm:col-start-2 sm:text-sm">
            Continue
          </button>
          <button type="button" @click="$emit('cancel')"
                  class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:col-start-1 sm:text-sm">
            Back
          </button>
        </div>
      </div>
</template>

<script>
  export default {
    name: "SchedulingModal"
  }
</script>

<style scoped>

</style>