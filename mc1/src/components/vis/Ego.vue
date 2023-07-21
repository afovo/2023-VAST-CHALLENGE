<template>
  <div style="display: flex">
    <div id="ego"><svg></svg></div>
    <div id="box1">
      <el-scrollbar>
        <div id="history">
          <div v-for="(e, i) in history" class="history_item">
            <span
              style="
                border: solid;
                border-width: 2px;
                border-color: #7275ec;
                background-color: white;
                border-radius: 5px;
              "
            >
              <div style="margin-left: 6px; margin-right: 6px">{{ e }}</div>
            </span>
            <span
              v-if="i != history.length - 1"
              style="margin-left: 10px; color: #7275ec; font-size: 1.5rem"
              >➤</span
            >
          </div>
        </div>
      </el-scrollbar>
    </div>
    <div id="box2">
      <Fieldset
        legend="Anomaly list"
        toggleable
        :collapsed="foldList"
        id="list"
      >
        <el-switch
          v-model="showAnomalyInNet"
          size="large"
          active-text="Show in Net"
          inactive-text="Hide in Net"
          style="margin-left: 20px"
        />
        <el-scrollbar max-height="780px">
          <DataTable :value="anomalyList" style="font-size: 0.8rem">
            <Column field="id" header="Name" style="max-width: 8rem"></Column>
            <Column field="weight" header="Weight">
              <template #body="slotProps">
                <span
                  :style="{
                    color: mapValueToColor(slotProps.data.weight),
                  }"
                >
                  {{ slotProps.data.weight }}
                </span>
              </template>
            </Column>
            <Column field="id" header="Delete">
              <template #body="slotProps">
                <el-button
                  type="danger"
                  :icon="Delete"
                  circle
                  size="small"
                  plain
                  style="margin-left: 5px"
                  @click="deleteAnomaly(slotProps.data.id)"
                />
              </template>
            </Column>
          </DataTable>
        </el-scrollbar>
      </Fieldset>

      <el-dialog v-model="dialogVisible" title="Anormaly List ➕" width="31%">
        <span
          >Are you sure you want to add {{ selectedNode }} to the anomaly
          list？</span
        >
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="dialogVisible = false">Cancel</el-button>
            <el-button type="primary" @click="AddAnomaly"> Confirm </el-button>
          </span>
        </template>
      </el-dialog>
    </div>

    <div id="card" style="position: relative">
      <TabView style="margin-top: 10px">
        <TabPanel>
          <template #header>
            <div style="font-size: 15px; height: 10px">ID</div>
          </template>
          <div v-for="i in nodesTypes">
            <div v-if="selectedNodeInfo.type === i">
              <svg width="19" height="19" viewBox="0 0 24 24">
                <path :d="nodesTypeIcons[i]"></path>
              </svg>
              <span style="margin-left: 15px"> {{ selectedNode }}</span>
            </div>
          </div>
          <div
            v-if="selectedNodeInfo.country !== 'null'"
            style="color: #585bd7; font-size: 15px; margin-top: 9px"
          >
            <div>⚑ Country:</div>
            <div style="color: #757577; margin-left: 30px">
              {{ selectedNodeInfo.country }}
            </div>
          </div>
          <div
            v-if="selectedNodeInfo.unity_name !== 'null'"
            style="color: #585bd7; font-size: 15px; margin-top: 9px"
          >
            <div>✧ Unit:</div>
            <div style="color: #555557; margin-left: 30px">
              {{ selectedNodeInfo.unity_name }}
            </div>
            <div style="color: #585bd7; margin-left: 30px">
              [ {{ selectedNodeInfo.unity_size }} members ]
            </div>
          </div>
          <div
            v-if="selectedNodeInfo.vessels_in_same_scc !== 'null'"
            style="color: #393ca2; font-size: 15px; margin-top: 10px"
          >
            <div>⛴ &nbsp;Bidirectional Reachable Vessels:</div>
            <div
              v-for="(item, i) in selectedNodeInfo.vessels_in_same_scc"
              style="
                color: #686869;
                margin-left: 25px;
                font-size: 14px;
                margin-top: 5px;
              "
            >
              <div v-if="i < 3">・ {{ item }}</div>
            </div>
            <div
              v-if="
                selectedNodeInfo.vessels_in_same_scc !== 'null' &&
                selectedNodeInfo.vessels_in_same_scc !== undefined
              "
              style="color: #585bd7; margin-left: 30px; margin-top: 5px"
            >
              [ {{ selectedNodeInfo.vessels_in_same_scc.length }} in total ]
            </div>
          </div>

          <div
            v-else-if="selectedNodeInfo.vessels_in_same_wcc !== 'null'"
            style="color: #393ca2; font-size: 15px; margin-top: 10px"
          >
            <div>⛴ &nbsp;Reachable Vessels:</div>
            <div
              v-for="(item, i) in selectedNodeInfo.vessels_in_same_wcc"
              style="
                color: #686869;
                margin-left: 25px;
                font-size: 14px;
                margin-top: 5px;
              "
            >
              <div v-if="i < 3">・ {{ item }}</div>
            </div>
            <div
              v-if="
                selectedNodeInfo.vessels_in_same_wcc !== 'null' &&
                selectedNodeInfo.vessels_in_same_wcc !== undefined
              "
              style="color: #585bd7; margin-left: 30px; margin-top: 5px"
            >
              [ {{ selectedNodeInfo.vessels_in_same_wcc.length }} in total ]
            </div>
          </div>

          <div v-else style="color: #af2b3a; font-size: 15px; margin-top: 10px">
            ⚠️ No Reachable Vessel
          </div>

          <div
            v-if="selectedNodeInfo.scc_sum_degrees_top3 !== 'null'"
            style="color: #393ca2; font-size: 15px; margin-top: 10px"
          >
            <div style="margin-bottom: 3px">
              🌐 &nbsp;Top 3 Largest Reachable Nodes:
            </div>
            <div
              v-for="(item, i) in selectedNodeInfo.scc_sum_degrees_top3"
              style="
                color: #686869;
                margin-left: 25px;
                font-size: 14px;
                margin-top: 5px;
              "
            >
              ・ {{ item[0] }} : {{ item[1] }}
            </div>
          </div>
          <div v-else>
            <div style="margin-bottom: 3px; margin-top: 10px">
              🌐 &nbsp;Top 3 Largest Reachable Nodes:
            </div>
            <div
              v-for="(item, i) in selectedNodeInfo.sum_degrees_top3"
              style="
                color: #686869;
                margin-left: 25px;
                font-size: 14px;
                margin-top: 5px;
              "
            >
              ・ {{ item[0] }} : {{ item[1] }}
            </div>
          </div>

          <div style="color: #393ca2; font-size: 15px; margin-top: 10px">
            <div style="margin-bottom: 3px">📍&nbsp;Distance:</div>
            <div
              v-if="selectedNodeInfo.distance_3388 !== 'null'"
              style="
                color: #585bd7;
                margin-left: 25px;
                font-size: 14px;
                margin-top: 5px;
              "
            >
              ⁃ Distance to 979893388 :
              <span style="color: #5e5e5e">{{
                Number.parseFloat(selectedNodeInfo.distance_3388).toFixed(2)
              }}</span>
            </div>
            <div
              v-if="selectedNodeInfo.ocean !== 'null'"
              style="
                color: #585bd7;
                margin-left: 25px;
                font-size: 14px;
                margin-top: 5px;
              "
            >
              ⁃ Distance to Oceanfront Oasis Inc Carriers :
              <span style="color: #5e5e5e">{{
                Number.parseFloat(selectedNodeInfo.distance_ocean).toFixed(2)
              }}</span>
            </div>
          </div>
        </TabPanel>
        <TabPanel>
          <template #header>
            <div style="font-size: 15px; height: 10px">Statistics</div>
          </template>
          <div style="display: flex; flex-direction: column">
            <div style="color: #393ca2; font-weight: bold">Neighbours:</div>
            <div v-for="i in nodesTypes" class="legend-card">
              <svg
                width="10"
                height="10"
                viewBox="0 0 24 24"
                style="margin-right: 8px; margin-left: 20px"
              >
                <path :d="nodesTypeIcons[i]"></path>
              </svg>
              <span class="card-statistics"
                >{{ i == "null" ? "unknown" : i }} :
                {{ selectedNodeInfo[i] }}</span
              >
            </div>
          </div>

          <div style="display: flex; flex-direction: column; margin-top: 10px">
            <div style="color: #393ca2; font-weight: bold">Edges:</div>
            <div
              v-for="i in linksTypes"
              class="legend-card"
              style="margin-left: 5px"
            >
              <span :style="{ color: linksTypeColors[i] }">——— </span>
              <span
                >{{ i == "null" ? "unknown" : i }} :
                {{ selectedNodeInfo[i] }}</span
              >
            </div>
            <div
              style="
                font-size: 14px;
                color: #585bd7;
                margin-top: 5px;
                margin-left: 20px;
              "
            >
              ➡️&nbsp; In Degree:
              <span style="color: #5d5b5b">
                {{ selectedNodeInfo.in_num }}
              </span>
            </div>
            <div style="font-size: 14px; color: #585bd7; margin-left: 20px">
              ⬅️&nbsp; Out Degree:
              <span style="color: #5d5b5b">
                {{ selectedNodeInfo.out_num }}
              </span>
            </div>
          </div>

          <div style="color: #393ca2; margin-top: 15px; font-weight: bold">
            Extra:
          </div>
          <div style="font-size: 14px; color: #585bd7">
            🏅 Top 3 Nodes with Most Connected Edges：
          </div>
          <div
            v-for="i in selectedNodeInfo.top3neighbor"
            class="legend-card"
            style="margin-left: 15px"
          >
            ・ {{ i[0] }} : {{ i[1] }}
          </div>
        </TabPanel>
        <TabPanel>
          <template #header>
            <div style="font-size: 10px; height: 20px; margin-top: -10px">
              Cycled Supply Chain
            </div>
          </template>
          <div class="card flex justify-content-center">
            <div class="flex flex-column gap-3">
              <div
                v-for="category of ringLengths"
                :key="category.key"
                class="flex align-items-center"
                style="margin-bottom: 18px; margin-left: 15px"
              >
                <Checkbox
                  v-model="selectedRingLengths"
                  :inputId="category.key"
                  name="category"
                  :value="category.name"
                  :disabled="count[category.name - 2] === 0"
                />
                <label
                  :for="category.key"
                  style="margin-left: 10px; color: #585bd7"
                  >{{ "  Length " + category.name + " : " }}
                  <span style="color: #5d5b5b">{{
                    count[category.name - 2]
                  }}</span>
                </label>
              </div>
            </div>
            <h4
              v-if="count[-1] > 0"
              style="margin-left: 8px; margin-top: -10px"
            >
              <br />Access Count : {{ count[-1] }}<br /><br />Rank : {{ rank }}
            </h4>
            <h4 v-else style="margin-left: 8px; margin-top: 35px">
              No Cycles Available
            </h4>
          </div>
        </TabPanel>
      </TabView>
      <div
        id="logo-container"
        style="position: absolute; bottom: 5px; right: 5px"
      >
        <img
          src="/fisheye.png"
          alt=""
          style="width: 120px; height: auto; opacity: 0.3"
        />
      </div>
    </div>
  </div>
