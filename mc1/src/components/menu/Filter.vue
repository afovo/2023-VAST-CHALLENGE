<template>
  <div
    style="
      color: #393ca2;
      margin-top: 3px;
      font-size: 15px;
      margin-bottom: 1px;
      margin-left: 5px;
      font-family: 'Arial Rounded MT Bold';
    "
  >
    Search Node By ID
  </div>
  <el-input
    style="left: 2%; width: 96%"
    clearable
    v-model="EGO"
    placeholder="Please input node id"
  ></el-input>
  <!--  <Divider style="margin-top: 5px; margin-bottom:5px;></Divider>-->
  <div class="title">Quick Select Suspect</div>
  <el-radio-group v-model="EGO" style="margin-left: 8px">
    <el-radio v-for="suspect in suspects" :label="suspect">
      <div style="font-size: 10px">
        {{ suspect }}
      </div>
    </el-radio>
  </el-radio-group>

  <div class="title">Link Type</div>
  <el-checkbox-group v-model="selectedLinksTypes" style="margin-left: 8px">
    <el-checkbox v-for="linksType in linksTypes" :label="linksType">
      <span :style="{ color: linksTypeColors[linksType] }"> ——— </span>
      <span>{{ linksType == "null" ? "unknown" : linksType }} </span>
    </el-checkbox>
  </el-checkbox-group>

  <div class="title">Node Type</div>
  <el-checkbox-group v-model="selectedNodesTypes" style="margin-left: 8px">
    <el-checkbox v-for="nodeType in nodesTypes" :label="nodeType">
      <span style="margin-right: 0.5rem"
        ><svg width="10" height="10" viewBox="0 0 24 24">
          <path :d="nodesTypeIcons[nodeType]"></path></svg
      ></span>
      <span>{{ nodeType == "null" ? "unknown" : nodeType }}</span>
    </el-checkbox>
  </el-checkbox-group>

  <div class="title">Node Country</div>
  <el-select-v2
    v-model="selectedNodesCountries"
    :options="nodesCountries"
    placeholder="Please select node country"
    style="width: 96%; left: 2%"
    :height="728"
    multiple
    clearable
    filterable
    collapse-tags
  />

  <div class="title">Link Direction</div>
  <span style="font-size: 9px; margin-left: 5px">EGO</span>
  <el-button-group>
    <el-button
      :icon="ArrowLeft"
      size="small"
      :type="linkDirection.in1 ? 'primary' : 'info'"
      @click="linkDirection.in1 = !linkDirection.in1"
      style="height: 20px"
    ></el-button>
    <el-button
      :icon="ArrowRight"
      size="small"
      :type="linkDirection.out1 ? 'primary' : 'info'"
      @click="linkDirection.out1 = !linkDirection.out1"
      style="height: 20px"
    >
    </el-button>
  </el-button-group>
  <span style="font-size: 9px">L1</span>
  <el-button-group>
    <el-button
      :icon="ArrowLeft"
      size="small"
      :type="linkDirection.in2 ? 'primary' : 'info'"
      @click="linkDirection.in2 = !linkDirection.in2"
      style="height: 20px"
    ></el-button>
    <el-button
      :icon="ArrowRight"
      size="small"
      :type="linkDirection.out2 ? 'primary' : 'info'"
      @click="linkDirection.out2 = !linkDirection.out2"
      style="height: 20px"
    >
    </el-button>
  </el-button-group>
  <span style="font-size: 9px">L2</span>
  <Divider
    style="margin-bottom: 10px; margin-top: 5px; border-color: #393ca2"
  />
  <el-button
    style="height: 23px; font-weight: bold"
    type="primary"
    size="small"
    @click="submit(EGO)"
    >Submit</el-button
  >
  <el-button
    style="height: 23px; font-weight: bold"
    type="danger"
    size="small"
    @click="clear"
    >Clear</el-button
  >
  <el-button
    style="height: 23px; font-weight: bold"
    type="warning"
    size="small"
    @click="reset"
    >Reset</el-button
  >
