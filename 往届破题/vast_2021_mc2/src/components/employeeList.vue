<template>
  <div>
    <a-card title="" header-tag="header" footer-tag="footer">
          <a-tabs content-class="mt-3">
            <a-tab-pane key="Engineering" title="Engineering" active>
              <a-table id="t_eng" striped hover
                       row-key="Fullname"
                       @cellClick="addItem"
                       :columns="columns" :data="employers_lst.get('Engineering')" :row-selection="rowSelection"
                       v-model:selectedKeys="selectedKeys"
                       :current-page="currentPage_eng"
                       small>
              </a-table>
            </a-tab-pane>
            <a-tab-pane key="Executive" title="Executive">
              <a-table id="t_eng" striped hover
                       row-key="Fullname"
                       @cellClick="addItem"
                       :columns="columns" :data="employers_lst.get('Executive')" :row-selection="rowSelection"
                       v-model:selectedKeys="selectedKeys"
                       :current-page="currentPage_exec"
                       small>
              </a-table>
            </a-tab-pane>
            <a-tab-pane key="Facilities" title="Facilities">
              <a-table id="t_fac" striped hover
                       row-key="Fullname"
                       @cellClick="addItem"
                       :columns="columns" :data="employers_lst.get('Facilities')" :row-selection="rowSelection"
                       v-model:selectedKeys="selectedKeys"
                       :current-page="currentPage_fac"
                       small>
              </a-table>
            </a-tab-pane>
            <a-tab-pane key="Information" title="Information Technology">
              <a-table id="t_IT" striped hover
                       row-key="Fullname"
                       @cellClick="addItem"
                       :columns="columns" :data="employers_lst.get('Information Technology')" :row-selection="rowSelection"
                       v-model:selectedKeys="selectedKeys"
                       :current-page="currentPage_IT"
                       small>
              </a-table>
            </a-tab-pane>
            <a-tab-pane key="Security" title="Security">
              <a-table id="t_sec" striped hover
                       row-key="Fullname"
                       @cellClick="addItem"
                       :columns="columns" :data="employers_lst.get('Security')" :row-selection="rowSelection"
                       v-model:selectedKeys="selectedKeys"
                       :current-page="currentPage_sec"
                       small>
              </a-table>
            </a-tab-pane>
          </a-tabs>
    </a-card>
  </div>