</template>
<style scoped>
.history_item {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 2.5rem;
  margin-left: 5px;
  margin-right: 5px;
  text-align: center;
  border-radius: 4px;
}
:deep(.el-card__body) {
  padding: 10px;
}
#ego {
  width: 1050px;
  height: 900px;
}

#card {
  width: 300px;
  height: 900px;
  background-color: #ffffff;
}

#box {
  position: fixed;
  top: 2rem;
  z-index: 3;
}

.legend-card {
  min-width: 11rem;
  font-size: 0.9rem;
  margin-top: 0.3rem;
  margin-left: 0.2rem;
}
#history {
  display: flex;
  flex-direction: row;
  max-width: 1020px;
  display: flex;
}
#box1 {
  position: absolute;
  top: 890px;
}
#box2 {
  position: absolute;
  top: 35px;
}
#list {
  top: 5rem;
  z-index: 3;
  display: flex;
  flex-direction: row;
}
</style>
<script setup>
import Fieldset from "primevue/fieldset";
import TabView from "primevue/tabview";
import TabPanel from "primevue/tabpanel";
import Checkbox from "primevue/checkbox";
import { ref, defineEmits, defineProps, watch } from "vue";
import Button from "primevue/button";
import * as d3 from "d3";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import { Delete } from "@element-plus/icons-vue";
import ColumnGroup from "primevue/columngroup"; // optional
import Row from "primevue/row"; // optional
import { ElMessage } from "element-plus";

