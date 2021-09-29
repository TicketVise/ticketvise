<script>
import { defineComponent } from 'vue'
import { HorizontalBar } from 'vue3-chart-v2'

export default defineComponent({
  name: 'HorizontalBarChart',
  extends: HorizontalBar,
  props: {
    data: {
      type: Object,
      default: null
    },
    options: {
      type: Object,
      default: null
    }
  },
  mounted () {
    this.renderChart(this.data, this.options)
  }
})
</script>