</template>
<script>
import { reactive, ref } from 'vue';
const selectedKeys = ref(['Lars Azada']);//设置一个默认值
const rowSelection = reactive({
  type: 'checkbox',
  showCheckedAll: true,
  onlyCurrent: false,
});
export default {
  name: "employeeList",
  props:{
    employers_lst: Map,
    selected_all: Boolean,
    refresh: Boolean
  },
  data() {
    return {
      currentPage_sec: 1,
      currentPage_eng: 1,
      currentPage_fac:1,
      currentPage_exec:1,
      currentPage_IT:1,
      currentPage_all: 1,
      sec_sel: [],
      eng_sel: [],
      fac_sel: [],
      IT_sel: [],
      exec_sel:[],
      exec_len:0,
      IT_len:0,
      fac_len:0,
      sec_len:0,
      eng_len:0,
      selectedKeys,
      rowSelection,
      columns: [
          {
            title: "Fullname",
            dataIndex: "Fullname",
          },
        {
          title:"CarID",
          dataIndex: "CarID",
        },
        {
          title:"Title",
          dataIndex: "Title",
        }],
      layout: {
        height:351,
        annotations: []
      }
    }
  },
  watch: {
    // whenever data changes, this function will run
    employers_lst(employers) {
      console.log("employers In Component Child", this.employers_lst);
      this.employers_lst.get("Engineering").forEach( (item)=>{
        if (this.eng_sel.filter(e => e.Fullname === item.Fullname).length > 0) {
          console.log("item incluso",item);
        }
        else console.log("non lo include", item);
      })
      console.log("Current Page", employers.get("Engineering").length);
      console.log("eng sel",this.eng_sel);
      this.exec_len = employers.get("Executive").length;
      this.eng_len = employers.get("Engineering").length;
      this.IT_len = employers.get("Information Technology").length;
      this.fac_len = employers.get("Facilities").length;
      this.sec_len = employers.get("Security").length;
      this.currentPage_IT = 1;
      this.currentPage_fac = 1;
      this.currentPage_eng  = 1;
      this.currentPage_sec  = 1;
      this.currentPage_exec  = 1;
    },
  },
  methods: {
    addItem() {
      console.log(this.selectedKeys)
      const emp = this.selectedKeys;
      this.$emit('get-employers', emp);
    },
    deleteItem(item,type) {
      switch (type){
        case 'Security':
          this.sec_sel.splice(this.sec_sel.indexOf(item), 1);
          break;
        case 'Executive':
          this.exec_sel.splice(this.exec_sel.indexOf(item), 1);
          break;
        case 'Information Technology':
          this.IT_sel.splice(this.IT_sel.indexOf(item), 1);
          break;
        case 'Facilities':
          this.fac_sel.splice(this.fac_sel.indexOf(item), 1);
          break;
        case 'Engineering':
          this.eng_sel.splice(this.eng_sel.indexOf(item), 1);
          break;
      }
      /*remove element for filter graphs*/
      this.employers_selected.splice(this.employers_selected.indexOf(item), 1);
      const emp = this.employers_selected;
      this.$emit('get-employers', emp);
    },
    selectAll(type,send){
      console.log("sono stato chiamato",type);
      switch (type){
        case 'Security':
          this.employers_lst.get('Security').forEach((element) => {
            if(!this.sec_sel.includes(element)){
              this.sec_sel.push(element);
              this.employers_selected.push(element);
            }
          })
          break;
        case 'Executive':
          this.employers_lst.get('Executive').forEach((element) => {
            if(!this.exec_sel.includes(element)){
              this.exec_sel.push(element);
              this.employers_selected.push(element);
              console.log("emp selected",this.employers_selected);

            }
          })
          break;
        case 'Information Technology':
          this.employers_lst.get('Information Technology').forEach((element) => {
            if(!this.IT_sel.includes(element)){
              this.IT_sel.push(element);
              this.employers_selected.push(element);
              console.log("emp selected",this.employers_selected);

            }
          })
          break;
        case 'Facilities':
          this.employers_lst.get('Facilities').forEach((element) => {
            if(!this.fac_sel.includes(element)){
              this.fac_sel.push(element);
              this.employers_selected.push(element);
              console.log("emp selected",this.employers_selected);

            }
          })
          break;
        case 'Engineering':
          this.employers_lst.get('Engineering').forEach((element) => {
            if(!this.eng_sel.includes(element)){
              this.eng_sel.push(element);
              this.employers_selected.push(element);
              console.log("emp selected",this.employers_selected);
            }
          })
          break;
      }
      if(send){
        const emp = this.employers_selected;
        this.$emit('get-employers', emp);
      }
    },
    clearAll(type){
      switch (type){
        case 'Security':
          this.employers_lst.get('Security').forEach((element) => {
            if(this.sec_sel.includes(element)){
              const index = this.sec_sel.indexOf(element);
              this.sec_sel.splice(index, 1);
              this.employers_selected.splice(this.employers_selected.indexOf(element), 1);
            }
          })
          break;
        case 'Executive':
          this.employers_lst.get('Executive').forEach((element) => {
            if(this.exec_sel.includes(element)){
              const index = this.exec_sel.indexOf(element);
              this.exec_sel.splice(index, 1);
              this.employers_selected.splice(this.employers_selected.indexOf(element), 1);
            }
          })
          break;
        case 'Information Technology':
          this.employers_lst.get('Information Technology').forEach((element) => {
            if(this.IT_sel.includes(element)){
              const index = this.IT_sel.indexOf(element);
              this.IT_sel.splice(index, 1);
              this.employers_selected.splice(this.employers_selected.indexOf(element), 1);
            }
          })
          break;
        case 'Engineering':
          this.employers_lst.get('Engineering').forEach((element) => {
            if(this.eng_sel.includes(element)){
              const index = this.eng_sel.indexOf(element);
              this.eng_sel.splice(index, 1);
              this.employers_selected.splice(this.employers_selected.indexOf(element), 1);
            }
          })
          break;
        case 'Facilities':
          this.employers_lst.get('Facilities').forEach((element) => {
            if(this.fac_sel.includes(element)){
              const index = this.fac_sel.indexOf(element);
              this.fac_sel.splice(index, 1);
              this.employers_selected.splice(this.employers_selected.indexOf(element), 1);
            }
          })
          break;
      }
      const emp = this.employers_selected;
      this.$emit('get-employers', emp);
    }
  }
}
</script>

<style scoped>

</style>
