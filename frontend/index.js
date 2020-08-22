import $ from 'jquery';
import 'jquery-ui';
import 'jquery-ui/ui/widgets/sortable';
import 'jquery-ui/ui/disable-selection';

window.jQuery = $;
window.$ = $;

/**
 * Import Axios for making api calls.
 */
window.axios = require('axios')

/**
 * Import vue into our appliction.
 */
import Vue from 'vue'
window.Vue = Vue
Vue.config.productionTip = false

import 'alpinejs'

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
  '/inboxes/*/tickets': ['ticket-overview'],
  '/inboxes/*/tickets/new': ['ticket-form'],
  '/inboxes/*/tickets/*': ['ticket'],
  '/profile': ['profile']
}

/* Now lets set them all up. */
create_vue(components)