const showAnomalyInNet = ref(false);
const ringLengths = ref([
  { name: 2, key: "A" },
  { name: 3, key: "B" },
  { name: 4, key: "C" },
  { name: 5, key: "D" },
  { name: 6, key: "E" },
]);
const selectedRingLengths = ref([]);
let ringLinks = [];
const count = ref([0, 0, 0, 0, 0, 0]); //-1: all
const rank = ref(0);
let cycles;

//资料卡变量
let selectedNode = ref("");
const selectedNodeInfo = ref({});
let nodeInfo = ref({});

const emit = defineEmits(["submit"]);
// 容器
let ego, width, height, svg, main, defs, nodeSize;
width = 1050;
height = 900;
nodeSize = 20;
// filter 文件内容
let suspects, nodesTypeIcons, linksTypeColors, nodesTypes, linksTypes;
// 数据
let netData;
// 图的选择集
let nodes, links;
// 交互函数
let dragStart,
  dragIng,
  dragEnd,
  hoverIn,
  hoverOut,
  singleClick,
  doubleClick,
  rightClick;
// simulation函数
let updateNode, updateLink, tick, simulation;
// 右键加入怀疑名单
let anomalyList, anomalyAll, foldList, deleteAnomaly, history;
anomalyList = ref();
history = ref([]);
foldList = ref(true);

