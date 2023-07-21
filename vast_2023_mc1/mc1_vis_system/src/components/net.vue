<template>
  <div style="display:flex; flex-direction:row">
    <div v-for="i in show_queue" style="display:flex; flex-direction:row">
      <div style="color: #4d4c4c; font-size:10px; margin-top: 7px">{{ i }}</div>
      <div style="color: #6d83d7; font-size:20px; font-weight: bold; margin-left: 10px; margin-right:10px"> ▻</div>
    </div>
  </div>

  <div style="z-index: 1; position: absolute; right:20%">
  <Fieldset legend="Anomaly list" toggleable :collapsed="false" style="width: 17rem; ">
    <div v-for="(item, i) in [...quickSet].sort((a,b)=>{return anomalyAll[b]-anomalyAll[a]})" style="width: 15rem; font-size: 0.7rem; margin-top: 0.6rem; margin-left: 0.2rem;">
      <div style="display:flex; flex-direction: row; justify-content: space-between">
        <div> {{ item }}</div>

        <div style="display:flex; flex-direction: row">
          <div style="margin-right: 9px">{{ anomalyAll[item] }}</div>
          <el-button type="danger" :icon="Delete" circle size="small" plain style="margin-top:-4px" @click="DeleteAnomaly(item)"/>
        </div>

      </div>
    </div>
  </Fieldset>
  </div>

  <el-dialog
      v-model="dialogVisible"
      title="Anormaly List ➕"
      width="31%"
  >
    <span>Are you sure you want to add {{selectedNode}} to the anomaly list？</span>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="AddAnomaly">
          Confirm
        </el-button>
      </span>
    </template>
  </el-dialog>

  <Dialog
      id="tip"
      v-model:visible="showCard"
      style="width: 31%; position: absolute"
      :header="selectedNode"
      :draggable="true"
  >
    <TabView>
      <TabPanel header="ID">
        <div v-for="i in nodeTypes">
          <div v-if="selectedNodeInfo.type === i">
            <img :src="`node/${i}.svg`" alt="" style="height: 17px; margin-right: 5px"/>
            {{ selectedNode }}
          </div>
        </div>
        <div v-if="selectedNodeInfo.country !== 'null'"
             style="color: #585bd7; font-size: 15px; margin-top:9px; display:flex; flex-direction:row">
          <div> ⚑ country:</div>
          <div style="color: #757577; margin-left:10px">
            {{ selectedNodeInfo.country }}
          </div>
        </div>
        <div v-if="selectedNodeInfo.unity_name !== 'null'"
             style="color: #585bd7; font-size: 15px; margin-top:9px; display:flex; flex-direction:row">
          <div> ✧ unit:</div>
          <div style="color: #757577; margin-left:10px">
            {{ selectedNodeInfo.unity_name }}
          </div>
          <div style="color: #585bd7; margin-left:10px">
            [ {{ selectedNodeInfo.unity_size }} members ]
          </div>
        </div>
        <div v-if="selectedNodeInfo.vessels_in_same_wcc !== 'null'"
             style="color: #393ca2; font-size: 15px; margin-top:10px; ">
          <div> ⛴ &nbsp;Reachable Vessels:</div>

          <div v-for="(item,i) in selectedNodeInfo.vessels_in_same_wcc"
               style="color: #757577; margin-left:25px; font-size: 8px">
            <div v-if="i < 3">
              ・ {{ item }}
            </div>
          </div>
          <div style="color: #585bd7; margin-left:30px; margin-top:5px;">
            [ {{ selectedNodeInfo.vessels_in_same_wcc.length }} in total ]
          </div>
        </div>
        <div v-else style="color: #af2b3a; font-size: 15px; margin-top:10px; ">⚠️ No Reachable Vessel</div>

        <div style="color: #393ca2; font-size: 15px; margin-top:10px; ">
          <div style="margin-bottom:3px"> 🌐 &nbsp;Top 3 Largest Reachable Nodes:</div>
          <div v-for="(item,i) in selectedNodeInfo.sum_degrees_top3"
               style="color: #757577; margin-left:25px; font-size: 8px">
            ・ {{ item[0] }} : {{ item[1] }}
          </div>
        </div>
      </TabPanel>
      <TabPanel header="Statistics">
        <div style="display: flex;flex-direction: row;">

          <div style="display: flex;flex-direction: column;">
            <div style="color: #393ca2;  font-weight: bold">Nodes:</div>
            <div v-for="i in nodeTypes" class="legend-card">
              <img :src="`node/${i}.svg`" alt="" style="height: 10px"/>
              <span class="card-statistics">{{ i }} : {{ selectedNodeInfo[i] }}</span>
            </div>
          </div>

          <div style="display: flex;flex-direction: column; margin-left: 8px">
            <div style="color: #393ca2;  font-weight: bold">Edges:</div>
            <div v-for="i in linkTypes" class="legend-card">
              <span :style="{ color: linkTypeColor[i] }">——— </span>
              <span>{{ i }} : {{ selectedNodeInfo[i] }}</span>
            </div>
            <div style="font-size: 14px; color: #585bd7; margin-top:5px"> ➡️ in :
              <span style="color: #5d5b5b">
              {{ selectedNodeInfo.in_num }}
                </span>
            </div>
            <div style="font-size: 14px; color: #585bd7"> ⬅️ out :
              <span style="color: #5d5b5b">
              {{ selectedNodeInfo.out_num }}
                </span>
            </div>
          </div>

        </div>

        <div style="color: #393ca2; margin-top: 15px; font-weight: bold">Extra:</div>
        <div style="font-size: 14px; color: #585bd7;"> 🏅 Top 3 Nodes with Most Connected Edges：</div>
        <div v-for="i in selectedNodeInfo.top3neighbor" class="legend-card">
          {{ i[0] }} : {{ i[1] }}
        </div>
      </TabPanel>
      <TabPanel header="Cycled Supply Chain">
        <div class="card flex justify-content-center">
          <div class="flex flex-column gap-3">
            <div
                v-for="category of ringLengths"
                :key="category.key"
                class="flex align-items-center"
            >
              <Checkbox
                  v-model="selectedRingLengths"
                  :inputId="category.key"
                  name="category"
                  :value="category.name"
                  :disabled="count[category.name-2]===0"
              />
              <label :for="category.key">{{
                  "  Length " + category.name +': '+count[category.name-2]
                }}</label>
            </div>
          </div>
          <h4 v-if="count[-1]>0"><br>Access Count: {{ count[-1] }}<br>Rank: {{ rank }}</h4>
          <h4 v-else>No Cycles Available</h4>
        </div>
      </TabPanel>
    </TabView
    >
  </Dialog>

  <div id="container">
    <div id="legend_container">
      <Fieldset legend="Node Type" toggleable :collapsed="false">
        <div v-for="i in nodeTypes" class="legend">
          <img :src="`node/${i}.svg`" alt="" style="height: 10px"/>
          <span class="legend">{{ i }}</span>
        </div>
      </Fieldset>
      <Fieldset legend="link Type" toggleable :collapsed="false">
        <div v-for="i in linkTypes" class="legend">
          <span :style="{ color: linkTypeColor[i] }">——— </span>
          <span>{{ i }}</span>
        </div>
      </Fieldset>

    </div>


    <div id="main">
      <svg></svg>
    </div>

  </div>
