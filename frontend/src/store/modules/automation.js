const state = () => ({
  filters: []
})

const actions = {}

const mutations = {
  newFilter (state) {
    state.filters.push({
      id: -1,
      name: '',
      open: true,
      conditions: []
    })
  },
  updateFilters (state, filters) {
    state.filters = filters
  },
  setConditionField (state, { filterId, condition, fieldName }) {
    state.filters.find(f => f.id === filterId).conditions.find(c => c.id === condition.id).field_name = fieldName
  },
  setConditionEvaluationFunc (state, { filterId, condition, evaluationFunc }) {
    state.filters.find(f => f.id === filterId).conditions.find(c => c.id === condition.id).evaluation_func = evaluationFunc
  },
  setConditionEvaluationValue (state, { filterId, condition, evaluationValue }) {
    state.filters.find(f => f.id === filterId).conditions.find(c => c.id === condition.id).evaluation_value = evaluationValue
  },
  setActionFunc (state, { filterId, actionFunc }) {
    state.filters.find(f => f.id === filterId).action_func = actionFunc
  },
  setActionValue (state, { filterId, actionValue }) {
    state.filters.find(f => f.id === filterId).action_value = actionValue
  },
  removeFilterCondition (state, { filterId, conditionId }) {
    const index = state.filters.find(f => f.id === filterId).conditions.findIndex(c => c.id === conditionId)
    state.filters.find(f => f.id === filterId).conditions.splice(index, 1)
  },
  updateFilterId (state, { filterId }) {
    state.filters.find(f => f.id === -1).id = filterId
  }
}

const getters = {
  getFilters (state) {
    return state.filters
  },
  getFilter (state, id) {
    return state?.filters?.find(filter => filter.id === id)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
