import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import { Auth0Plugin } from "./auth";
import HighlightJs from "./directives/highlight";

import { library } from "@fortawesome/fontawesome-svg-core";
import { faLink, faUser, faPowerOff } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { domain, clientId } from "../auth_config.json";
//import Cloudinary,{CldVideo, CldTransformation} from 'cloudinary-vue';
import config from 'config'

const configMixin = Vue.mixin({
  created: function () {
    this.$config = config
  }
})

Vue.config.productionTip = false;

Vue.use(Auth0Plugin, {
  domain,
  clientId,
  onRedirectCallback: appState => {
    router.push(
      appState && appState.targetUrl
        ? appState.targetUrl
        : window.location.pathname
    );
  }
});
/*
Vue.use(Cloudinary, {
  configuration: { 
    cloudName: "classmethod-japan",
    apiKey: '449295245557726', 
    apiSecret: '07qivnPL6bay1I1azj1Uop9mFiY',
    uploadPrefix: 'https://api-ap.cloudinary.com'
  }
});
*/
Vue.directive("highlightjs", HighlightJs);

library.add(faLink, faUser, faPowerOff);
Vue.component("font-awesome-icon", FontAwesomeIcon);

new Vue({
  router,
  configMixin,
  render: h => h(App)
}).$mount("#app");