</template>
<style scoped>
marker-end {
  stroke-width: 1;
  width: 20px;
  height: 10px;
}

:deep(.p-panel-content) {
  padding: 0;
}

:deep(.p-fieldset.p-fieldset-toggleable .p-fieldset-legend a) {
  padding: 0.5rem;
}

:deep(.p-component, .p-component *) {
  margin-top: 1rem;
  margin-left: 1rem;
}

:deep(.p-fieldset-legend-text) {
  min-width: 7rem;
}

:deep(.p-fieldset .p-fieldset-content) {
  padding: 0;
}

:deep(.p-panel-title) {
  font-size: 1.6rem;
}

:deep(.p-panel-header-icon) {
  opacity: 0;
}

.legend {
  min-width: 9rem;
  font-size: 0.7rem;
  margin-top: 0.2rem;
  margin-left: 0.2rem;
}

.legend-card {
  min-width: 11rem;
  font-size: 0.7rem;
  margin-top: 0.3rem;
  margin-left: 0.2rem;
}

.card-statistics {
  margin-left: 0.2rem;
}

.p-dialog-header {
  display: none;
}

#container {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
  z-index: 0;
}

#legend_container {
  display: flex;
  flex-direction: column;
  position: absolute;
  z-index: 1;
}

#main {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
}
</style>
<script setup>
import {defineProps, defineEmits, ref, watch} from "vue";
import TabPanel from "primevue/tabpanel";
import Fieldset from "primevue/fieldset";
import TabView from "primevue/tabview";
import Dialog from "primevue/dialog";
import Checkbox from "primevue/checkbox";
import Panel from "primevue/panel";
import Breadcrumb from 'primevue/breadcrumb';
import Button from 'primevue/button';
import * as d3 from "d3";
import { Delete } from '@element-plus/icons-vue'


