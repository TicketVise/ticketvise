import { createStore } from 'vuex'
import router from '@/router'
import axios from 'axios'

import automation from '@/store/modules/automation'
import onboarding from '@/store/modules/onboarding'

const TOKEN_KEY = 'token'
const urlQueryParams = new URLSearchParams(window.location.search)
const urlToken = urlQueryParams.get(TOKEN_KEY)

function isLocalStorageAvailable () {
  // https://stackoverflow.com/questions/16427636/check-if-localstorage-is-available
  if (typeof localStorage !== 'undefined') {
    try {
      localStorage.setItem('feature_test', 'yes')
      if (localStorage.getItem('feature_test') === 'yes') {
        localStorage.removeItem('feature_test')
        return true
      } else {
        return false
      }
    } catch (e) {
      return false
    }
  }

  return false
}

const store = createStore({
  state: {
    token: urlToken || (isLocalStorageAvailable() ? localStorage.getItem(TOKEN_KEY) : null),
    user: {},
    inboxes: []
  },
  mutations: {
    auth_success (state, user) {
      state.user = user
    },
    update_token (state, token) {
      if (isLocalStorageAvailable()) localStorage.setItem(TOKEN_KEY, token)

      state.token = token
    },
    unauth_success (state) {
      if (isLocalStorageAvailable()) localStorage.removeItem(TOKEN_KEY)

      state.user = {}
      state.token = null
    },
    update_inboxes (state, inboxes) {
      state.inboxes = inboxes
    },
    update_tickets (state, payload) {
      // if (state.user.is_superuser) return
      state.inboxes.find(i => i.id === parseInt(payload.inbox)).tickets = payload.tickets
    },
    update_public_tickets (state, payload) {
      // if (state.user.is_superuser) return
      state.inboxes.find(i => i.id === parseInt(payload.inbox)).public_tickets = payload.public_tickets
    }
  },
  actions: {
    login ({ commit }, payload) {
      return new Promise((resolve, reject) => {
        const data = {
          username: payload.username,
          password: payload.password
        }

        axios.post('/api/login', data)
          .then(resp => {
            commit('update_token', resp.data.token)
            commit('auth_success', resp.data.user)
            router.go({ name: 'Dashboard' })
            resolve(resp)
          })
          .catch(err => {
            commit('unauth_success')
            reject(err)
          })
      })
    },
    sync ({ commit }) {
      return new Promise((resolve, reject) => {
        axios.get('/api/me')
          .then(resp => {
            commit('auth_success', resp.data)
            resolve(resp)
          })
          .catch(err => {
            commit('unauth_success')
            reject(err)
          })
      })
    },
    logout ({ commit }) {
      commit('unauth_success')
      router.push({ name: 'Login' })
    },
    async update_inboxes ({ commit, state }) {
      if (state.user.is_superuser) {
        const response = await axios.get('/api/inboxes')
        commit('update_inboxes', response.data)
      } else {
        const response = await axios.get('/api/me/inboxes')
        commit('update_inboxes', response.data.map(inbox => inbox.inbox))
      }
    },
    demo_tickets ({ commit, state }, payload) {
      const ticket = {
        id: 1,
        ticket_inbox_id: 1,
        title: 'Example ticket',
        date_created: Date.now(),
        author: { first_name: 'John', last_name: 'Doe' },
        assignee: payload.status !== 'pending' ? state.user : null,
        labels: [
          {
            id: 1,
            name: 'General',
            color: '#9061F9'
          }
        ]
      }
      const inbox = {
        inbox: payload.inboxId,
        tickets: [
          {
            label: 'Pending',
            total: 1,
            tickets: payload.status === 'pending' ? [ticket] : []
          },
          {
            label: 'Assigned',
            total: 0,
            tickets: payload.status === 'assigned' ? [ticket] : []
          },
          {
            label: 'Awaiting response',
            total: 0,
            tickets: payload.status === 'awaiting' ? [ticket] : []
          },
          {
            label: 'Closed',
            total: 0,
            tickets: payload.status === 'closed' ? [ticket] : []
          }
        ]
      }

      commit('update_tickets', inbox)
    }
  },
  getters: {
    isAuthenticated: state => !!state.token,
    inbox: (state) => (id) => state.inboxes.find(i => i.id === parseInt(id))
  },
  modules: {
    automation,
    onboarding
  }
})

axios.interceptors.request.use((config) => {
  if (store.getters.isAuthenticated) {
    config.headers.Authorization = 'Token ' + store.state.token
  }

  return config
})

axios.interceptors.response.use(response => response, error => {
  if (error.response && error.response.status === 401) {
    store.dispatch('logout')
  } else {
    return Promise.reject(error)
  }
})

// Check if launched from LTI (when 'token' query param is in URL)
if (urlToken) {
  // Remove token parameter from URL.
  const url = new URL(window.location.href)
  url.searchParams.delete(TOKEN_KEY)

  if (isLocalStorageAvailable()) localStorage.setItem(TOKEN_KEY, urlToken)

  window.history.replaceState({}, document.title, url.href)
}

// Sync user data.
if (store.getters.isAuthenticated) store.dispatch('sync')

export default store