function mapValueToColor(value) {
  // 确保输入值在范围内（60到100）
  const clampedValue = Math.min(100, Math.max(60, value));

  // 计算红色通道值
  let red;
  red = value > 60 ? Math.floor((255 * (clampedValue - 60)) / 40) : 128;

  // 灰色通道值保持不变，都为128
  const gray = 50;

  // 返回RGB颜色
  return `rgb(${red}, ${gray}, ${gray})`;
}

//弹窗显示
let dialogVisible = ref(false);

async function initContainer() {
  ///////////// 读资料卡json /////////////////
  await d3
    .json("data/card_statistics.json")
    .then((data) => {
      // console.log(data);
      nodeInfo.value = data;
      // console.log(nodeInfo.value);
    })
    .catch((error) => {
      console.error(error);
    });
  //////////end 读资料卡json /////////////////

  // 设置宽高以及zoom
  let ego = d3.select("#ego");
  ego.select("svg").remove();
  let svg = d3
    .select("#ego")
    .append("svg")
    .attr("width", width)
    .attr("height", height);
  main = svg.append("g").attr("id", "main");
  ego.call(
    d3.zoom().on("zoom", (e) => {
      d3.select("#ego svg g").attr("transform", e.transform);
    })
  );
  // 禁止原生鼠标右键事件;
  document.oncontextmenu = function () {
    return false;
    return true;
  };
  ego.on("dblclick.zoom", null);
  // 读取 filter josn 拿到图例
  await d3.json("data/Filter.json").then((data) => {
    suspects = new Set(data.suspects);
    nodesTypeIcons = data.nodesTypeIcons;
    linksTypeColors = data.linksTypeColors;
    nodesTypes = data.nodesTypes;
    linksTypes = data.linksTypes;
  });
  // 添加箭头
  defs = svg.append("defs");
  Object.keys(linksTypeColors).forEach((linkType) => {
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
      .attr("fill", `${linksTypeColors[linkType]}`);
  });
  // 添加 node icon
  Object.keys(nodesTypeIcons).forEach((nodeType) => {
    defs
      .append("symbol")
      .attr("id", nodeType)
      .append("svg")
      .attr("viewBox", "0 0 24 24")
      .append("path")
      .attr("d", nodesTypeIcons[nodeType]);
  });
}