class FixedQueue {
  constructor(capacity) {
    this.capacity = capacity;
    this.queue = [];
  }

  enqueue(item) {
    if (this.queue.length >= this.capacity) {
      this.queue.shift();
    }
    this.queue.push(item);
  }

  dequeue() {
    return this.queue.shift();
  }

  size() {
    return this.queue.length;
  }
}

const history_queue = new FixedQueue(7);
const show_queue = ref([])

const props = defineProps({
  net: Object,
  cycles: Object
});
const showCard = ref(false);
const selectedNode = ref("");
const selectedNodeInfo = ref({});

const emit = defineEmits(["change"]);
//环显示
const ringLengths = ref([
  {name: 2, key: "A"},
  {name: 3, key: "B"},
  {name: 4, key: "C"},
  {name: 5, key: "D"},
  {name: 6, key: "E"},
]);
const selectedRingLengths = ref([]);
let ringLinks = []
const count = ref([0,0,0,0,0,0]);//-1: all
const rank = ref(0);


let iconMap = {
  null: "M12,24A12,12,0,1,1,24,12,12.013,12.013,0,0,1,12,24ZM12,2A10,10,0,1,0,22,12,10.011,10.011,0,0,0,12,2Z",
  company:
      "m4 13h3v2h-3zm5 2h3v-2h-3zm-5 4h3v-2h-3zm5 0h3v-2h-3zm-5-12h3v-2h-3zm5 0h3v-2h-3zm-5 4h3v-2h-3zm5 0h3v-2h-3zm15-3v16h-24v-21a3 3 0 0 1 3-3h10a3 3 0 0 1 3 3v2h5a3 3 0 0 1 3 3zm-10-5a1 1 0 0 0 -1-1h-10a1 1 0 0 0 -1 1v19h12zm8 5a1 1 0 0 0 -1-1h-5v15h6zm-4 7h2v-2h-2zm0 4h2v-2h-2zm0-8h2v-2h-2z",
  organization:
      "M24,11.984a4,4,0,0,0-3.957-4A9.05,9.05,0,0,0,16,3.949a4,4,0,0,0-7.99,0A9.05,9.05,0,0,0,3.957,7.988a3.995,3.995,0,0,0-.016,7.989,9.044,9.044,0,0,0,4.064,4.074,4,4,0,0,0,7.99,0,9.044,9.044,0,0,0,4.064-4.074A4,4,0,0,0,24,11.984ZM12,2a2,2,0,1,1-2,2A2,2,0,0,1,12,2ZM2,11.984a2,2,0,1,1,2,2A2,2,0,0,1,2,11.984ZM12,22a2,2,0,1,1,2-2A2,2,0,0,1,12,22Zm3.478-3.939a3.965,3.965,0,0,0-6.956,0,7.062,7.062,0,0,1-2.59-2.6,3.966,3.966,0,0,0,.015-6.957,7.052,7.052,0,0,1,2.575-2.57,3.965,3.965,0,0,0,6.956,0,7.052,7.052,0,0,1,2.575,2.57,3.966,3.966,0,0,0,.015,6.957A7.062,7.062,0,0,1,15.478,18.061ZM20,13.983a2,2,0,1,1,2-2A2,2,0,0,1,20,13.983Z",
  person:
      "M21,24H19V18.957A2.96,2.96,0,0,0,16.043,16H7.957A2.96,2.96,0,0,0,5,18.957V24H3V18.957A4.963,4.963,0,0,1,7.957,14h8.086A4.963,4.963,0,0,1,21,18.957ZM12,12a6,6,0,1,1,6-6A6.006,6.006,0,0,1,12,12ZM12,2a4,4,0,1,0,4,4A4,4,0,0,0,12,2Z",
  location:
      "M12,12A4,4,0,1,0,8,8,4,4,0,0,0,12,12Zm0-6a2,2,0,1,1-2,2A2,2,0,0,1,12,6ZM16,22.03l8,1.948V13.483a3,3,0,0,0-2.133-2.871l-2.1-.7A8.037,8.037,0,0,0,20,8.006a8,8,0,0,0-16,0,8.111,8.111,0,0,0,.1,1.212A2.992,2.992,0,0,0,0,12v9.752l7.983,2.281ZM7.757,3.764a6,6,0,0,1,8.493,8.477L12,16.4,7.757,12.249a6,6,0,0,1,0-8.485ZM2,12a.985.985,0,0,1,.446-.832A1.007,1.007,0,0,1,3.43,11.1l1.434.518a8.036,8.036,0,0,0,1.487,2.056L12,19.2l5.657-5.533a8.032,8.032,0,0,0,1.4-1.882l2.217.741a1,1,0,0,1,.725.961v7.949L16,19.97l-7.98,2L2,20.246Z",
  political_organization:
      "M24,11.983a3.994,3.994,0,0,0-2.607-3.735l-.038-.091a10.07,10.07,0,0,0-5.294-5.419l-.329-.144a3.981,3.981,0,0,0-7.462,0l-.418.188A10.19,10.19,0,0,0,2.617,8.245a3.98,3.98,0,0,0-.03,7.468l.128.3a10.1,10.1,0,0,0,5.162,5.228l.393.176a3.982,3.982,0,0,0,7.46,0l.367-.163a10.193,10.193,0,0,0,5.309-5.534A4,4,0,0,0,24,11.983Zm-8.107,7.131a3.991,3.991,0,0,0-7.787,0A8.093,8.093,0,0,1,4.875,15.88,3.991,3.991,0,0,0,4.9,8.1a8.19,8.19,0,0,1,3.206-3.2,3.991,3.991,0,0,0,7.785,0A8.225,8.225,0,0,1,19.1,8.093a3.991,3.991,0,0,0,.015,7.785A8.207,8.207,0,0,1,15.893,19.114Z",
  vessel:
      "M14.96,6.139A5.033,5.033,0,0,0,11.78,5H8.771L7.453,0H1.029L2.347,5H0V7H11.78a3.029,3.029,0,0,1,1.913.687A13.424,13.424,0,0,1,17.077,12H14.7l-3,2H0v2H12.3l3-2h6.641A9.012,9.012,0,0,1,13,22H0v2H13A11.013,11.013,0,0,0,24,13V12H19.287A15.726,15.726,0,0,0,14.96,6.139ZM3.625,2H5.912L6.7,5H4.415ZM12,11H0V9H12ZM3,20a1,1,0,1,1,1-1A1,1,0,0,1,3,20Zm4,0a1,1,0,1,1,1-1A1,1,0,0,1,7,20Zm4,0a1,1,0,1,1,1-1A1,1,0,0,1,11,20Z",
  movement:
      "M23.351,10.253c-.233-.263-.462-.513-.619-.67L20.487,7.3a1,1,0,0,0-1.426,1.4l2.251,2.29L21.32,11H13V2.745l2.233,2.194a1,1,0,0,0,1.4-1.426l-2.279-2.24c-.163-.163-.413-.391-.674-.623A2.575,2.575,0,0,0,12.028.006.28.28,0,0,0,12,0l-.011,0a2.584,2.584,0,0,0-1.736.647c-.263.233-.513.462-.67.619L7.3,3.513A1,1,0,1,0,8.7,4.939l2.29-2.251L11,2.68V11H2.68l.015-.015L4.939,8.7A1,1,0,1,0,3.513,7.3L1.274,9.577c-.163.163-.392.413-.624.675A2.581,2.581,0,0,0,0,11.989L0,12c0,.01.005.019.006.029A2.573,2.573,0,0,0,.65,13.682c.233.262.461.512.618.67l2.245,2.284a1,1,0,0,0,1.426-1.4L2.744,13H11v8.32l-.015-.014L8.7,19.062a1,1,0,1,0-1.4,1.425l2.278,2.239c.163.163.413.391.675.624a2.587,2.587,0,0,0,3.43,0c.262-.233.511-.46.669-.619l2.284-2.244a1,1,0,1,0-1.4-1.425L13,21.256V13h8.256l-2.2,2.233a1,1,0,1,0,1.426,1.4l2.239-2.279c.163-.163.391-.413.624-.675A2.589,2.589,0,0,0,23.351,10.253Z",
  event:
      "m19,2h-1v-1c0-.552-.448-1-1-1s-1,.448-1,1v1h-8v-1c0-.552-.448-1-1-1s-1,.448-1,1v1h-1C2.243,2,0,4.243,0,7v12c0,2.757,2.243,5,5,5h14c2.757,0,5-2.243,5-5V7c0-2.757-2.243-5-5-5Zm-14,2h14c1.654,0,3,1.346,3,3v1H2v-1c0-1.654,1.346-3,3-3Zm14,18H5c-1.654,0-3-1.346-3-3v-9h20v9c0,1.654-1.346,3-3,3Zm-2.603-6.648c0,.379-.264.698-.566.866l-1.564.87.694,1.893c.134.367.013.778-.299,1.013h0c-.319.24-.759.237-1.075-.007l-1.556-1.203-1.556,1.203c-.316.244-.756.247-1.075.007h0c-.312-.235-.433-.646-.299-1.013l.694-1.893-1.564-.87c-.302-.168-.566-.487-.566-.866,0-.321.279-.676.731-.676h2.247l.596-2.283c.094-.362.419-.614.792-.621.373.007.698.259.792.621l.596,2.283h2.247c.452,0,.731.354.731.676Z",
};
let nodeTypes = [
  "null",
  "company",
  "organization",
  "person",
  "location",
  "political_organization",
  "vessel",
  "movement",
  "event",
];
let linkTypes = [
  "null",
  "ownership",
  "partnership",
  "family_relationship",
  "membership",
];
let linkTypeColor = {
  null: "black",
  ownership: "#fc8d59",
  partnership: "#228522",
  family_relationship: "#2166ac",
  membership: "#542788",
};
let anomalyColor = ["#ff9999","#ff6666","#ff0000"]//score>60,>80,>95
let quickSet = ref( new Set([
  "Mar de la Vida OJSC",
  "979893388",
  "Oceanfront Oasis Inc Carriers",
  "8327",
]));
// let AnomalyList = ref(new Set([
//   "Mar de la Vida OJSC",
//   "979893388",
//   "Oceanfront Oasis Inc Carriers",
//   "8327",
// ]));
let net;
let cycles;

