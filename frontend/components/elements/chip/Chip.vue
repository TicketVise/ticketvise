<template>
  <span class="inline-block bg-gray-200 rounded-full px-2 py-1 text-xs font-semibold text-gray-700"
        :style="style" style="line-height: 1 !important;">
    <slot></slot>
  </span>
</template>

<script>
  export default {
    props: {
      background: {
        type: String,
        default: null,
        required: false
      }
    },
    data() {
      return {
        style: {
          backgroundColor: this.background,
          color: this.getFontColor(this.background)
        },
      }
    },
    methods: {
      getFontColor(hexcolor) {
        if (hexcolor.slice(0, 1) === '#') {
          hexcolor = hexcolor.slice(1);
        }

        let r = parseInt(hexcolor.substr(0, 2), 16);
        let g = parseInt(hexcolor.substr(2, 2), 16);
        let b = parseInt(hexcolor.substr(4, 2), 16);
        let brightness = ((r * 299) + (g * 587) + (b * 114)) / 1000;
        return (brightness >= 128) ? "#374151" : "#ffffff";
      }
    }
  }
</script>

<style>

</style>
