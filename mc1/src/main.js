import { createApp } from "vue";
import ElementPlus from "element-plus";
import PrimeVue from "primevue/config";
import router from "./router";
import App from "./App.vue";
import "element-plus/dist/index.css";

import "./style.css";
//theme
import "primevue/resources/themes/lara-light-indigo/theme.css";
//core
import "primevue/resources/primevue.min.css";

const app = createApp(App);
app.use(router).use(ElementPlus).use(PrimeVue).mount("#app");
