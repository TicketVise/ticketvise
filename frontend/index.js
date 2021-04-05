import Vue from 'vue'
import 'alpinejs'
import './email/index.js'
import App from "./App";
import store from "./store";
import router from "./router";

import './styles/index.scss'

/**
 * Load every vue single file components.
 */
let files = require.context('./components/', true, /\.vue$/i)
files.keys().map(key =>
    Vue.component(
        key.split('/')
            .pop()
            .split('.')[0],
        files(key).default
    )
)

/* Load layout components. */
files = require.context('./layouts/components/', true, /\.vue$/i)
files.keys().map(key =>
    Vue.component(
        key.split('/')
            .pop()
            .split('.')[0],
        files(key).default
    )
)

/**
 * Load the different layouts in.
 */
import Default from "./layouts/Default.vue"
import ThickHeader from "./layouts/ThickHeader.vue"
import AuthForm from "./layouts/AuthForm.vue"
import Inbox from "./layouts/Inbox.vue"

Vue.component('default-layout', Default);
Vue.component('thick-header-layout', ThickHeader);
Vue.component('auth-form-layout', AuthForm);
Vue.component('inbox-layout', Inbox);

/**
 * Create the VueJS instance.
 */
new Vue({
    store: store,
    router: router,
    el: "#app",
    components: {App},
    template: "<App/>",
});
