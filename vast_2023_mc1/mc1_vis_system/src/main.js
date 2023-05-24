import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import ECharts from 'vue-echarts'
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import 'echarts';

const app = createApp(App);
app.use(ElementPlus)
app.component('ECharts', ECharts)
app.mount("#app");