async function render() {
  net = props.net;
  cycles = props.cycles;
  await initRender();
  await updateRender();
}

let dialogVisible= ref(false);
let nodeInfo = ref({});
let anomalyAll = ref([]);
let main, width, height;
let svg, defs, nodes, links, linksMark;
let simulation, tick, updateNode, updateLink;
let singleClick, doubleClick, rightClick, dragStart, drag, dragEnd, dragStartTime;
let hoverOn, hoverOut;

function AddAnomaly() {
  quickSet.value.add(selectedNode.value);
  console.log(quickSet.value);
  dialogVisible.value = false;
}

function DeleteAnomaly(item) {
  console.log(item);
  quickSet.value.delete(item);

}

async function initRender() {
  // get the dom
  main = document.getElementById("main");
  main.parentElement.style.height = main.parentElement.style.width = "100%";
  main.style.height = main.style.width = "100%";
  width = main.clientWidth;
  height = main.clientHeight;
  d3.select("#main svg").remove();
  svg = d3
      .select("#main")
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .append("g");
  ///////////// 读资料卡json /////////////////
  d3.json("card_statistics.json").then(data => {
    console.log('lalalalaltxy')
    // console.log(data);
    nodeInfo.value = data;
    console.log(nodeInfo.value);

  }).catch(error => {
    console.error(error)
  })
  //////////end 读资料卡json /////////////////

  ///////////// 读资料卡json /////////////////
  await d3.json("anomaly_list.json").then(data => {
    console.log('hahahatxy')
    // console.log(data);
    anomalyAll.value = data;
    // console.log(anomalyAll.value);

  }).catch(error => {
    console.error(error)
  })
  //////////end 读资料卡json /////////////////

  ////////////// 初始化 全局zoom效果 //////////////
  // 创建缩放行为
  let zoom = d3.zoom();
  // 设置双击事件的处理函数
  zoom.on("zoom", (e) => {
    d3.select("#main svg g").attr("transform", e.transform);
  });
  d3.select("#main").call(zoom).on("dblclick.zoom", null).on("contextmenu", function ( d) {
    console.log("right click");
    dialogVisible.value = true;
    console.log(d.target.id)

    selectedNode.value = d.target.id;
  })
  ////////////// 初始化 全局zoom效果 end //////////////

  ////////////// 初始化 重复元素  //////////////
  defs = d3.select("#main svg").append("defs");
  Object.keys(iconMap).forEach((nodeType) => {
    let icon = defs
        .append("symbol")
        .attr("id", nodeType)
        .append("svg")
        .attr("viewBox", "0 0 24 24");
    // 添加透明圆底
    icon
        .append("circle")
        .attr("r", 12)
        .attr("transform", "translate(12,12)")
        .attr("fill", "white")
        .style("opacity", 1);
    // 添加icon的 d属性
    icon.append("path").attr("d", iconMap[nodeType]);
  });
  Object.keys(linkTypeColor).forEach((linkType) => {
    defs
        .append("marker")
        .attr("id", `arrow-${linkType}`)
        .attr("viewBox", "0 0 20 10")
        .attr("refX", 40)
        .attr("refY", 5)
        .attr("markerWidth", 10)
        .attr("markerHeight", 5)
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M0,0L0,10L20,5L0,0")
        .attr("fill", `${linkTypeColor[linkType]}`);
  });

  ////////////// 初始化 重复元素 end  //////////////

  ////////////// 初始化 节点交互函数  //////////////
  let click_store = null;
  singleClick = function (event, d) {
    // 清除第一次单击事件
    clearTimeout(click_store);
    // 单击事件的代码
    click_store = setTimeout(function () {
      console.log("single click");

      // 资料卡数据读入
      selectedNode.value = d.id;
      selectedNodeInfo.value = nodeInfo.value[d.id];


      count.value = [0,0,0,0,0,0,0]
      rank.value = 0
      if (cycles[selectedNode.value] !== undefined) {
        for(let i=0;i<=4;i++){
          if(cycles[selectedNode.value][i+2] !== undefined) {
            count.value[i] = cycles[selectedNode.value][i+2]["lcount"]
          }
        }

        count.value[-1] = cycles[selectedNode.value]["count"]
        rank.value = cycles[selectedNode.value]["rank"]
      }

      showCard.value = true;
      setTimeout(() => {
        let tip = document.getElementById("tip");
        if (tip !== null) {
          tip.style.left = event.clientX + "px";
          tip.style.top = event.clientY + "px";
        } else {
          showCard.value = false;
          selectedRingLengths.value = [];
        }
      }, 2);
    }, 300);
  };
  doubleClick = function (event, d) {
    // 清除第二次单击事件
    clearTimeout(click_store);
    // 双击事件代码
    console.log("double click");
    if (history_queue.size() >= history_queue.capacity) {
      history_queue.dequeue();
    }
    history_queue.enqueue(d.id);
    console.log(history_queue.queue);
    show_queue.value = history_queue.queue;
    console.log(show_queue.value);
    emit("change", d.id);
  };
  // rightClick = function (event, d) {
  //   d3.event.preventDefault();
  //   // 清除第二次单击事件
  //   clearTimeout(click_store);
  //   // 双击事件代码
  //   console.log("right click");
  //   dialogVisible = true
  //
  // };
  dragStart = function (event, d) {
    event.sourceEvent.stopPropagation();
    if (!event.active) simulation.alphaTarget(0.01).restart();
    d.fx = d.x;
    d.fy = d.y;
    dragStartTime = new Date();
  };
  drag = function (event, d) {
    d.fx = event.x;
    d.fy = event.y;
  };
  dragEnd = function (event, d) {
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
    new Date() - dragStartTime > 15 * 1000
        ? (console.log("hold more than 15s " + d.id), emit("change", d.id))
        : {};
  };
  hoverOn = function (event, d) {
    d3.select(this).select("text").style("display", "inline");
  };
  hoverOut = function (event, d) {
    d3.select(this).select("text").style("display", "none");
  };
  ////////////// 初始化 节点交互函数 end  //////////////

  ////////////// 初始化 两种连接  //////////////
  links = svg
      .append("g")
      .attr("id", "links")
      .selectAll()
      .data([...net.links1, ...net.links2])
      .enter()
      .append("path")
      .attr("fill", "none")
      .attr("marker-end", (d) => `url(#arrow-${d.type})`)
      .attr("stroke", (d) => linkTypeColor[d.type])
      .attr("stroke-width", (d) => d.weight)
      .attr("stroke-width", 1)
      .style("opacity", (d) => (net.links1.has(d) ? 0.75 : 0.25));
  ////////////// 初始化 两种连接 end //////////////

  ////////////// 初始化 三种节点  //////////////
  nodes = svg
      .append("g")
      .attr("id", "nodes")
      .selectAll()
      .data([net.ego, ...net.nodes1, ...net.nodes2])
      .enter()
      .append("g")
      .on("mouseover", hoverOn)
      .on("mouseout", hoverOut)
      .on("click", singleClick)
      .on("dblclick", doubleClick)
      .call(d3.drag().on("start", dragStart).on("drag", drag).on("end", dragEnd));

  nodes
      .append("use")
      .attr("id", (d) => {
        return d.id;
      })
      .attr("width", 20)
      .attr("height", 20)
      .attr("xlink:href", (d) => {
        return `#${d.type}`;
      })
      .attr("fill", (d) => {
        if (d.id == net.ego.id) return "blue";
        else if (quickSet.value.has(d.id)) return "red";
        else {
          let score = anomalyAll.value[d.id];
          if (score>60){
            if (score>80){
              if (score>95){
                return anomalyColor[2]
              }
              return anomalyColor[1]
            }
            return anomalyColor[0]
          }
          return "black";
        }
      });

  nodes
      .append("text")
      .text((d) => {
        return d.id;
      })
      .attr("dy", -7)
      .attr("fill", "black")
      .attr("text-anchor", "start")
      .style("font-size", 20)
      .style("display", "none");
  ////////////// 初始化 三种节点 end //////////////
}

