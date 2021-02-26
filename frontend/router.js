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
import PublicTickets from "./components/inbox/PublicTickets";

Vue.use(VueRouter)

const router = new VueRouter({
    routes: [
        {path: "/notifications", component: Notifications, name: "Notifications"},
        {path: "/", component: Inboxes, name: "Home"},
        {path: "/login", component: Login, name: "Login"},
        {path: "/inboxes", component: Inboxes, name: "Inboxes"},
        {
            path: "/inboxes/:inboxId",
            component: Inbox,
            children: [
                {path: "tickets", component: TicketOverview, name: "Inbox"},
                {path: "public", component: PublicTickets, name: "Public"},
                {path: "tickets/new", component: TicketForm, name: "NewTicket"},
                {path: "statistics", component: InboxStatistics, name: "InboxStatistics"},
                {path: "settings", component: InboxSettings, name: "InboxSettings"},
                {path: "users", component: Users, name: "InboxUsers"},
                {path: "users/:userId", component: User, name: "InboxUser"},
                {path: "labels", component: Labels, name: "InboxLabels"},
                {path: "labels/:labelId", component: Label, name: "InboxLabel"},
            ]
        },
        {path: "/inboxes/:inboxId/tickets/:ticketInboxId", component: Ticket, name: "Ticket"},
        {path: "/account", component: Account, name: "Account"},
        {path: "/admin", component: Admin, name: "Admin"}
    ]
})

router.beforeEach((to, from, next) => {
    if (to.name !== 'Login' && !store.getters.isAuthenticated) {
        next({name: 'Login'})
    } else if (to.name === "Login" && store.getters.isAuthenticated) {
        next({name: "Inboxes"})
    } else {
        next()
    }
})

export default router