<template>
  <div
    style="
      display: flex;
      flex-direction: row;
      justify-content: flex-start;
      align-items: center;
    "
  >
    <Panel header="Filter" id="filter" style="width: 22%">
      <div class="filterContainer">
        <div class="row"><span class="text">Switch Graph</span></div>
        <div class="row" style="height: 2.4rem">
          <ToggleButton
            v-model="GraphSwitch"
            offLabel="Switch to EGO-Net"
            onLabel="Switch to Hierachy-Tree"
            style="margin-left: 1rem; min-width: 90%"
            v-on:change="
              () => {
                if (GraphSwitch) {
                  resize();
                }
              }
            "
          />
        </div>
        <div class="row"><span class="text">Quick Select</span></div>
        <div class="row">
          <Dropdown
            editable
            v-model="ego"
            dropdown
            :options="quick"
            style="width: 95%; margin-left: 0.5rem"
          />
        </div>
        <div class="row"><span class="text">Link Type</span></div>
        <div class="row">
          <MultiSelect
            v-model="selectedLinkTypes"
            :options="
              linkTypes.flatMap((e) => {
                return { label: e, value: e };
              })
            "
            filter
            display="chip"
            placeholder="Select Link Type"
            optionLabel="label"
            optionValue="value"
            scrollHeight="450px"
            style="width: 95%; margin-left: 0.5rem"
            ><template #option="slotProps">
              <div class="flex align-items-center">
                <span :style="{ color: linkTypeColor[slotProps.option.label] }"
                  >———
                </span>
                <span style="font-size: 1rem; margin-left: 0.5rem">{{
                  slotProps.option.label
                }}</span>
              </div>
            </template></MultiSelect
          >
        </div>
        <div class="row"><span class="text">Node Type</span></div>
        <div class="row">
          <MultiSelect
            v-model="selectedNodeTypes"
            :options="
              nodeTypes.flatMap((e) => {
                return { label: e, value: e };
              })
            "
            filter
            display="chip"
            placeholder="Select Node Type"
            optionLabel="label"
            optionValue="value"
            scrollHeight="450px"
            style="width: 95%; margin-left: 0.5rem"
            ><template #option="slotProps">
              <div class="flex align-items-center">
                <img
                  :src="`node/${slotProps.option.label}.svg`"
                  style="width: 1rem; height: 1rem"
                />
                <span style="font-size: 1rem; margin-left: 0.5rem">{{
                  slotProps.option.label
                }}</span>
              </div>
            </template></MultiSelect
          >
        </div>
        <div class="row"><span class="text">Node Country</span></div>
        <div class="row">
          <MultiSelect
            v-model="selectedCountries"
            :options="
              countries.flatMap((e) => {
                return { label: e, value: e };
              })
            "
            filter
            display="chip"
            placeholder="Select Countries"
            optionLabel="label"
            optionValue="value"
            scrollHeight="440px"
            style="width: 95%; margin-left: 0.5rem"
          >
            <template #footer>
              <div class="py-2 px-3">
                <b>{{ selectedCountries ? selectedCountries.length : 0 }}</b>
                countr{{
                  (selectedCountries ? selectedCountries.length : 0) > 1
                    ? "ies"
                    : "y"
                }}
                selected.
              </div>
            </template>
          </MultiSelect>
        </div>
        <div class="row"><span class="text">Link Direction</span></div>
        <div class="row" style="height: 2.4rem">
          <ToggleButton
            v-model="in1"
            onLabel=""
            offLabel=""
            onIcon="pi pi-arrow-left"
            offIcon="pi pi-times"
            style="margin-left: 1rem"
          />
          <ToggleButton
            v-model="out1"
            onLabel=""
            offLabel=""
            onIcon="pi pi-arrow-right"
            offIcon="pi pi-times"
            style="margin-right: 0.5rem"
          />

          <ToggleButton
            v-model="in2"
            onLabel=""
            offLabel=""
            onIcon="pi pi-arrow-left"
            offIcon="pi pi-times"
            style="margin-left: 0.5rem"
          />
          <ToggleButton
            v-model="out2"
            onLabel=""
            offLabel=""
            onIcon="pi pi-arrow-right"
            offIcon="pi pi-times"
            style="margin-right: 1rem"
          />
        </div>
        <div class="row"><span class="text">Submit</span></div>
        <div class="row" style="height: 2.4rem">
          <Button
            label="Submit"
            icon="pi pi-check"
            severity="info"
            @click="submit"
            style="margin-left: 1rem; margin-right: 0.5rem; min-width: 42%"
          />
          <Button
            label="Reset"
            icon="pi pi-times"
            severity="danger"
            @click="reload"
            style="margin-left: 0.5rem; margin-right: 1rem; min-width: 42%"
          />
        </div>
      </div>
    </Panel>
    <Panel
      header="Graph"
      :id="GraphSwitch ? 'EGONET' : 'HierachyTree'"
      style="width: 78%"
    >
      <Net :net="net" :cycles="cycles" ref="netComponent" @change="change" v-if="GraphSwitch" />
      <HierachyTree v-if="!GraphSwitch"></HierachyTree>
    </Panel>
  </div>
  <ParallelCoordinates ref="parallelCoordinates" :anomalies="quick" :nodeID="ego" :nodeType="'organization'"></ParallelCoordinates>