</template>
<style scoped>
.title {
  color: #393ca2;
  margin-top: 4px;
  margin-bottom: 1px;
  margin-left: 5px;
  font-size: 15px;
  font-family: "Arial Rounded MT Bold";
}

.el-checkbox,
.el-radio {
  width: 100%;
  height: 20px;
  padding-left: 5px;
  padding-right: 5px;
  color: rgba(74, 74, 74, 0.899);
}

.el-button--small {
  margin-left: 5px;
  margin-right: 5px;
}

.p-divider.p-divider-horizontal {
  margin: 0;
  margin-top: 1.5px;
  color: rgb(71, 92, 175);
}

.el-vl__window.el-select-dropdown__list {
  height: 500px;
}
</style>
<script setup>
import { ArrowLeft, ArrowRight } from "@element-plus/icons-vue";
import Divider from "primevue/divider";
import { ref, defineEmits, defineExpose } from "vue";
import * as d3 from "d3";
import router from "../../router";
// 调用父组件方法
const emit = defineEmits(["getEgoNetFromFilter"]);

// 选择
const EGO = ref();
const selectedLinksTypes = ref([]);
const selectedNodesTypes = ref([]);
const selectedNodesCountries = ref([]);
const linkDirection = ref({});

// filter 文件内容
const suspects = ref([""]);
const allNodes = ref([""]);
const nodesTypes = ref([""]);
const nodesTypeIcons = ref({});
const nodesCountries = ref([{}]);
const linksTypes = ref([""]);
const linksTypeColors = ref({});

// raw data文件内容（MC1和cycles）
const nodes = ref();
const links = ref();
const cycles = ref();

async function initFilter() {
  await d3.json("data/Filter.json").then((data) => {
    EGO.value = "Oceanfront Oasis Inc Carriers";
    suspects.value = data.suspects;
    allNodes.value = data.nodes;
    nodesTypes.value = data.nodesTypes;
    nodesTypeIcons.value = data.nodesTypeIcons;
    nodesCountries.value = data.nodesCountries.flatMap((e) => {
      return { label: e, value: e };
    });
    linksTypes.value = data.linksTypes;
    linksTypeColors.value = data.linksTypeColors;
    // 默认选择哪些
    selectedLinksTypes.value = linksTypes.value;
    selectedNodesTypes.value = nodesTypes.value;
    selectedNodesCountries.value = data.nodesCountries;
    linkDirection.value = {
      out1: true,
      in1: true,
      out2: true,
      in2: true,
    };
  });
}

async function initFullRawData() {
  await d3.json("data/MC1.json").then((data) => {
    // 初始化所有node，存放到字典 nodes 里
    nodes.value = {};
    data.nodes.forEach((node) => {
      nodes.value[node.id] = {
        id: node.id,
        type: node.type ? node.type : "null",
        country: node.country ? node.country : "unknown",
      };
    });
    // 初始化所有link，存放到数组 links 里
    links.value = [];
    data.links.forEach((link) => {
      links.value.push(link);
    });
  });
  await d3.json("data/cycles.json").then((data) => {
    cycles.value = data;
  });
}

function node(id) {
  return nodes.value[id];
}

function reset() {
  initFilter();
}

function clear() {
  EGO.value = "";
  selectedLinksTypes.value = [];
  selectedNodesTypes.value = [];
  // selectedNodesCountries.value = [];
  linkDirection.value = {
    out1: false,
    in1: false,
    out2: false,
    in2: false,
  };
}

