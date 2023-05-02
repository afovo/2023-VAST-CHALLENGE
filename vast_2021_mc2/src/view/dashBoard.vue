<template>
  <d3-abila-map
    :path-coords-to-send="this.pathCoordsToSend" :range-to-abilia="rangeToAbila" :color-map="colorMap"></d3-abila-map> -->
   <!-- <three-abila-map :path-coords-to-send="this.pathCoordsToSend" :range-to-abilia="rangeToAbila" :color-map="colorMap"></three-abila-map> -->
    <a-select v-model="rangeSelected"
            style="position:absolute; top:83%;"
            placeholder="Please select a Range Hour ..."
            @change="changeRange"
            id="timePickerS">
    <a-option :value="null" disabled>  Select a Range Hour  </a-option>
    <a-option v-for="(item,ind) in this.rangeH"
              :key="ind"
              :value=item>
      {{ item }}
    </a-option>
  </a-select>
<!--  ToDo: 日期选取   参考 https://arco.design/vue/component/date-picker   范围看public/csv/df_gps_car-->
  <employee-list
      style="position:absolute; top:88%;"
      @get-employers="filterEmployers"
      @get-refresh="refreshMap"
      :employers_lst="this.employers_to_send"
  ></employee-list>

 <!-- <three-abila-map style="top:100%;"></three-abila-map> -->
</template>

