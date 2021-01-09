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

const router = new VueRouter({
    routes: [
        {path: "/notifications", component: Notifications},
        {path: "/", component: Inboxes},
        {path: "/login", component: Login, name: "Login"},
        {path: "/inboxes", component: Inboxes, name: "Inboxes"},
        {
            path: "/inboxes/:inboxId",
            component: Inbox,
            children: [
                {path: "tickets", component: TicketOverview, name: "Inbox"},
                {path: "tickets/new", component: TicketForm},
                {path: "statistics", component: InboxStatistics},
                {path: "settings", component: InboxSettings},
                {path: "users", component: Users},
                {path: "users/:userId", component: User},
                {path: "labels", component: Labels},
                {path: "labels/:labelId", component: Label},
            ]
        },
        {path: "/inboxes/:inboxId/tickets/:ticketInboxId", component: Ticket},
        {path: "/account", component: Account},
        {path: "/admin", component: Admin}
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