import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import router from "./router";

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        token: localStorage.getItem('token'),
        user: {},
    },
    mutations: {
        auth_success(state, user) {
            state.user = user
        },
        update_token(state, token) {
            localStorage.setItem("token", token)
            state.token = token
        },
        unauth_success(state) {
            localStorage.removeItem('token')
            state.user = {}
            state.token = null
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
                        commit("update_token", resp.data.token)
                        commit('auth_success', resp.data.user)
                        router.push({name: 'Inboxes'})
                        resolve(resp)
                    })
                    .catch(err => {
                        commit('unauth_success')
                        reject(err)
                    })
            })
        },
        relogin({commit}, {token, inboxId}) {
            commit("update_token", token)

            return new Promise((resolve, reject) => {
                axios.get('/api/me')
                    .then(resp => {
                        commit('auth_success', resp.data)
                        if (inboxId) {
                            router.push({name: 'Inbox', params: {inboxId: inboxId}})
                        } else if (!window.location.hash) {
                            router.push({name: 'Inboxes'})
                        }

                        resolve(resp)
                    })
                    .catch(err => {
                        commit('unauth_success')
                        reject(err)
                    })
            })
        },
        logout({commit}) {
            commit('unauth_success')
            router.push({name: 'Login'})
        }
    },
    getters: {
        isAuthenticated: state => !!state.token
    }
})