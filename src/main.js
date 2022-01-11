import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import VueChartkick from "vue-chartkick";
import "chartkick/chart.js";

const app = createApp(App);
// functionality
app.use(router).use(VueChartkick);

// mounting
app.mount("#app");
