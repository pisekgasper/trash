import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import VueChartkick from "vue-chartkick";
import "chartkick/chart.js";
import SimpleTypeahead from 'vue3-simple-typeahead'; //Optional default CSS


const app = createApp(App);
// functionality
app.use(router).use(VueChartkick).use(SimpleTypeahead);

// mounting
app.mount("#app");
