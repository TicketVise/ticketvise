import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

const routes = [
  {
    path: '/',
    name: 'Home',
    redirect: {
      name: 'Login'
    }
  },
  {
    path: '/login',
    name: 'Login',
    // route level code-splitting
    // this generates a separate chunk (login.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "login" */ '@/views/Login.vue'),
    meta: {
      layout: 'AppLayoutAuth'
    }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import(/* webpackChunkName: "dashboard" */ '@/views/Dashboard.vue'),
    meta: {
      layout: 'AppLayoutGeneral'
    }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import(/* webpackChunkName: "admin" */ '@/views/Admin.vue'),
    meta: {
      layout: 'AppLayoutGeneral'
    }
  },
  {
    path: '/account',
    name: 'Account',
    component: () => import(/* webpackChunkName: "account" */ '@/views/Account.vue'),
    meta: {
      layout: 'AppLayoutGeneral'
    }
  },
  {
    path: '/notifications',
    name: 'Notifications',
    component: () => import(/* webpackChunkName: "notifications" */ '@/views/Notifications.vue'),
    meta: {
      layout: 'AppLayoutGeneral'
    }
  },
  {
    path: '/inboxes/:inboxId/overview',
    name: 'Overview',
    component: () => import(/* webpackChunkName: "overview" */ '@/views/Overview.vue'),
    meta: {
      layout: 'AppLayoutInbox'
    }
  },
  {
    path: '/inboxes/:inboxId/tickets',
    name: 'Tickets',
    component: () => import(/* webpackChunkName: "tickets" */ '@/views/Tickets.vue'),
    meta: {
      layout: 'AppLayoutInbox'
    }
  },
  {
    path: '/inboxes/:inboxId/tickets/:ticketInboxId',
    name: 'Ticket',
    component: () => import(/* webpackChunkName: "ticket" */ '@/views/Ticket.vue'),
    meta: {
      layout: 'AppLayoutTicket'
    }
  },
  {
    path: '/inboxes/:inboxId/tickets/new',
    name: 'Create',
    component: () => import(/* webpackChunkName: "create" */ '@/views/Create.vue'),
    meta: {
      layout: 'AppLayoutTicket'
    }
  },
  {
    path: '/inboxes/:inboxId/public',
    name: 'Public',
    component: () => import(/* webpackChunkName: "public" */ '@/views/Public.vue'),
    meta: {
      layout: 'AppLayoutInbox'
    }
  },
  {
    path: '/inboxes/:inboxId/users',
    name: 'Users',
    component: () => import(/* webpackChunkName: "users" */ '@/views/Users.vue'),
    meta: {
      layout: 'AppLayoutInbox'
    }
  },
  {
    path: '/inboxes/:inboxId/agents',
    name: 'Agents',
    component: () => import(/* webpackChunkName: "agents" */ '@/views/Agents.vue'),
    meta: {
      layout: 'AppLayoutInbox'
    }
  },
  {
    path: '/inboxes/:inboxId/users/:userId',
    name: 'User',
    component: () => import(/* webpackChunkName: "users" */ '@/views/Users.vue'),
    meta: {
      layout: 'AppLayoutInbox'
    }
  },
  {
    path: '/inboxes/:inboxId/labels',
    name: 'Labels',
    component: () => import(/* webpackChunkName: "labels" */ '@/views/Labels.vue'),
    meta: {
      layout: 'AppLayoutInbox'
    }
  },
  {
    path: '/inboxes/:inboxId/labels/:labelId',
    name: 'Label',
    component: () => import(/* webpackChunkName: "label" */ '@/views/Label.vue'),
    meta: {
      layout: 'AppLayoutInbox'
    }
  },
  {
    path: '/inboxes/:inboxId/insights/:tab?/:itemId?',
    name: 'Insights',
    component: () => import(/* webpackChunkName: "insights" */ '@/views/Insights.vue'),
    meta: {
      layout: 'AppLayoutInbox'
    }
  },
  {
    path: '/inboxes/:inboxId/settings/:tab?/:itemId?',
    name: 'Settings',
    component: () => import(/* webpackChunkName: "settings" */ '@/views/Settings.vue'),
    meta: {
      layout: 'AppLayoutInbox'
    }
  },
  {
    path: '/inboxes/:inboxId/automation',
    name: 'Automation',
    component: () => import(/* webpackChunkName: "automation" */ '@/views/Automation.vue'),
    meta: {
      layout: 'AppLayoutInbox'
    }
  },

  /* This is the last route in the list, which is a 404 route */
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import(/* webpackChunkName: "NotFound" */ '@/views/404.vue'),
    meta: {
      layout: 'AppLayoutDefault'
    }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.name !== 'Login' && !store.getters.isAuthenticated) {
    next({ name: 'Login' })
  } else if (to.name === 'Login' && store.getters.isAuthenticated) {
    next({ name: 'Dashboard' })
  } else {
    next()
  }
})

export default router
