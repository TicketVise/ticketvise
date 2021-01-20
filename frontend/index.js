import Vue from 'vue'
import 'alpinejs'
import './email/index.js'
import App from "./App";
import store from "./store";
import router from "./router";

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
