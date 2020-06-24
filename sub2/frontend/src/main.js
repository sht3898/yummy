import Vue from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import infiniteScroll from "vue-infinite-scroll";
import router from "./router";
import store from "./vuex/store";
import Vuex from 'vuex'
import axios from 'axios'
import VueCarousel from 'vue-carousel';
import VueMomentJS from "vue-momentjs"
import moment from "moment"

import GAuth from 'vue-google-oauth2'
Vue.use(VueMomentJS, moment)
export const EventBus = new Vue()
Vue.use(VueCarousel);
Vue.use(Vuex)
const gauthOption = {
  clientId: process.env.VUE_APP_GOOGLE,
  scope: 'profile email',
  prompt: 'select_account'
}

Vue.use(GAuth, gauthOption)

Vue.prototype.$Axios = axios;


Vue.config.productionTip = false;
Vue.use(infiniteScroll);
new Vue({
  vuetify,
  router,
  store,
  render: h => h(App)
}).$mount("#app");
