import Vue from 'vue'
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

const router = new VueRouter({
    routes: [
        {path: "/notifications", component: Notifications},
        {path: "/", component: Inboxes},
        {path: "/login", component: Login},
        {path: "/inboxes", component: Inboxes},
        {path: "/inboxes/:inboxId/tickets", component: TicketOverview},
        {path: "/inboxes/:inboxId/tickets/new", component: TicketForm},
        {path: "/inboxes/:inboxId/tickets/:ticketInboxId", component: Ticket},
        {path: "/inboxes/:inboxId/statistics", component: InboxStatistics},
        {path: "/inboxes/:inboxId/settings", component: InboxSettings},
        {path: "/inboxes/:inboxId/users", component: Users},
        {path: "/inboxes/:inboxId/users/:userId", component: User},
        {path: "/inboxes/:inboxId/labels", component: Labels},
        {path: "/inboxes/:inboxId/labels/:labelId", component: Label},
        {path: "/profile", component: Profile},
        {path: "/admin", component: Admin}
    ]
})

window.Vue = Vue
window.axios = require('axios')
Vue.config.productionTip = false

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
    router,
    el: "#app",
    components: {App},
    template: "<App/>",
});