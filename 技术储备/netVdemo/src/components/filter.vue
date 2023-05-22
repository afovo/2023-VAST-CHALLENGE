<template>
  <el-form :v-model="filter" label-width="120px">
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

    <el-form-item label="Out Degree" prop="">
      <el-button style="width: 5rem"
        >min:{{ filter.out_degree_range[0] }}</el-button
      >
      <el-slider
        range
        show-stops
        :step="1"
        :min="1"
        :max="400"
        v-model="filter.out_degree_range"
        style="width: 600px"
      />
      <el-button style="width: 5rem"
        >max:{{ filter.out_degree_range[1] }}</el-button
      >
    </el-form-item>
    <el-form-item label="In Degree" prop="">
      <el-button style="width: 5rem"
        >min:{{ filter.in_degree_range[0] }}</el-button
      >
      <el-slider
        range
        show-stops
        :step="1"
        :min="1"
        :max="400"
        v-model="filter.in_degree_range"
        style="width: 600px"
      />
      <el-button style="width: 5rem"
        >max:{{ filter.in_degree_range[1] }}</el-button
      >
    </el-form-item>
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
      <el-button type="success" @click="submit">Submit</el-button>
      <el-button type="info" @click="clear">Clear</el-button>
    </el-form-item>
  </el-form>
</template>
<style>
.el-slider__runway {
  margin-left: 40px;
  margin-right: 40px;
}
</style>
<script setup>
import * as d3 from "d3";
let filter = $ref({
  show1: true, // 显示一阶邻居
  show2: false, // 显示二阶邻居
  out_degree_range: [50, 100],
  in_degree_range: [50, 200],
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
let entities = new Set([
  "Mar de la Vida OJSC",
  "979893388",
  "Oceanfront Oasis Inc Carrie",
  "8327",
]);
const submit = function () {};
const clear = function () {
  filter = {
    show1: true, // 显示一阶邻居
    show2: false, // 显示二阶邻居
    out_degree_range: [50, 100],
    in_degree_range: [50, 200],
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
  };
};
</script>