async function initFunctions() {
  // 交互函数
  dragStart = function (event, d) {
    event.sourceEvent.stopPropagation();
    if (!event.active) simulation.alphaTarget(0.01).restart();
    d.fx = d.x;
    d.fy = d.y;
  };
  dragIng = function (event, d) {
    d.fx = event.x;
    d.fy = event.y;
  };
  dragEnd = function (event, d) {
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  };
  hoverIn = function (event, d) {
    d3.select(this)
      .select("#hover")
      .attr("fill", "#FBEEAC")
      .attr("stroke", "grey")
      .attr("stroke-dasharray", "1 1");
    d3.select(this).select("text").style("display", "inline");
  };
  hoverOut = function (event, d) {
    d3.select(this)
      .select("#hover")
      .attr("fill", "white")
      .attr("stroke", "none");
    d3.select(this)
      .select("text")
      .style("display", (d) => {
        return d.select ? "inline" : "none";
      });
  };
  singleClick = function (event, d) {
    // console.log(d.id);
    // 资料卡数据读入
    if (selectedNode.value != d.id || selectedNode.value == null) {
      // 第一次选中该点
      selectedNode.value = d.id;
      selectedNodeInfo.value = nodeInfo.value[d.id];
      selectedRingLengths.value = [];
      count.value = [0, 0, 0, 0, 0, 0, 0];
      rank.value = 0;
      // console.log(cycles);
      if (cycles[selectedNode.value] !== undefined) {
        for (let i = 0; i <= 4; i++) {
          if (cycles[selectedNode.value][i + 2] !== undefined) {
            count.value[i] = cycles[selectedNode.value][i + 2]["lcount"];
          }
        }
        // console.log(cycles[selectedNode.value]);
        count.value[-1] = cycles[selectedNode.value]["count"];
        rank.value = cycles[selectedNode.value]["rank"];
      }

      nodes
        .select("text")
        .style("fill", (d) => {
          return d.id == selectedNode.value ? "red" : "black";
        })
        .style("display", (d) => {
          return d.id == selectedNode.value ? "inline" : "none";
        });
      nodes
        .select(".select")
        .attr("stroke", (d) => {
          return d.id == selectedNode.value ? "red" : "none";
        })
        .attr("stroke-dasharray", (d) => {
          return d.id == selectedNode.value ? "1 1" : "0 0";
        })
        .style("display", (d) => {
          return d.id == selectedNode.value ? "inline" : "none";
        });
      // if (d.id != history.value[-1]) history.value.push(d.id);
    } else if (selectedNode.value == d.id) {
      // 取消选中该点
      selectedNode.value = null;
      nodes
        .select("text")
        .style("fill", (d) => {
          return d.id == selectedNode.value ? "red" : "black";
        })
        .style("display", (d) => {
          return d.id == selectedNode.value ? "inline" : "none";
        });
      nodes
        .select(".select")
        .attr("stroke", (d) => {
          return "none";
        })
        .attr("stroke-dasharray", (d) => {
          return "0 0";
        })
        .style("display", (d) => {
          return "none";
        });
      // 删除历史记录
      // history.value = history.value.filter((e) => {
      //   if (e != d.id) {
      //     return e;
      //   }
      // });
      selectedNode.value == null;
    }
  };
  doubleClick = function (event, d) {
    // console.log(" db click ");
    // 告诉他爹app， 更改 ego id
    // 让 app 调用 filter 调用 submit

    emit("submit", d.id);
  };
  rightClick = function (d, i) {
    let set = new Set(anomalyList.value.flatMap((e) => e.id));
    if (!set.has(d.target.parentElement.id)) {
      selectedNode.value = d.target.parentElement.id;
      dialogVisible.value = true;
    } else {
      ElMessage.error(
        "Oops, It has been already added in to the anomaly list."
      );
    }
  };
  deleteAnomaly = function (id) {
    anomalyList.value = anomalyList.value.filter((e) => {
      if (e.id != id) return e;
    });
    updateAnomalyList();
  };
}

