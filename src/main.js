import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import VueChartkick from "vue-chartkick";
import "chartkick/chart.js";
import SimpleTypeahead from 'vue3-simple-typeahead';
import 'vue3-simple-typeahead/dist/vue3-simple-typeahead.css'; //Optional default CSS


const app = createApp(App);
// functionality
app.use(router).use(VueChartkick).use(SimpleTypeahead);

VueChartkick.options = {
    colors: ['#444444']
}

// mounting
app.mount("#app");
