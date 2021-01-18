import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import router from "./router";
import {hasLocalStorage} from "./utils";

const TOKEN_KEY = "token"
const urlQueryParams = new URLSearchParams(window.location.search);
const urlToken = urlQueryParams.get(TOKEN_KEY)

if (urlToken && hasLocalStorage) {
    localStorage.setItem(TOKEN_KEY, urlToken)
}

Vue.use(Vuex);

const store = new Vuex.Store({
    state: {
        token: urlToken || (hasLocalStorage ? localStorage.getItem(TOKEN_KEY) : null),
        user: {},
    },
    mutations: {
        auth_success(state, user) {
            state.user = user
        },
        update_token(state, token) {
            if (hasLocalStorage) {
                localStorage.setItem(TOKEN_KEY, token)
            }
            console.log(localStorage.getItem(TOKEN_KEY))

            state.token = token
        },
        unauth_success(state) {
            if (hasLocalStorage) {
                localStorage.removeItem(TOKEN_KEY)
            }

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
        sync({commit}) {
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
        logout({commit}) {
            commit('unauth_success')
            router.push({name: 'Login'})
        }
    },
    getters: {
        isAuthenticated: state => !!state.token
    }
})

axios.interceptors.request.use((config) => {
    if (store.getters.isAuthenticated) {
        config.headers["Authorization"] = "Token " + store.state.token
    }

    return config;
});

axios.interceptors.response.use(response => response, error => {
    if (error.response && error.response.status === 401) {
        store.dispatch("logout")
    } else {
        return Promise.reject(error);
    }
});

// Check if launched from LTI (when 'token' query param is in URL)
if (urlToken) {
    // Remove token parameter from URL.
    const url = new URL(window.location.href)
    url.searchParams.delete(TOKEN_KEY)

    window.history.replaceState({}, document.title, url.href);
}

if (store.getters.isAuthenticated) {
    // Sync user data.
    store.dispatch("sync")
}

export default store