async function updateRender() {
  ////////////// 初始化 更新函数   //////////////
  updateNode = function () {
    nodes.attr("transform", (d) => {
      let radius = 10;
      return `translate(${d.x - radius},${d.y - radius})`;
    });
  };
  updateLink = function () {
    links.attr("d", (d) => {
      // 计算起点和终点的中点坐标
      var midX = (d.source.x + d.target.x) / 2;
      var midY = (d.source.y + d.target.y) / 2;
      var sum = 0;
      for (var i = 0; i < d.type.length; i++) {
        sum += d.type.charCodeAt(i);
      }
      // 使用模板字符串生成弧形路径，控制点为起点和终点的中点
      var path = `M ${d.source.x} ${d.source.y}
      Q ${midX - sum / 85} ${midY + sum / 95}
      ${d.target.x} ${d.target.y}`;
      return path;
    });
  };
  tick = function () {
    updateLink();
    updateNode();
  };
  ////////////// 初始化 更新函数 end //////////////

  ////////////// 初始化 力导向 模拟  //////////////
  simulation = d3
      .forceSimulation()
      .alphaDecay(0.55)
      .nodes([net.ego, ...net.nodes1, ...net.nodes2])
      .force(
          "link",
          d3
              .forceLink([...net.links1, ...net.links2])
              .id(function (d) {
                return d.id;
              })
              .distance(55)
              .strength(1)
      )
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("charge", d3.forceManyBody().strength(-20))
      .force("collide", d3.forceCollide().radius(30).iterations(50))
      .on("tick", tick);
  ////////////// 初始化 力导向 模拟 end  //////////////
}


