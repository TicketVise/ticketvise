<template>
  <div class="grid grid-cols-3 gap-2 w-full">
    <SelectInput v-model="selectedType" :data="types" emptyLabel="Choose field" />
    <SelectInput v-model="selectedOption" :data="options" :emptyLabel="!selectedType ? 'First choose field' : 'Choose option'" :disabled="!selectedType" />
    <SelectInput v-if="selectedType?.input === 'labels'" v-model="selectedValue" :data="labels" :emptyLabel="!selectedType ? 'First choose field' : 'Choose value'" :disabled="!selectedType" />
    <div v-else-if="selectedType?.input === 'datetime'" class="mt-1">
      <input v-model="selectedValue" datepicker :id="`datepicker_${id}`" type="text" class="focus:ring-primary focus:border-primary block w-full sm:text-sm border-gray-300 rounded-md" placeholder="Select date">
    </div>
    <div v-else-if="selectedType?.input !== 'none'" class="mt-1">
      <label for="value" class="sr-only">Value</label>
      <input required v-model="selectedValue" type="text" name="value" id="value" class="focus:ring-primary focus:border-primary block w-full sm:text-sm border-gray-300 rounded-md" :placeholder="!selectedType ? 'First choose field' : 'Choose value'" :disabled="!selectedType" />
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import axios from 'axios'
import SelectInput from '@/components/inputs/SelectInput'

import Datepicker from '@themesberg/tailwind-datepicker/dist/js/datepicker'

const types = [
  {
    name: 'Title',
    value: 'title',
    options: [
      { name: 'Contains', value: 'contains' },
      { name: 'Contains not', value: 'contains_not' },
      { name: 'Equals', value: 'equals' }
    ],
    input: 'text'
  },
  {
    name: 'Content',
    value: 'content',
    options: [
      { name: 'Contains', value: 'contains' },
      { name: 'Contains not', value: 'contains_not' },
      { name: 'Equals', value: 'equals' }
    ],
    input: 'text'
  },
  {
    name: 'Labels',
    value: 'labels',
    options: [
      { name: 'Contains', value: 'contains' },
      { name: 'Contains not', value: 'contains_not' },
      { name: 'Equals', value: 'equals' }
    ],
    input: 'labels'
  },
  {
    name: 'Is public',
    value: 'is_public',
    options: [
      { name: 'True', value: 'true' },
      { name: 'False', value: 'false' }
    ],
    input: 'none'
  },
  {
    name: 'Created at',
    value: 'date_created',
    options: [
      { name: 'Greater than', value: 'gt' },
      { name: 'Greater than or equal', value: 'ge' },
      { name: 'Less than', value: 'lt' },
      { name: 'Less than or equal', value: 'le' },
      { name: 'Equals', value: 'eq' }
    ],
    input: 'datetime'
  }
]

export default {
  name: 'AutomationCondition',
  components: {
    SelectInput
  },
  props: {
    filterId: {
      required: true,
      type: Number
    },
    conditionId: {
      required: false,
      type: Number
    }
  },
  data: () => ({
    id: '',
    inbox_id: window.location.pathname.split('/')[2],
    labels: [],
    options: []
  }),
  setup () {
    return { types }
  },
  async mounted () {
    await axios.get(`/api/inboxes/${this.inbox_id}/labels/all`).then(response => {
      this.labels = response.data
    })

    /* Set random id */
    // this.id = Math.random().toString(36).substr(2, 9)

    /* Initialize datepicker */
    // const datepickerEl = document.getElementById(`datepicker_${this.id}`)
    // if (datepickerEl) {
    //   console.log('test')
    //   new Datepicker(datepickerEl)
    // }
  },
  watch: {
    selectedType: {
      handler (newType, oldType) {
        if (oldType === newType) return
        if (!newType) return

        this.options = newType.options

        if (newType.input === 'labels') this.selectedValue = this.labels[0]
        else this.selectedValue = ''
      },
      deep: true
    },
    selectedOption: {
      handler (newOption) {
        if (!newOption) return

        if (this.selectedType.value === 'is_public')
          this.selectedValue = newOption.value === 'true' ? true : false
      }
    }
  },
  computed: {
    ...mapState('automation', {
      condition (state) {
        return state.filters?.find(filter => parseInt(filter.id) === parseInt(this.filterId))?.conditions.find(condition => parseInt(condition.id) === parseInt(this.conditionId))
      }
    }),
    selectedType: {
      get () {
        return this.types.find(type => type.value === this.condition?.field_name)
      },
      set (value) {
        this.$store.commit('automation/setConditionField', {
          filterId: this.filterId,
          condition: this.condition,
          fieldName: value.value
        })
      }
    },
    selectedOption: {
      get () {
        return this.selectedType?.options.find(option => option.value === this.condition?.evaluation_func)
      },
      set (value) {
        this.$store.commit('automation/setConditionEvaluationFunc', {
          filterId: this.filterId,
          condition: this.condition,
          evaluationFunc: value?.value
        })
      }
    },
    selectedValue: {
      get () {
        if (this.selectedType?.input === 'labels')
          return this.labels.find(label => parseInt(label.id) === parseInt(this.condition?.evaluation_value))

        return this.condition?.evaluation_value
      },
      set (value) {
        if (this.selectedType?.input === 'labels') value = value.id
        this.$store.commit('automation/setConditionEvaluationValue', {
          filterId: this.filterId,
          condition: this.condition,
          evaluationValue: value
        })
      }
    }
  }
}
</script>