</template>

<style scoped>
:root {
  font-family: Inter, system-ui;
}
span {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
  font-size: 1.3rem;
  min-width: 8%;
  margin-left: 2%;
}
.direction {
  margin: 0;
  width: auto;
  min-width: 1rem;
  margin-right: 1rem;
}
:deep(.p-multiselect-panel) {
  width: 20%;
}
.filterContainer {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
}
.row {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin-top: 0.3rem;
}
.p-dropdown {
  width: 81%;
}
.p-multiselect {
  width: 87%;
}
.p-multiselect-items-wrapper {
  max-height: 400px;
}
.p-togglebutton {
  min-width: 20%;
}
#first {
  width: 87%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.text {
  font-weight: 600;
  font-size: 1.4rem;
  margin-left: 1rem;
  margin-top: 0.5rem;
}
.p-sidebar-top,
.p-sidebar {
  height: auto;
}
:deep(.p-panel-title) {
  font-size: 1.6rem;
}
:deep(.p-panel-header-icon) {
  /* display: none; */
  opacity: 0;
}
:deep(.p-component, .p-component) {
  height: 100%;
}
</style>

<script setup>
import ToggleButton from "primevue/togglebutton";
import MultiSelect from "primevue/multiselect";
import Dropdown from "primevue/dropdown";
import Button from "primevue/button";
import Panel from "primevue/panel";
import HierachyTree from "./charts/HierachyTree.vue";
import ParallelAxis from "./charts/ParallelAxis.vue";
import Net from "/src/components/net.vue";
import { ref } from "vue";
import * as d3 from "d3";
import ParallelCoordinates from "./ParallelCoordinates.vue";
/////////////// filter start ///////////////
let GraphSwitch = ref(true);
let quick = ref([
  "Mar de la Vida OJSC",
  "979893388",
  "Oceanfront Oasis Inc Carriers",
  "8327",
]);
let ego = ref("Oceanfront Oasis Inc Carriers");
let out1 = ref(true);
let in1 = ref(true);
let out2 = ref(true);
let in2 = ref(true);
let linkTypeColor = {
  null: "black",
  ownership: "#fc8d59",
  partnership: "#228522",
  family_relationship: "#2166ac",
  membership: "#542788",
};
let countries = [
  "null",
  "Nalakond",
  "Rio Isla",
  "Country_271835",
  "Country_789455",
  "Osterivaria",
  "Country_712875",
  "Oceanus",
  "Country_19028",
  "Vesperanda",
  "Riodelsol",
  "Vesperand's Bay",
  "Country_951683",
  "Syrithania",
  "Country_628643",
  "Merigrad",
  "Country_338740",
  "Vesperlandia",
  "Country_245265",
  "Marebak",
  "Country_552976",
  "Quandoria",
  "Uzimoria",
  "Country_874023",
  "Country_895471",
  "Country_766259",
  "Country_34878",
  "Polarisdom",
  "Country_459036",
  "Country_415128",
  "Country_437825",
  "Country_198078",
  "Country_931736",
  "Country_984533",
  "Oceanterra",
  "Country_483478",
  "Country_981995",
  "Country_461742",
  "Country_542476",
  "Country_887466",
  "Country_789037",
  "Ivarisia",
  "Country_449947",
  "Country_204272",
  "Country_800653",
  "Wysterion",
  "Country_907876",
  "Country_709784",
  "Arreciviento",
  "Luminsia",
  "Country_990614",
  "Country_283574",
  "Ariuzima",
  "Country_663412",
  "Country_948318",
  "Country_242593",
  "Islavaria",
  "Country_443882",
  "Uzifrica",
  "Brindivaria",
  "Country_338923",
  "Country_729731",
  "Helvoris",
  "Kethanor",
  "Country_980042",
  "Mawazam",
  "Country_216139",
  "Country_913963",
  "Country_230197",
  "Country_675160",
  "Uzilandor",
  "Country_462996",
  "Country_699698",
  "Country_322527",
  "Country_256617",
  "Rio Solovia",
  "Orvietea",
  "Quandarix",
  "Country_996415",
  "Country_57382",
  "Puerto del Mar",
  "Country_358951",
  "Country_146155",
  "Country_342065",
  "Country_144251",
  "Helixia",
  "Country_167470",
  "Country_323509",
  "Country_12955",
  "Country_697428",
  "Country_925382",
  "Country_247330",
  "Country_614826",
  "Country_940095",
  "Country_945731",
  "Country_760479",
  "Country_753331",
  "Country_54147",
  "Country_492608",
  "Country_214033",
  "Country_233547",
  "Zambalantis",
  "Country_11605",
  "Country_226679",
  "Country_821432",
  "Country_246944",
  "Country_746165",
  "Country_950691",
  "Country_982684",
  "Country_670336",
  "Country_244549",
  "Country_470077",
  "Country_532332",
  "Country_984172",
  "Country_193919",
  "Country_928409",
  "Country_615819",
  "Country_286580",
];
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
let selectedCountries = ref(countries);
let selectedNodeTypes = ref(nodeTypes);
let selectedLinkTypes = ref(linkTypes);
/////////////// filter end ///////////////

