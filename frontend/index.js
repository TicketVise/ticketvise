import Vue from 'vue'
import Vuex from 'vuex'
import 'alpinejs'
import './email/index.js'
import VueRouter from 'vue-router'
import App from "./App";
import store from "./store";
import router from "./router";
import axios from 'axios'

Vue.use(Vuex)
Vue.use(VueRouter)

// global is declared using DefinePlugin in the webpack.config.js
if (typeof SENTRY_DSN !== 'undefined') {
    Sentry.init({
        dsn: SENTRY_DSN,
        integrations: [
            new VueIntegration({
                Vue,
                tracing: true,
                logErrors: true
            }),
            new Integrations.BrowserTracing()
        ],
        tracesSampleRate: 1 / 100
    });
}

axios.interceptors.request.use((config) => {
    const token = localStorage.getItem("token")
    if (token) {
        config.headers["Authorization"] = "Token " + token
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

/**
 * Load every vue single file components.
 */
const files = require.context('./components/', true, /\.vue$/i)
files.keys().map(key =>
    Vue.component(
        key.split('/')
            .pop()
            .split('.')[0],
        files(key).default
    )
)

new Vue({
    store: store,
    router: router,
    el: "#app",
    components: {App},
    template: "<App/>",
});