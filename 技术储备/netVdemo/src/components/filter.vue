<template>
  <el-form :model="filter" label-width="120px">
    <el-form-item label="Search by ID" prop="">
      <el-input placeholder="input node id" v-model="filter.select_id" />
    </el-form-item>
    <el-form-item label="Quick Select" prop="">
      <el-radio-group v-model="filter.select_id" class="ml-4">
        <el-radio v-for="id in Array.from(entities)" :label="id">{{
          id
        }}</el-radio>
      </el-radio-group></el-form-item
    >

    <el-form-item label="Node Type" prop="">
      <el-checkbox
        v-for="type in Object.keys(filter.node_types)"
        v-model="filter.node_types[type]"
        :label="type"
    /></el-form-item>
    <el-form-item label="Link Type" prop="">
      <el-checkbox
        v-for="type in Object.keys(filter.link_types)"
        v-model="filter.link_types[type]"
        :label="type"
      />
    </el-form-item>
    <el-form-item label="Out Degree" prop=""></el-form-item>
    <el-form-item label="In  Degree" prop=""></el-form-item>
    <div v-if="filter.select_id != ''">
      <el-form-item label="Hierarchy">
        <el-switch
          v-model="filter.show1"
          active-text="First-Order"
          style="margin-left: 10px"
        />
        <el-switch
          v-model="filter.show2"
          active-text="Second-Order"
          style="margin-left: 20px"
        />
      </el-form-item>
    </div>
    <el-form-item label="">
      <el-button type="primary" @click="submit">Submit</el-button>
      <el-button type="info" @click="clear">Clear</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import * as d3 from "d3";
let filter = $ref({
  show1: true, // 显示一阶邻居
  show2: false, // 显示二阶邻居
  node_types: {
    company: false,
    organization: false,
    person: false,
    location: false,
    political_organization: false,
    vessel: false,
    movement: false,
    event: false,
  }, // 节点类型
  link_types: {
    ownership: false,
    partnership: false,
    family_relationship: false,
    membership: false,
  }, // 边的类型
  select_id: "", //根据id搜索节点
});
const submit = function () {};
const clear = function () {
  filter = {
    show1: true,
    show2: false,
    node_types: {
      company: false,
      organization: false,
      person: false,
      location: false,
      political_organization: false,
      vessel: false,
      movement: false,
      event: false,
    },
    link_types: {
      ownership: false,
      partnership: false,
      family_relationship: false,
      membership: false,
    },
    select_id: "",
  };
};

let nodes, links, source, target, cneter;

let entities = new Set([
  "Mar de la Vida OJSC",
  "979893388",
  "Oceanfront Oasis Inc Carrie",
  "8327",
]);

// mini json 的处理过程如下

// let data, first, second, first_link, second_link;
// d3.json("MC1.json").then((d) => {
//   nodes = d.nodes;
//   links = d.links;
//   data = {};
//   Array.from(entities).forEach((ego) => {
//     first = new Set();
//     first_link = new Set();
//     second = new Set();
//     second_link = new Set();
//     // 第一遍遍历 links，获取一阶邻居
//     links.forEach((link) => {
//       source = link.source.toString();
//       target = link.target.toString();
//       if (source == ego) {
//         first.add(target);
//         first_link.add({
//           source: source,
//           target: target,
//         });
//       }
//       if (target == ego) {
//         first.add(source);
//         first_link.add({
//           source: source,
//           target: target,
//         });
//       }
//     });
//     // 第二遍遍历 links，获取不与 center 直接连线的二阶邻居
//     links.forEach((link) => {
//       source = link.source.toString();
//       target = link.target.toString();
//       if (
//         // 不与 center 直接相连
//         source !== ego &&
//         target !== ego &&
//         // 且不能两端都在一阶中
//         !(first.has(source) && first.has(target))
//       ) {
//         if (first.has(source)) {
//           second.add(target);
//           second_link.add({
//             source: source,
//             target: target,
//           });
//         }
//         if (first.has(target)) {
//           second.add(source);
//           second_link.add({
//             source: source,
//             target: target,
//           });
//         }
//       }
//     });
//     data[ego] = {
//       first: Array.from(first),
//       second: Array.from(second),
//       first_link: Array.from(first_link),
//       second_link: Array.from(second_link),
//     };
//   });
//   console.log(data);
// });

// 预览mini json
// d3.json("mini.json").then((d) => {
//   console.log(d);
// });
</script>