async function initLinks() {
  links = main
    .append("g")
    .attr("id", "links")
    .selectAll()
    .data([...netData.links1, ...netData.links2])
    .enter()
    .append("path")
    .attr("fill", "none")
    .attr("marker-end", (d) => `url(#arrow-${d.type})`)
    .attr("stroke", (d) => linksTypeColors[d.type])
    .attr("stroke-width", 1)
    .style("opacity", (d) => (netData.links1.has(d) ? 0.75 : 0.25));
}

async function initNodes() {
  nodes = main
    .append("g")
    .attr("id", "nodes")
    .selectAll()
    .data([netData.ego, ...netData.nodes1, ...netData.nodes2])
    .enter()
    .append("g")
    .attr("id", (d) => d.id)
    .call(
      d3.drag().on("start", dragStart).on("drag", dragIng).on("end", dragEnd)
    )
    .on("mouseover", hoverIn)
    .on("mouseout", hoverOut)
    .on("click", singleClick)
    .on("dblclick", doubleClick)
    .on("contextmenu", rightClick);

  // 添加 圆形底
  nodes
    .append("circle")
    .attr("id", "hover")
    .attr("r", 14)
    .attr("fill", "white")
    .attr("transform", `translate(${nodeSize / 2},${nodeSize / 2})`)
    .style("opacity", 0.6);

  nodes
    .append("circle")
    .attr("id", "bottom")
    .attr("r", 14)
    .attr("fill", "white")
    .attr("transform", `translate(${nodeSize / 2},${nodeSize / 2})`)
    .style("opacity", 0.1);

  // 添加单击高亮
  nodes
    .append("circle")
    .attr("class", "select")
    .attr("r", 14)
    .attr("fill", "#F4D160")
    .attr("transform", `translate(${nodeSize / 2},${nodeSize / 2})`)
    .style("display", (d) => {
      if (d.id == netData.ego.id) {
        d.select = true;
        return "inline";
      } else {
        d.select = false;
        return "none";
      }
    });

  // 添加图标以及颜色
  nodes
    .append("use")
    .attr("id", (d) => {
      return d.id;
    })
    .attr("width", nodeSize)
    .attr("height", nodeSize)
    .attr("xlink:href", (d) => {
      return `#${d.type}`;
    })
    .attr("fill", (d) => {
      if (d.id == netData.ego.id) return "blue";
      else if (suspects.has(d.id)) return "red";
      else return "black";
    });
  // 添加名字的 label
  nodes
    .append("text")
    .text((d) => {
      return d.id;
    })
    .attr("dy", -7)
    .attr("fill", "black")
    .attr("text-anchor", "start")
    .style("font-size", 14)
    .style("display", "none");
}

