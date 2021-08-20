<template>
  <div class="flex-1 min-w-0">
    <label for="search" class="sr-only">Search</label>
    <div class="relative rounded-md border border-gray-300">
      <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <!-- Heroicon name: solid/search -->
        <svg
          class="h-5 w-5 text-gray-400"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
          aria-hidden="true"
        >
          <path
            fill-rule="evenodd"
            d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
            clip-rule="evenodd"
          />
        </svg>
      </div>
      <input
        name="search"
        id="search"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        class="focus:ring-primary focus:border-primary block w-full p-2 pl-10 rounded-md dark:bg-gray-800 dark:text-white"
        :class="{ 'text-sm': small }"
        placeholder="Search"
      />
    </div>
  </div>
</template>

<script>
  export default {
    name: 'SearchBar',
    emits: ['update:modelValue'],
    props: {
      small: {
        required: false,
        type: Boolean,
        default: false
      },
      modelValue: {
          type: String,
          default: '',
          required: true
      }
    }
  }
</script>