let nodes = ref({});
let links = ref([]);
let net = ref({});
let cycles = ref({});

const netComponent = ref(null);
const parallelCoordinates = ref(null);

function node(id) {
  return nodes.value[id];
}

async function initFullData() {
  await d3.json("MC1.json").then((data) => {
    // 初始化所有node，存放到字典 nodes 里
    nodes.value = {};
    data.nodes.forEach((node) => {
      nodes.value[node.id] = {
        id: node.id,
        type: node.type ? node.type : "null",
        country: node.country ? node.country : "null",
      };
    });
    // 初始化所有link，存放到数组 links 里
    links.value = [];
    data.links.forEach((link) => {
      links.value.push(link);
    });
  });
  await d3.json("cycles.json").then((data) => {
    cycles.value = data
  })
}

async function initEgoNet() {
  links.value = new Set(links.value);
  let id = ego.value;
  let set1 = new Set();
  let set2 = new Set();
  let link1 = [];
  let link2 = [];
  // 根据 link type 筛选
  let TYPE = new Set(selectedLinkTypes.value);
  links.value.forEach((link) => {
    let type = link.type;
    if (!TYPE.has(type)) {
      links.value.delete(link);
    }
  });
  // 根据 node type 筛选
  // 根据 node country 筛选
  let NODETYPE = new Set(selectedNodeTypes.value);
  let NODECOUNTRY = new Set(selectedCountries.value);
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
    if (out1.value && in1.value) {
      source === id ? (set1.add(target), link1.push(link)) : {};
      target === id ? (set1.add(source), link1.push(link)) : {};
    } else if (out1.value && !in1.value) {
      source === id ? (set1.add(target), link1.push(link)) : {};
    } else if (!out1.value && in1.value) {
      target === id ? (set1.add(source), link1.push(link)) : {};
    } else if (!out1.value && !in1.value) {
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
      if (out2.value && in2.value) {
        set1.has(source) ? (set2.add(target), link2.push(link)) : {};
        set1.has(target) ? (set2.add(source), link2.push(link)) : {};
      } else if (out2.value && !in2.value) {
        set1.has(source) ? (set2.add(target), link2.push(link)) : {};
      } else if (!out2.value && in2.value) {
        set1.has(target) ? (set2.add(source), link2.push(link)) : {};
      } else if (!out2.value && !in2.value) {
      }
    }
  });
  // 打印预览;
  console.log(
    `EGO ${
      out1.value && in1.value
        ? "<-->"
        : out1.value
        ? "--->"
        : in1.value
        ? "<---"
        : "x"
    } One ${
      out2.value && in2.value
        ? "<-->"
        : out2.value
        ? "--->"
        : in2.value
        ? "<---"
        : "x"
    } Two`
  );
  // 图格式返回
  net.value = {
    ego: node(id),
    nodes1: new Set([...set1].flatMap((e) => node(e))),
    nodes2: new Set([...set2].flatMap((e) => node(e))),
    links1: new Set(link1),
    links2: new Set(link2),
  };
}

function reload() {
  location.reload();
}

async function resize() {
  let app = document.getElementById("app");
  app.style.height = `${window.innerHeight - 20}px`;
  let panelHead = document.getElementsByClassName("p-panel-header")[0];
  let panelContent = document.getElementsByClassName("p-panel-content");
  for (let i = 0; i < panelContent.length; i++) {
    panelContent[i].style.padding = 0;
    panelContent[i].style.height =
      window.innerHeight - panelHead.clientHeight - 20 + "px";
  }
  submit();
}
async function submit() {
  await initFullData();
  await initEgoNet();
  // 传递 net 给子组件，并调用net的render方法绘图
  GraphSwitch.value ? await netComponent.value.render() : {};
  await parallelCoordinates.value.updateAxis();

}

function change(id) {
  ego.value = id;
  resize();
}
setTimeout(async () => {
  resize();
}, 1);
</script>
