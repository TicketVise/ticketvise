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
import Profile from "./components/profile/Profile";
import Admin from "./components/admin/Admin";
import store from "./store";

const router = new VueRouter({
    routes: [
        {path: "/notifications", component: Notifications},
        {path: "/", component: Inboxes},
        {path: "/login", component: Login, name: "Login"},
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

router.beforeEach((to, from, next) => {
  if (to.name !== 'Login' && !store.getters.isAuthenticated) {
      next({ name: 'Login' })
  }
  else {
      next()
  }
})

export default router