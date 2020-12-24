import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import router from "./router";

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        token: localStorage.getItem('token') || '',
        user: {},
    },
    mutations: {
        auth_success(state, token, user) {
            state.token = token
            state.user = user
        },
        unauth_success(state) {
            state.token = ''
            state.user = {}
        },
    },
    actions: {
        login({commit}, payload) {
            return new Promise((resolve, reject) => {
                const data = {
                    "username": payload.username,
                    "password": payload.password
                }

                axios.post('/api/login', data)
                    .then(resp => {
                        const token = resp.data.token
                        const user = resp.data.user
                        localStorage.setItem('token', token)
                        axios.defaults.headers.common['Authorization'] = "Token " + token
                        commit('auth_success', token, user)
                        router.push({ path: 'inboxes', query: { plan: 'private' } })
                        resolve(resp)
                    })
                    .catch(err => {
                        localStorage.removeItem('token')
                        reject(err)
                    })
            })
        },
        logout({commit}) {
            localStorage.removeItem('token')
            axios.defaults.headers.common['Authorization'] = ""
            commit('unauth_success')
            router.push({ path: 'login' })
        }
    },
    getters: {
        isAuthenticated: state => !!state.token,
    }
})