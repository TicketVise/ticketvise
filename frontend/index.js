import Vue from 'vue'
import 'alpinejs'
import './email/index.js'
import * as Sentry from "@sentry/browser";
import {Vue as VueIntegration} from "@sentry/integrations";
import {Integrations} from '@sentry/tracing';

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

window.Vue = Vue
window.axios = require('axios')
Vue.config.productionTip = false

/**
 * Load every vue single file components.
 */
const files = require.context('./components/', true, /\.vue$/i)
files.keys().map(key =>
    Vue.component(
        key
            .split('/')
            .pop()
            .split('.')[0],
        files(key).default
    )
)

/**
 * Create a vue component if the url path suffice.
 * @param {String} el = the name of the vue component.
 */
let create_vue = (components) => {
    for (let key in components) {
        if (window.location.pathname.match('^' + key.replace(/\*/g, '[^.]*') + '$')) {
            for (let el of components[key]) {
                new Vue({
                    el: '#' + el,
                    template: `
          <${el}></${el}>
          `
                })
            }

            return
        }
    }
}

/**
 * Next let's enable the application containers.
 * As a key you can define on which page the vue component show render.
 * The value is than a list of the vue components for that page.
 * The name of the vue component if the lowercase name with dashes in between.
 */
let components = {
  '/notifications': ['notifications'],
  '/inboxes/*/tickets': ['ticket-overview'],
  '/inboxes/*/tickets/new': ['ticket-form'],
  '/inboxes/*/tickets/*': ['ticket'],
  '/inboxes/*/statistics': ['inbox-statistics'],
  '/profile': ['profile'],
  '/admin': ['admin']
}

/* Now lets set them all up. */
create_vue(components)
