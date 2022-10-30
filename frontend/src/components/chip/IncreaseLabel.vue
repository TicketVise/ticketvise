<template>
  <!-- <span v-if="b !== 0" class="px-2 py-1 text-sm rounded-full"
        :class="{
          'bg-green-200 text-green-700': value < 0,
          'bg-red-200 text-red-700': value > 0,
          'bg-gray-200 text-gray-700': value === 0,
        }">
    <i v-if="value > 0" class="fa fa-arrow-up"></i>
    <i v-else-if="value < 0" class="fa fa-arrow-down"></i>
    <i v-else class="fa fa-minus"></i>
    <span class="ml-2 font-medium ">
      {{ value }}
    </span>
  </span> -->
  <div
    :class="[
      value === 0
        ? 'bg-gray-100 text-gray-800'
        : value > 0
        ? 'bg-green-100 text-green-800'
        : 'bg-red-100 text-red-800',
      'inline-flex items-baseline px-2.5 py-0.5 rounded-full text-sm font-medium md:mt-2 lg:mt-0',
    ]"
  >
    <MinusIcon
      v-if="value === 0"
      class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5 text-gray-500"
      aria-hidden="true"
    />
    <ArrowSmallUpIcon
      v-else-if="value > 0"
      class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5 text-green-500"
      aria-hidden="true"
    />
    <ArrowSmallDownIcon
      v-else
      class="-ml-1 mr-0.5 flex-shrink-0 self-center h-5 w-5 text-red-500"
      aria-hidden="true"
    />
    <span class="sr-only">
      {{ value > 0 ? "Increased" : "Decreased" }} by
    </span>
    {{ value }}%
  </div>
</template>

<script>
import {
  ArrowSmallDownIcon,
  ArrowSmallUpIcon,
  MinusIcon,
} from "@heroicons/vue/24/solid";

export default {
  name: "IncreaseLabel",
  components: {
    ArrowSmallDownIcon,
    ArrowSmallUpIcon,
    MinusIcon,
  },
  props: {
    a: {
      required: true,
      type: Number,
    },
    b: {
      required: true,
      type: Number,
    },
  },
  computed: {
    value() {
      if (this.a === this.b) {
        return 0;
      }
      if (this.b === 0) {
        return "100.00";
      }

      const increase = this.a - this.b;

      return ((increase / this.b) * 100).toFixed(2);
    },
  },
};
</script>
