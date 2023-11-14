import router from '../../router'

const state = () => ({
  status: {
    active: false,
    popup: false,
    step: 0
  }
})

const actions = {
  next({ commit, state }) {
    commit('next')

    if (state.status.step === 0) {
      commit('open')
    }
    if (state.status.step === 1) {
      commit('close')
    }
    if (state.status.step === 2) {
      router.push('tickets')
      commit('close')
    }
  }
}

const mutations = {
  next(state) {
    state.status.step++
  },
  prev(state) {
    state.status.step--
  },
  open(state) {
    state.status.popup = true
  },
  close(state) {
    state.status.popup = false
  }
}

const getters = {}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