<script>
import * as d3 from "d3";
import employeeList from "@/components/employeeList";
import d3AbilaMap from "@/components/d3AbilaMap";
// import threeAbilaMap from "@/components/threeAbilaMap";
let avg_mvg_a = new Map();
let avg_mvg_t = new Map();
function formatTime(element) {
  if(element < 10)
    return "0"+(element).toString()
  else
    return element.toString();
}
function findIntervalRange(hour){
  switch (hour){
    case '0':
    case '1':
      return '0-2';
    case '2':
    case '3':
      return '2-4';
    case '4':
    case '5':
      return '4-6';
    case '6':
    case '7':
      return '6-8';
    case '8':
    case '9':
      return '8-10';
    case '10':
    case '11':
      return  '10-12';
    case '12':
    case '13':
      return  '12-14';
    case '14':
    case '15':
      return  '14-16';
    case '16':
    case '17':
      return '16-18';
    case '18':
    case '19':
      return  '18-20';
    case '20':
    case '21':
      return '20-22';
    case '22':
    case '23':
      return '22-24';
  }
}
export default {
  name: "dashBoard",
  components: {
    employeeList,
    d3AbilaMap,
    // threeAbilaMap,
  },
  data() {
    return {
      rangeH: ['0-2','2-4','4-6','6-8','8-10','10-12','12-14','14-16','16-18','18-20','20-22', '22-24'],
      refresh: false,
      dataPayments: Array,
      pathCoords: new Map(),
      pathCoordsToSend: new Map(),
      dayCoords: new Map(),
      empCoords: new Map(),
      selectedDay: '',
      loc_amount: new Map(),
      loc_trans: new Map(),
      aggrBarChartMap: new Map(),
      hour_amount: new Map(),
      hour_trans: new Map(),
      day_amount: new Map(),
      day_trans: new Map(),
      ht_amount: new Map(),
      ht_trans: new Map(),
      aggrHeatMap:new Map(),
      aggrHeatMapHour:new Map(),
      aggrTrans:true,
      loyalyNum: null,
      EmpType: Array,
      employers: new Map(),
      employers_sel: [],
      selected_all: false,
      colorMap: new Map(),
      group_trans: new Map(),
      group_trans_day: new Map(),
      group_trans_hour:new Map(),
      transactions: [],
      employers_to_send: new Map(),
      rangeSelected: null,
      rangeToAbila: null
    }},
  mounted() {

    /** Lettura e Parsing dei due data set */

    d3.csv('/csv/df_cc_loyalty.csv')
        .then((rows) => {
          let cc_loyalty_cards = rows
              .map((row) => {

                //from string to date
                const dateParse = d3.timeParse("%Y-%m-%d");
                const dateF = dateParse(row.date)

                /*Add a String to indicate method of payment of employee*/
                let method;
                if(row.last4ccnum === 'No')
                  method = 'Loyalty'
                else if (row.loyaltynum === 'No')
                  method = 'Card'
                else
                  method = 'Both'
                let range = findIntervalRange(row.Hour);
                if(range === '0-2')
                  console.log("range 0-2",range)
                return {
                  Date: dateF,
                  location: row.location,
                  price: +row.price,
                  last4ccnum: row.last4ccnum,
                  loyaltynum: row.loyaltynum,
                  date: row.date,
                  hour: row.Hour,
                  minutes: row.Minutes,
                  method: method,
                  rangeHour: range,
                };
              });
          // Let's calculate some aggregation for the stack bar chart
          console.log("cc_loyalty_cards filterd", cc_loyalty_cards);
          this.dataPayments = cc_loyalty_cards;
          // count transaction per location and method
          this.loc_trans = d3.rollup(cc_loyalty_cards, v => v.length, d => d.location,d => d.method)
          this.group_trans = d3.group(cc_loyalty_cards, d => d.location,d => d.method);
          this.group_trans_day = d3.group(cc_loyalty_cards, d => d.location,d => d.date);
          this.group_trans_hour = d3.group(cc_loyalty_cards, d => d.location,d => d.rangeHour);
          console.log("raggruppamento per ora",this.group_trans_hour);
          const l_t_All = d3.rollup(cc_loyalty_cards, v => v.length, d => d.location)
          avg_mvg_t = d3.rollup(cc_loyalty_cards, v => v.length, d => d.location, d=>d.date)
          avg_mvg_t.forEach((day_v_map,loc) => {
            let sum = 0;
            day_v_map.forEach((v) => {
              sum = sum + v;
            })
            avg_mvg_t.set(loc,Math.round(sum/day_v_map.size));
          })
          console.log("ALL", avg_mvg_t)
          this.loc_trans.forEach((value, key) => {
            value.set("All",l_t_All.get(key));
            value.set("Avg",avg_mvg_t.get(key));
          } )
          // total amount per location and method
          this.loc_amount = d3.rollup(cc_loyalty_cards, v => d3.sum(v, d => d.price), d => d.location,d => d.method)
          const l_a_All = d3.rollup(cc_loyalty_cards, v => d3.sum(v, d => d.price), d => d.location)
          avg_mvg_a = d3.rollup(cc_loyalty_cards, v => d3.sum(v, d => d.price), d => d.location, d=>d.date);
          avg_mvg_a.forEach((day_v_map,loc) => {
            let sum = 0;
            day_v_map.forEach((v) => {
              sum = sum + v;
            })
            avg_mvg_a.set(loc,Math.round(sum/day_v_map.size));
          })
          this.loc_amount.forEach((value, key) => {
            value.set("All",l_a_All.get(key));
            value.set("Avg",avg_mvg_a.get(key));
          } )

          this.aggrBarChartMap = this.loc_trans;
          console.log("Location Amount: ", this.group_trans);

          // total amount per range hour and location

          this.hour_amount = d3.rollup(cc_loyalty_cards, v => d3.sum(v, d => d.price),d => d.rangeHour, d => d.location)
          this.hour_trans = d3.rollup(cc_loyalty_cards, v => v.length, d => d.rangeHour,d => d.location)
          this.day_trans = d3.rollup(cc_loyalty_cards, v => v.length, d => d.date,d => d.location)
          this.day_amount = d3.rollup(cc_loyalty_cards,  v => d3.sum(v, d => d.price), d => d.date,d => d.location)

          this.aggrHeatMap  = this.day_trans;
          this.aggrHeatMapHour = this.hour_trans;

        });

    function assignColorToPath(colorMap,ind){ //给路径ID赋颜色
      const randomColor = Math.floor(Math.random()*16777215).toString(16);
      let color= "#" + randomColor;
      colorMap.set(ind,color);
      return colorMap.get(ind);
    }

    function getDuration(h_start, min_start, h_last, min_last) {
      if(h_start === h_last){
        return Math.abs(min_last - min_start);
      }
      else{
        return Math.abs((min_last + 60) - min_start);
      }
    }


    /* Import Gps and Car Cards Data */
    d3.csv('/csv/df_gps_car.csv')
        .then((rows) => {
          const gps_car = rows
              .map((row,i) => {
                let range = findIntervalRange(row.Hour);
                return {
                  CarID: row.CarID,
                  CurrentEmploymentType:  row.CurrentEmploymentType,
                  CurrentEmploymentTitle: row.CurrentEmploymentTitle,
                  fullname: row.FullName,
                  lat: row.lat,
                  long: row.long,
                  coordinate: row.lat + " " + row.long,
                  date: row.date,
                  hour: row.Hour,
                  minutes: row.Minutes,
                  seconds: row.Seconds,
                  timestamp_id: i,
                  path_id : row.PathID,
                  rangeHour:range
                };
              });
          console.log("gps_car: ", gps_car);
          let Employers_Set = new Set();
          gps_car.forEach((el) => {
            Employers_Set.add(JSON.stringify({Fullname: el.fullname, CarID: parseInt(el.CarID),
              Title: el.CurrentEmploymentTitle, Type:el.CurrentEmploymentType}))})
          console.log("Employer Set: ", Employers_Set);
          let emp_list = []
          function parseSetElements(entry) {
            emp_list.push(JSON.parse(entry));
          }
          Employers_Set.forEach(parseSetElements);
          console.log("Employer List",emp_list);
          let emp_listByType = d3.group(emp_list, d => d.Type)

          console.log("emloyers",emp_listByType);
          this.employers = emp_listByType;
          this.employers_to_send = this.employers;

          /*gps by path*/

          const gpsByPath = d3.group(gps_car, v => v.path_id)
          let path_coord = new Map();

          function getHourRange(range_array, hour_start, hour_end) {
            let rangeToReturn = '';
            range_array.forEach((range) => {
              let range_splitted = range.split("-");
              if((parseInt(hour_end)<=parseInt(range_splitted[1])) && (parseInt(hour_start)>=
                  parseInt(range_splitted[0]))) {
                rangeToReturn = range;
              }
            })
            return rangeToReturn;
          }

          /* create a map that link each path with its coordinates list */
          gpsByPath.forEach((el,path) => {
                let coord_list = [];
                el.forEach((coord) =>{
                      coord_list.push([coord.lat,coord.long]);
                    }
                )
                let r = getHourRange(this.rangeH,formatTime(el[0].hour),formatTime(el[el.length-1].hour));
                let prop = {"CarID": (el[0].CarID).toString(),
                  "Employer": el[0].fullname,
                  "Type": el[0].CurrentEmploymentType,
                  "Day": el[0].date,
                  "PathId":(el[0].path_id).toString(),
                  "hour_start":formatTime(el[0].hour),
                  "min_start": formatTime(el[0].minutes),
                  "hour_last": formatTime(el[el.length-1].hour),
                  "min_last":formatTime(el[el.length-1].minutes),
                  "duration":getDuration(el[0].hour,el[0].minutes,el[el.length-1].hour,el[el.length-1].minutes),
                  "range_hour": r
                }
                path_coord.set(path,[prop,coord_list]);
              }
          )
          this.pathCoords = path_coord;
          [...this.pathCoords.keys()].forEach(key => {
            assignColorToPath(this.colorMap, key);
          })

          console.log("path coords", this.pathCoords);
          /*gps by day and emp*/
          const gpsByDay = d3.group(gps_car, v => v.date, v=>v.fullname)
          let day_coord = new Map();
          gpsByDay.forEach((dip_map,day) => {
            let map_dip_el = new Map();
            dip_map.forEach((arr,dip) => {
              let dip_list = new Set();
              arr.forEach((ele) => {
                dip_list.add(ele.path_id);
              })
              map_dip_el.set(dip,dip_list);
            })
            day_coord.set(day,map_dip_el);
          })
          this.dayCoords = day_coord; //ToDo: filter by day
          console.log("GPS DATA  IN DASH",day_coord);

          const gpsByEmp = d3.group(gps_car, v=>v.fullname, v => v.date);
          let emp_coord = new Map();
          gpsByEmp.forEach((day_map,emp) => {
            let map_day_el = new Map();
            day_map.forEach((arr,day) => {
              let day_list = new Set();
              arr.forEach((ele) => {
                day_list.add(ele.path_id);
              })
              map_day_el.set(day,day_list);
            })
            emp_coord.set(emp,map_day_el);
          })
          this.empCoords = emp_coord;
          console.log("emp_coord", emp_coord);

          const gpsByEmpRange = d3.group(gps_car, v=>v.fullname, v => v.date, v=>v.rangeHour);
          let emp_coord_hour = new Map();
          gpsByEmpRange.forEach((day_map,emp) => {
            let map_day_el = new Map();
            day_map.forEach((hour_map,day) => {
              let map_hour_el = new Map();
              hour_map.forEach((arr,rangeH) => {
                let hour_list = new Set();
                arr.forEach((ele) => {
                  hour_list.add(ele.path_id);
                })
                map_hour_el.set(rangeH,hour_list);
              })
              map_day_el.set(day,map_hour_el);
            })
            emp_coord_hour.set(emp,map_day_el)
          })
          console.log("emp_coord_hour", emp_coord_hour);

        });
  },
  computed:{
    isAllday(){
      return this.selectedDay === ' ' || this.selectedDay === 0;
    },
    isPathToSendEmpty(){
      return this.pathCoordsToSend.size === 0;
    },
  },
  methods: {
    changeRange(rangeSelected){
      this.rangeToAbila = rangeSelected;
    },
    refreshMap(){
      console.log("refresh map", this.refresh);
      console.log("refresh path", this.pathCoordsToSend);

      if(this.refresh){
        this.pathCoordsToSend.clear();
        this.refresh = false;
      }
      else
        this.refresh = true;
    },

    // filterDay(day) {
    //   this.selectedDay = day;
    //
    //   /* Given a Date(day) filters Stack BarChart and HeatMap */
    //
    //   //filter bar chart stack per day selected
    //   let cc_loyalty_cards = this.dataPayments;
    //   /*check if day is not empty*/
    //   if (day && this.loyalyNum )  {
    //     cc_loyalty_cards =  cc_loyalty_cards.filter(d => d.date === day);
    //     cc_loyalty_cards =  cc_loyalty_cards.filter(d => d.loyaltynum === this.loyalyNum);
    //   }
    //   else if(day){
    //     cc_loyalty_cards =  cc_loyalty_cards.filter(d => d.date === day);
    //   }
    //   this.group_trans = d3.group(cc_loyalty_cards, d => d.location,d => d.method);
    //   this.group_trans_day = d3.group(cc_loyalty_cards, d => d.location,d => d.date);
    //   this.group_trans_hour = d3.group(cc_loyalty_cards, d => d.location,d => d.rangeHour);
    //   this.loc_trans = d3.rollup(cc_loyalty_cards, v => v.length, d => d.location,d => d.method)
    //   const l_t_All = d3.rollup(cc_loyalty_cards, v => v.length, d => d.location)
    //   this.loc_trans.forEach((value, key) => {
    //     value.set("All",l_t_All.get(key));
    //     value.set("Avg",avg_mvg_t.get(key));
    //   } )
    //   this.loc_amount = d3.rollup(cc_loyalty_cards, v => d3.sum(v, d => d.price), d => d.location,d => d.method)
    //   const l_a_All = d3.rollup(cc_loyalty_cards, v => d3.sum(v, d => d.price), d => d.location)
    //   this.loc_amount.forEach((value, key) => {
    //     value.set("All",l_a_All.get(key));
    //     value.set("Avg",avg_mvg_a.get(key));
    //   } )
    //
    //   // filter heatmap per day selected
    //   this.hour_amount = d3.rollup(cc_loyalty_cards, v => d3.sum(v, d => d.price),d => d.rangeHour, d => d.location)
    //   this.hour_trans = d3.rollup(cc_loyalty_cards, v => v.length, d => d.rangeHour,d => d.location)
    //   if(this.aggrTrans){
    //     this.aggrHeatMapHour = this.hour_trans;
    //     this.aggrBarChartMap = this.loc_trans;
    //   }
    //   else{
    //     this.aggrHeatMapHour = this.hour_amount;
    //     this.aggrBarChartMap = this.loc_amount;
    //   }
    //
    //   /* Given a Date(day) filters Stack GPS and Map */
    //   if(day) {
    //     console.log("day");
    //     /* case in which there is no employer select yet*/
    //     if (this.employers_sel.length === 0) {
    //       this.selected_all = true;
    //     } else {
    //       this.selected_all = false;
    //       let all_path = [];
    //       this.employers_sel.forEach((k) => {
    //         console.log("k", k);
    //         if(this.dayCoords.get(day).has(k)){
    //           let dayC = this.dayCoords.get(day).get(k);
    //           console.log("dayC else", dayC);
    //           dayC = Array.from(dayC);
    //           dayC.forEach((el) => {
    //             all_path.push(el);
    //           })
    //         }
    //       })
    //       let path_coords = new Map(this.pathCoords);
    //       for (let k of path_coords.keys()) {
    //         if (!(all_path.includes(k))) {
    //           path_coords.delete(k);
    //         }
    //       }
    //       this.pathCoordsToSend = path_coords;
    //     }
    //   } else{
    //     console.log("Giorno non c'è",this.pathCoordsToSend.clear());
    //     this.filterEmployers(this.employers_sel);
    //   }
    //   /*Filter list of employers */
    //   if(day){
    //     let dayCoords = this.dayCoords;
    //     dayCoords =  dayCoords.get(day);
    //
    //     let employer_type = new Map(
    //         JSON.parse(
    //             JSON.stringify(Array.from(this.employers))
    //         )
    //     );
    //     let emp_type = new Map();
    //     let emp_per_day  = [...dayCoords.keys()];
    //
    //     employer_type.forEach((arr_emp,type) =>{
    //       let list_emp = [];
    //       arr_emp.forEach( v => {
    //         if((emp_per_day.includes(v.Fullname))){
    //           list_emp.push(v);
    //         }
    //       })
    //       emp_type.set(type,list_emp);
    //     })
    //     console.log("Filter emplo list per day 2", emp_type);
    //     this.employers_to_send = emp_type;
    //   }
    //   else {
    //     this.employers_to_send = this.employers;
    //   }
    // },

    // toggleSideBar(stack){
    //   console.log("stack in dash", stack['label']);
    //   let g_trans = new Map(this.group_trans);
    //   let trans_array = g_trans.get(stack['label']);
    //   let transaction_to_send = new Map();
    //   console.log("transaction in toggle", trans_array);
    //   trans_array.forEach((array_details,method) => {
    //     if((stack['cc'].includes(method))){
    //       transaction_to_send.set(method,array_details);
    //     }
    //   })
    //
    //   let values = [...transaction_to_send.values()].flat(1);
    //   values = values.map(function(e) {
    //     e.hour = formatTime(parseInt(e.hour));
    //     e.minutes =formatTime(parseInt(e.minutes));
    //     return e;
    //   });
    //
    //   console.log("values to send",values);
    //
    //   this.transactions = values;
    //   console.log("transaction in toggle", this.transactions);
    //   this.$root.$emit('bv::toggle::collapse', 'sidebar-1');
    // },
    // toggleSideBarDay(ht){
    //   console.log("heat in dash", ht);
    //   let g_trans = new Map(this.group_trans_day);
    //   let trans_array = g_trans.get(ht['x']).get(ht['y']);
    //   //let transaction_to_send = new Map();
    //   console.log("HeatMap Toggle", typeof(trans_array));
    //   if(typeof(trans_array)!='undefined'){
    //     trans_array = trans_array.map(function(e) {
    //       e.hour = formatTime(parseInt(e.hour));
    //       e.minutes =formatTime(parseInt(e.minutes));
    //       return e;
    //     });
    //     this.transactions = trans_array;
    //     console.log("transaction in toggle", this.transactions);
    //     this.$root.$emit('bv::toggle::collapse', 'sidebar-1');
    //   }
    // },
    // toggleSideBarHour(ht){
    //   console.log("heat in dash", ht);
    //   let g_trans = new Map(this.group_trans_hour);
    //   let trans_array = g_trans.get(ht['x']).get(ht['y']);
    //   //let transaction_to_send = new Map();
    //   console.log("HeatMap Toggle", trans_array);
    //   if(typeof(trans_array)!='undefined'){
    //     trans_array = trans_array.map(function(e) {
    //       e.hour = formatTime(parseInt(e.hour));
    //       e.minutes =formatTime(parseInt(e.minutes));
    //       return e;
    //     });
    //     this.transactions = trans_array;
    //     console.log("transaction in toggle", this.transactions);
    //     this.$root.$emit('bv::toggle::collapse', 'sidebar-1');
    //   }
    // },


    /* Given a List of selected Employers filter the Map */
    filterEmployers(employers_list){
      this.employers_sel = employers_list;
      console.log("selectedDay", this.selectedDay.length);

      /* Given a list of employers filters Stack GPS and Map */
        this.selected_all = false;
        let all_path = [];
        employers_list.forEach((k) => {
          console.log("k",k);
          let empC = this.empCoords.get(k);
          empC.forEach((array_path) => {
            array_path.forEach((el) => {
              all_path.push(el);
            })
          })
        })
        let path_coords = new Map(this.pathCoords);
        for (let k of path_coords.keys()) {
          if (!(all_path.includes(k))) {
            path_coords.delete(k);
          }
        }
        this.pathCoordsToSend = path_coords;//把路径数据传给Abila地图组件
        console.log(path_coords);
    },
  }
}
</script>

<style scoped>

</style>
