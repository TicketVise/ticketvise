import router from '../../router'

const state = () => ({
  status: {
    active: false,
    popup: false,
    step: 0
  }
})

const actions = {
  start({ commit }) {
    commit('start')
  },
  next({ commit, state }) {
    commit('next')

    switch (state.status.step) {
      case 0:
        commit('open')
        break;
      case 1:
        commit('close')
        break;
      case 2:
        router.push('tickets')
        commit('close')
        break;
      case 3:
        router.push('public')
        commit('close')
        break;
      case 4:
        router.push('labels')
        commit('close')
        break;
    }
  }
}

const mutations = {
  start(state) {
    state.status.active = true
    state.status.popup = true
  },
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
