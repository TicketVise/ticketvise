<template>
  <div class="grid grid-cols-3 gap-2 w-full">
    <SelectInput v-model="selectedType" :data="types" emptyLabel="Choose field" />
    <SelectInput v-model="selectedOption" :data="options" :emptyLabel="!selectedType ? 'First choose field' : 'Choose option'" :disabled="!selectedType" />
    <SelectInput v-if="selectedType?.input === 'labels'" v-model="selectedValue" :data="labels" :emptyLabel="!selectedType ? 'First choose field' : 'Choose value'" :disabled="!selectedType" />
    <div v-else-if="selectedType?.input === 'datetime'" class="mt-1">
      <input v-model="selectedValue" datepicker :id="`datepicker_${id}`" type="text" class="focus:ring-primary focus:border-primary block w-full sm:text-sm border-gray-300 rounded-md" placeholder="Select date">
    </div>
    <div v-else-if="selectedType?.input !== 'none'" class="mt-1">
      <label for="email" class="sr-only">Email</label>
      <input v-model="selectedValue" type="email" name="email" id="email" class="focus:ring-primary focus:border-primary block w-full sm:text-sm border-gray-300 rounded-md" :placeholder="!selectedType ? 'First choose field' : 'Choose value'" :disabled="!selectedType" />
    </div>
  </div>
</template>

<script>
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
    name: 'Public',
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
    condition: {
      type: Object,
      default: () => ({
        evaluation_func: '',
        evaluation_value: '',
        field_name: ''
      })
    }
  },
  data: () => ({
    id: '',
    inbox_id: window.location.pathname.split('/')[2],
    labels: [],
    options: [],
    selectedType: null,
    selectedOption: null,
    selectedValue: null
  }),
  setup () {
    return { types }
  },
  mounted () {
    axios.get(`/api/inboxes/${this.inbox_id}/labels/all`).then(response => {
      this.labels = response.data
    })

    this.selectedType = this.types.find(type => type.value === this.condition.field_name)

    if (this.selectedType) {
      this.selectedOption = this.selectedType.options.find(option => option.value === this.condition.evaluation_func)
      this.selectedValue = this.condition.evaluation_value
    }

    /* Set random id */
    this.id = Math.random().toString(36).substr(2, 9)

    /* Initialize datepicker */
    const datepickerEl = document.getElementById(`datepicker_${this.id}`)
    if (datepickerEl) {
      console.log('test')
      new Datepicker(datepickerEl)
    }
  },
  watch: {
    selectedType: {
      handler (value) {
        this.selectedType = value
        this.options = this.types.find(type => type.name === value?.name)?.options
      },
      immediate: true
    }
  }
}
</script>
