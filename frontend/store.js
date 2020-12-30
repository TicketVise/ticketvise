import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import router from "./router";

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        user: null,
    },
    mutations: {
        auth_success(state, user) {
            state.user = user
        },
        unauth_success(state) {
            state.user = null
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
                        localStorage.setItem('token', resp.data.token)
                        commit('auth_success', resp.data.user)
                        router.push({name: 'Inboxes'})
                        resolve(resp)
                    })
                    .catch(err => {
                        localStorage.removeItem('token')
                        reject(err)
                    })
            })
        },
        relogin({commit}, inboxIdValue) {
            return new Promise((resolve, reject) => {
                axios.get('/api/me')
                    .then(resp => {
                        commit('auth_success', resp.data)
                        if (inboxIdValue) {
                            router.push({name: 'Inbox', params: {inboxId: inboxIdValue}})
                        } else {
                            router.push({name: 'Inboxes'})
                        }
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
            commit('unauth_success')
            router.push({name: 'Login'})
        }
    },
    getters: {
        isAuthenticated: state => !!state.user,
    }
})