<template>
  <el-form :model="filter" label-width="120px">
    <el-form-item label="Search by ID" prop="">
      <el-input placeholder="input node id" v-model="filter.select_id" />
    </el-form-item>
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
    <el-form-item label="Hierarchy" v-if="filter.select_id != ''">
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
    <el-form-item label="">
      <el-button type="primary" @click="submit">Submit</el-button>
      <el-button type="info" @click="clear">Clear</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import * as d3 from "d3";
let filter = $ref({
  show1: false, // 显示一阶邻居
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
    show1: false,
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

// let nodes, links;
// d3.json("/MC1.json").then((data) => {
//   nodes = data.nodes;
//   links = data.links;
//   // 遍历 nodes
//   nodes.forEach((node) => {
//     node.type !== undefined ? node_types.add(node.type) : {};
//   });
//   console.log(Array.from(node_types));
//   // 遍历 links
//   links.forEach((link) => {
//     link.type !== undefined ? link_types.add(link.type) : {};
//   });
//   console.log(Array.from(link_types));
// });

const props = defineProps({
  cnt: {
    type: Number,
    required: true,
  },
});
console.log(props);
</script>
