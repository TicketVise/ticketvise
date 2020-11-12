import Vue from 'vue'
import Vuex from 'vuex'
import 'alpinejs'
import './email/index.js'
import Notifications from "./components/notifications/Notifications";
import Inboxes from "./components/inbox/Inboxes";
import TicketOverview from "./components/inbox/TicketOverview";
import InboxSettings from "./components/inbox/InboxSettings";
import InboxStatistics from "./components/inbox_statistics/InboxStatistics";
import Ticket from "./components/ticket/Ticket";
import Users from "./components/inbox/Users";
import User from "./components/inbox/User";
import Labels from "./components/inbox/Labels";
import Label from "./components/inbox/Label";
import Profile from "./components/profile/Profile";
import Admin from "./components/admin/Admin";
import TicketForm from "./components/ticket/TicketForm";
import VueRouter from 'vue-router'
import App from "./App";
import Login from "./components/Login";
import store from "./store";
import router from "./router";

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