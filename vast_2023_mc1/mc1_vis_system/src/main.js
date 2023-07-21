import { createApp } from "vue";
import "./style.css";
import "primeicons/primeicons.css";
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from "./App.vue";
import PrimeVue from "primevue/config";
//theme
import "primevue/resources/themes/lara-light-indigo/theme.css";

//core
import "primevue/resources/primevue.min.css";

createApp(App).use(PrimeVue).use(ElementPlus).mount("#app");