watch(selectedRingLengths, (newVal, oldVal) => {
      console.log('RingLengths update')
      if (oldVal.length === 0 || oldVal.every(x => newVal.includes(x))) {//新来的只是有所增加
        newVal.filter(x => !oldVal.includes(x)).forEach((l) => {
          if (cycles[selectedNode.value][l] !== undefined) {
            let array = Array.from(cycles[selectedNode.value][l]["data"]);
            // let flattenedArray = array.flat().map((item) => JSON.parse(JSON.stringify(item)));
            ringLinks = ringLinks.concat(array);
          }
        })
      } else {//有减少，皮肤还原
        for (let i = 0; i < ringLinks.length - 1; i++) {
          let sourceId = ringLinks[i];
          let targetId = ringLinks[i + 1];
          // 选择对应的线元素并修改属性
          svg.select("#links")
              .selectAll("path")
              .filter(function (linkData) {
                return linkData.source.id === sourceId && linkData.target.id === targetId;
              })
              .attr("marker-end", (d) => `url(#arrow-${d.type})`)
              .attr("stroke", (d) => linkTypeColor[d.type])
              .attr("stroke-width", 10)
              .style("opacity", 0);
          updateLink();

          // 选择对应的点元素并修改属性
          svg.select("#nodes")
              .selectAll("use")
              .filter(function (nodeData) {
                return (nodeData.id === sourceId || nodeData.id === targetId) && !quickSet.value.has(nodeData.id);
              })
              .attr("fill", (d) => {
                if (d.id == net.ego.id) return "blue";
                else if (quickSet.value.has(d.id)) return "red";
                else {
                  let score = anomalyAll.value[d.id];
                  if (score>60){
                    if (score>80){
                      if (score>95){
                        return anomalyColor[2]
                      }
                      return anomalyColor[1]
                    }
                    return anomalyColor[0]
                  }
                  return "black";
                }
              });
        }
        ringLinks = []
        selectedRingLengths.value.forEach((l) => {
          if (cycles[selectedNode.value][l] !== undefined) {
            let array = Array.from(cycles[selectedNode.value][l]["data"]);
            ringLinks = ringLinks.concat(array);
          }
        })
      }
      for (let i = 0; i < ringLinks.length - 1; i++) {
        let sourceId = ringLinks[i];
        let targetId = ringLinks[i + 1];
        // 选择对应的线元素并修改属性
        svg.select("#links")
            .selectAll("path")
            .filter(function (linkData) {
              return linkData.source.id === sourceId && linkData.target.id === targetId;
            })
            .attr("marker-end", (d) => `url(#arrow-${d.type})`)
            .attr("stroke", "yellow")
            .attr("stroke-width", 10)
            .style("opacity", 0);
        updateLink();

        // 选择对应的点元素并修改属性
        svg.select("#nodes")
            .selectAll("use")
            .filter(function (nodeData) {
              return (nodeData.id === sourceId || nodeData.id === targetId) && !quickSet.value.has(nodeData.id);
            })
            .attr("fill", "yellow");
      }
    },
    {
      deep: true,
    }
)
defineExpose({render});
</script>