async function submit(id) {
  // console.log(id);
  EGO.value = id;
  await initFullRawData();
  // console.log(nodes.value[id]);
  let net = {};
  links.value = new Set(links.value);
  let set1 = new Set();
  let set2 = new Set();
  let link1 = [];
  let link2 = [];
  // 根据 link type 筛选
  let TYPE = new Set(selectedLinksTypes.value);
  links.value.forEach((link) => {
    let type = link.type;
    if (!TYPE.has(type)) {
      links.value.delete(link);
    }
  });
  // 根据 node type 筛选
  // 根据 node country 筛选
  let NODETYPE = new Set(selectedNodesTypes.value);
  let NODECOUNTRY = new Set(selectedNodesCountries.value);
  links.value.forEach((link) => {
    let ego = node(id);
    let source = node(link.source);
    let target = node(link.target);
    if (source == ego) {
      // 只用筛选 target 的类型
      if (!NODETYPE.has(target.type) || !NODECOUNTRY.has(target.country)) {
        links.value.delete(link);
      }
    } else if (target == ego) {
      // 只用筛选 source 的类型
      if (!NODETYPE.has(source.type) || !NODECOUNTRY.has(source.country)) {
        links.value.delete(link);
      }
    } else {
      // 筛选两边的类型，得两边同时满足条件
      if (!NODETYPE.has(target.type) || !NODECOUNTRY.has(target.country)) {
        links.value.delete(link);
      }
      if (!NODETYPE.has(source.type) || !NODECOUNTRY.has(source.country)) {
        links.value.delete(link);
      }
    }
  });
  // 根据出入方向，筛选一阶
  links.value.forEach((link) => {
    let source = link.source;
    let target = link.target;
    if (linkDirection.value.out1 && linkDirection.value.in1) {
      source === id ? (set1.add(target), link1.push(link)) : {};
      target === id ? (set1.add(source), link1.push(link)) : {};
    } else if (linkDirection.value.out1 && !linkDirection.value.in1) {
      source === id ? (set1.add(target), link1.push(link)) : {};
    } else if (!linkDirection.value.out1 && linkDirection.value.in1) {
      target === id ? (set1.add(source), link1.push(link)) : {};
    } else if (!linkDirection.value.out1 && !linkDirection.value.in1) {
    }
  });
  // 根据出入方向，筛选二阶
  links.value.forEach((link) => {
    let source = link.source;
    let target = link.target;
    if (set1.has(source) && set1.has(target)) {
      // 一阶之间的相互连接，加入到link2
      link2.push(link);
    } else if (source == id || target == id) {
      // 防止加入一阶的
    } else {
      if (linkDirection.value.out2 && linkDirection.value.in2) {
        set1.has(source) ? (set2.add(target), link2.push(link)) : {};
        set1.has(target) ? (set2.add(source), link2.push(link)) : {};
      } else if (linkDirection.value.out2 && !linkDirection.value.in2) {
        set1.has(source) ? (set2.add(target), link2.push(link)) : {};
      } else if (!linkDirection.value.out2 && linkDirection.value.in2) {
        set1.has(target) ? (set2.add(source), link2.push(link)) : {};
      } else if (!linkDirection.value.out2 && !linkDirection.value.in2) {
      }
    }
  });
  net = {
    cycles: cycles,
    direction: `EGO ${
      linkDirection.value.out1 && linkDirection.value.in1
        ? "<-->"
        : linkDirection.value.out1
        ? "--->"
        : linkDirection.value.in1
        ? "<---"
        : "x"
    } One ${
      linkDirection.value.out2 && linkDirection.value.in2
        ? "<-->"
        : linkDirection.value.out2
        ? "--->"
        : linkDirection.value.in2
        ? "<---"
        : "x"
    } Two`,
    ego: node(id),
    nodes1: new Set([...set1].flatMap((e) => node(e))),
    nodes2: new Set([...set2].flatMap((e) => node(e))),
    links1: new Set(link1),
    links2: new Set(link2),
    egoType: node(id).type === "null" ? "unknown" : node(id).type,
  };
  // 打印预览;
  // console.log(net);

  //点按 submit 时候把 net 传给他爷爷app
  emit("getEgoNetFromFilter", net);
}

// 跟随页面加载
setTimeout(async () => {
  await initFilter();
  // await submit(EGO.value);
}, 1);

defineExpose({ submit });
</script>
