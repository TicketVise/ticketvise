import VueRouter from "vue-router";
import Notifications from "./components/notifications/Notifications";
import Inboxes from "./components/inbox/Inboxes";
import Login from "./components/Login";
import TicketOverview from "./components/inbox/TicketOverview";
import TicketForm from "./components/ticket/TicketForm";
import Ticket from "./components/ticket/Ticket";
import InboxStatistics from "./components/inbox_statistics/InboxStatistics";
import InboxSettings from "./components/inbox/InboxSettings";
import Users from "./components/inbox/Users";
import User from "./components/inbox/User";
import Labels from "./components/inbox/Labels";
import Label from "./components/inbox/Label";
import Account from "./components/account/Account";
import Admin from "./components/admin/Admin";
import store from "./store";
import Inbox from "./components/inbox/Inbox";
import Vue from "vue";

Vue.use(VueRouter)

const router = new VueRouter({
    routes: [
        { path: "/notifications", component: Notifications, name: "Notifications" },
        { path: "/", redirect: { name: "Login" } },
        { path: "/login", component: Login, name: "Login", meta: { layout: "auth-form" } },
        { path: "/inboxes", component: Inboxes, name: "Inboxes", meta: { layout: "thick-header" } },
        {
            path: "/inboxes/:inboxId",
            component: Inbox,
            redirect: { name: "Inbox" },
            children: [
                { path: "tickets", component: TicketOverview, name: "Inbox", meta: { layout: "inbox" } },
                { path: "tickets/new", component: TicketForm, name: "NewTicket", meta: { layout: "inbox" } },
                { path: "statistics", component: InboxStatistics, name: "InboxStatistics", meta: { layout: "inbox" } },
                { path: "settings", component: InboxSettings, name: "InboxSettings", meta: { layout: "inbox" } },
                { path: "users", component: Users, name: "InboxUsers", meta: { layout: "inbox" } },
                { path: "users/:userId", component: User, name: "InboxUser", meta: { layout: "inbox" } },
                { path: "labels", component: Labels, name: "InboxLabels", meta: { layout: "inbox" } },
                { path: "labels/:labelId", component: Label, name: "InboxLabel", meta: { layout: "inbox" } },
            ]
        },
        { path: "/inboxes/:inboxId/tickets/:ticketInboxId", component: Ticket, name: "Ticket" },
        { path: "/account", component: Account, name: "Account" },
        { path: "/admin", component: Admin, name: "Admin" }
    ]
})

router.beforeEach((to, from, next) => {
    if (to.name !== 'Login' && !store.getters.isAuthenticated) {
        next({ name: 'Login' })
    } else if (to.name === "Login" && store.getters.isAuthenticated) {
        next({ name: "Inboxes" })
    } else {
        next()
    }
})

export default router