async function initSimulation() {
  // 图的力导向函数
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
  simulation = d3
    .forceSimulation()
    .alphaDecay(0.55)
    .nodes([netData.ego, ...netData.nodes1, ...netData.nodes2])
    .force(
      "link",
      d3
        .forceLink([...netData.links1, ...netData.links2])
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
}

async function initAnomalyList() {
  anomalyList = ref([]);
  anomalyAll = ref();
  await d3.json("data/anomaly_list.json").then((data) => {
    anomalyAll.value = data;
    Object.keys(data).forEach((e) => {
      if (data[e] > 60) {
        anomalyList.value.push({
          id: e,
          weight: data[e].toFixed(3),
        });
      }
    });
  });
  d3.select(".p-fieldset-content").style("padding", 0);
}
async function updateAnomalyList() {
  anomalyList.value = anomalyList.value.sort((a, b) => {
    return b.weight - a.weight;
  });
  if (anomalyList.value.length <= 0) foldList.value = true;
}

async function AddAnomaly() {
  dialogVisible.value = false;
  anomalyList.value.push({
    id: selectedNode.value,
    weight: Number.parseFloat(anomalyAll.value[selectedNode.value]).toFixed(2),
  });
  // console.log(anomalyList.value);
  updateAnomalyList();
}

async function renderEgoNet(net) {
  console.log("render net");
  // 添加 ego 到 历史记录里面
  console.log(net.ego.id);
  history.value.push(net.ego.id);
  console.log(history.value);
  if (
    history.value.length > 1 &&
    history.value[history.value.length - 1] ==
      history.value[history.value.length - 2]
  ) {
    history.value.pop();
  }
  cycles = net.cycles.value;
  netData = net;
  await initContainer();
  await initAnomalyList();
  await updateAnomalyList();
  await initFunctions();
  await initLinks();
  await initNodes();
  await initSimulation();
  // selectedNode.value = netData.ego.id;
  selectedNodeInfo.value = nodeInfo.value[netData.ego.id];
}

const ComponentName = ref("ego");

watch(
  selectedRingLengths,
  (newVal, oldVal) => {
    // console.log("RingLengths update");
    // console.log(newVal, oldVal);
    if (oldVal.length === 0 || oldVal.every((x) => newVal.includes(x))) {
      //新来的只是有所增加
      newVal
        .filter((x) => !oldVal.includes(x))
        .forEach((l) => {
          if (cycles[selectedNode.value][l] !== undefined) {
            let array = Array.from(cycles[selectedNode.value][l]["data"]);
            // let flattenedArray = array.flat().map((item) => JSON.parse(JSON.stringify(item)));
            ringLinks = ringLinks.concat(array);
          }
        });
    } else {
      //有减少，皮肤还原
      for (let i = 0; i < ringLinks.length - 1; i++) {
        let sourceId = ringLinks[i];
        let targetId = ringLinks[i + 1];
        // 选择对应的线元素并修改属性
        links.style("opacity", (d) => {
          // console.log(d.source.id, d.target.id);
          if (netData.links1.has(d)) {
            return 0.75;
          } else return 0.25;
        });
        // 选择对应的点元素并修改属性
        nodes.select("circle").attr("fill", "white").attr("stroke", "none");
      }
      ringLinks = [];
      selectedRingLengths.value.forEach((l) => {
        if (cycles[selectedNode.value][l] !== undefined) {
          let array = Array.from(cycles[selectedNode.value][l]["data"]);
          ringLinks = ringLinks.concat(array);
        }
      });
    }
    for (let i = 0; i < ringLinks.length - 1; i++) {
      let sourceId = ringLinks[i];
      let targetId = ringLinks[i + 1];
      // 选择对应的线元素并修改属性
      links.style("opacity", (d) => {
        // console.log(d.source.id, d.target.id);
        if (sourceId == d.source.id && targetId == d.target.id) {
          return 1;
        } else if (netData.links1.has(d)) {
          return 0.2;
        } else return 0.1;
      });
      // 选择对应的点元素并修改属性
      nodes
        .select("circle")
        .attr("fill", (d) => {
          if (d.id == sourceId || d.id == targetId) {
            return "#FBEEAC";
          } else return "white";
        })
        .attr("stroke-dasharray", "1 1")
        .attr("stroke", (d) => {
          if (d.id == sourceId || d.id == targetId) {
            return "grey";
          } else return "none";
        });
    }
  },
  {
    deep: true,
  }
);
const opacityScale = d3
  .scalePow()
  .exponent(2)
  .domain([0, 100])
  .range([0.3, 0.9]);
watch(showAnomalyInNet, (newV, oldV) => {
  if (newV) {
    let anomalyMap = {};
    anomalyList.value.forEach((a) => {
      anomalyMap[a.id] = anomalyAll.value[a.id];
    });
    nodes
      .select("#bottom")
      .attr("fill", (d) => {
        if (anomalyMap[d.id]) {
          return "rgb(255, 50, 50)";
        } else return "white";
      })
      .style("opacity", (d) => {
        if (anomalyMap[d.id]) {
          let opa = opacityScale(anomalyMap[d.id]).toFixed(1) + "";
          return opa;
        } else return 0.1;
      });
  } else if (!newV) {
    nodes
      .select("#bottom")
      .attr("fill", (d) => {
        return "white";
      })
      .style("opacity", (d) => {
        return 0.1;
      });
  }
});

defineExpose({ renderEgoNet, ComponentName });
</script>
