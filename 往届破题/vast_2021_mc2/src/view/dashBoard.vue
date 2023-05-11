<template>
  <d3-abila-map
    :path-coords-to-send="this.pathCoordsToSend" :range-to-abilia="rangeToAbila" :color-map="colorMap"></d3-abila-map>
  <a-select v-model="daySelected" style="position:absolute; top:84%;" placeholder="Please select a Day ..."
            @change="changeRange" id="timePickerD">
    <a-option :value="null" disabled> Select a Day </a-option>
    <a-option v-for="(item, ind) in this.rangeD" :key="ind" :value=item>
      {{ item }}
    </a-option>
  </a-select>
  <a-select v-model="rangeSelected"
            style="position:absolute; top:88%;"
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
      style="position:absolute; top:93%;"
      @get-employers="filterEmployers"
      @get-refresh="refreshMap"
      :employers_lst="this.employers_to_send"
  ></employee-list>
   <three-abila-map style="top:180%;" :path-coords-to-send="this.pathCoordsToSend" :range-to-abilia="rangeToAbila" :color-map="colorMap"></three-abila-map>
</template>

<script>
import * as d3 from "d3";
import d3AbilaMap from "@/components/d3AbilaMap";
import employeeList from "@/components/employeeList";
import threeAbilaMap from "@/components/threeAbilaMap";
// let avg_mvg_a = new Map();
// let avg_mvg_t = new Map();
function formatTime(element) {
  if (element < 10)
    return "0" + (element).toString()
  else
    return element.toString();
}
function findIntervalRange(hour) {
  switch (hour) {
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
      return '10-12';
    case '12':
    case '13':
      return '12-14';
    case '14':
    case '15':
      return '14-16';
    case '16':
    case '17':
      return '16-18';
    case '18':
    case '19':
      return '18-20';
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
    threeAbilaMap,
  },
  data() {
    return {
      rangeD: ['2014-01-06', '2014-01-07', '2014-01-08', '2014-01-09', '2014-01-10', '2014-01-11', '2014-01-12', '2014-01-13',
        '2014-01-14', '2014-01-15', '2014-01-16', '2014-01-17', '2014-01-18', '2014-01-19'],
      rangeH: ['0-24', '0-2', '2-4', '4-6', '6-8', '8-10', '10-12', '12-14', '14-16', '16-18', '18-20', '20-22', '22-24'],
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
      aggrHeatMap: new Map(),
      aggrHeatMapHour: new Map(),
      aggrTrans: true,
      loyalyNum: null,
      EmpType: Array,
      employers: new Map(),
      employers_sel: [],
      selected_all: false,
      colorMap: new Map(),
      group_trans: new Map(),
      group_trans_day: new Map(),
      group_trans_hour: new Map(),
      transactions: [],
      employers_to_send: new Map(),
      rangeSelected: null,
      daySelected: null,
      rangeToAbila: null
    }
  },
  mounted() {

    /** Lettura e Parsing dei due data set */

    function assignColorToPath(colorMap, ind) { //给路径ID赋颜色
      const randomColor = Math.floor(Math.random() * 16777215).toString(16);
      let color = "#" + randomColor;
      colorMap.set(ind, color);
      return colorMap.get(ind);
    }

    function getDuration(h_start, min_start, h_last, min_last) {
      if (h_start === h_last) {
        return Math.abs(min_last - min_start);
      }
      else {
        return Math.abs((min_last + 60) - min_start);
      }
    }


    /* Import Gps and Car Cards Data */
    d3.csv('/csv/df_gps_car.csv')
        .then((rows) => {
          const gps_car = rows
              .map((row, i) => {
                let range = findIntervalRange(row.Hour);
                return {
                  CarID: row.CarID,
                  CurrentEmploymentType: row.CurrentEmploymentType,
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
                  path_id: row.PathID,
                  rangeHour: range
                };
              });
          console.log("gps_car: ", gps_car);
          let Employers_Set = new Set();
          gps_car.forEach((el) => {
            Employers_Set.add(JSON.stringify({
              Fullname: el.fullname, CarID: parseInt(el.CarID),
              Title: el.CurrentEmploymentTitle, Type: el.CurrentEmploymentType
            }))
          })
          console.log("gps-car: ", gps_car);
          console.log("Employer Set: ", Employers_Set);
          let emp_list = []
          function parseSetElements(entry) {
            emp_list.push(JSON.parse(entry));
          }
          Employers_Set.forEach(parseSetElements);
          console.log("Employer List", emp_list);
          let emp_listByType = d3.group(emp_list, d => d.Type)

          console.log("emloyers", emp_listByType);
          this.employers = emp_listByType;
          this.employers_to_send = this.employers;

          /*gps by day and hour and people*/

          const gpsByPath = d3.group(gps_car, v => v.path_id)
          // 元组键值是天和车
          // const gpsByDayCar = d3.group(gps_car, v => v.date +" "+ v.fullName)
          // console.log("group: ", gpsByDay);
          let path_coord = new Map();

          function getHourRange(range_array, hour_start, hour_end) {
            let rangeToReturn = '';
            range_array.forEach((range) => {
              let range_splitted = range.split("-");
              if ((parseInt(hour_end) <= parseInt(range_splitted[1])) && (parseInt(hour_start) >=
                  parseInt(range_splitted[0]))) {
                rangeToReturn = range;
              }
            })
            return rangeToReturn;
          }

          gpsByPath.forEach((el, path) => {
                let coord_list = [];
                console.log("el: ", el)
                // push的是同一个pathid下的所有坐标，就是一个小时内某辆车的坐标
                el.forEach((coord) => {
                      coord_list.push([coord.lat, coord.long]);
                    }
                )
                let r = getHourRange(this.rangeH, formatTime(el[0].hour), formatTime(el[el.length - 1].hour));
                let prop = {
                  "CarID": (el[0].CarID).toString(),
                  "Employer": el[0].fullname,
                  "Type": el[0].CurrentEmploymentType,
                  "Day": el[0].date,
                  "PathId": (el[0].path_id).toString(),
                  "hour_start": formatTime(el[0].hour),
                  "min_start": formatTime(el[0].minutes),
                  "hour_last": formatTime(el[el.length - 1].hour),
                  "min_last": formatTime(el[el.length - 1].minutes),
                  "duration": getDuration(el[0].hour, el[0].minutes, el[el.length - 1].hour, el[el.length - 1].minutes),
                  "range_hour": r
                }
                // if (this.rangeD === el[0].date && this.rangeH === r) {
                path_coord.set(path, [prop, coord_list]);
                // }
              }
          )
          this.pathCoords = path_coord;
          [...this.pathCoords.keys()].forEach(key => {
            assignColorToPath(this.colorMap, key);
          })

          console.log("path coords", this.pathCoords);


          const gpsByEmp = d3.group(gps_car, v => v.fullname, v => v.date);
          let emp_coord = new Map();
          gpsByEmp.forEach((day_map, emp) => {
            let map_day_el = new Map();
            day_map.forEach((arr, day) => {
              let day_list = new Set();
              arr.forEach((ele) => {
                day_list.add(ele.path_id);
              })
              map_day_el.set(day, day_list);
            })
            emp_coord.set(emp, map_day_el);
          })
          this.empCoords = emp_coord;
          console.log("emp_coord", emp_coord);

          const gpsByEmpRange = d3.group(gps_car, v => v.fullname, v => v.date, v => v.rangeHour);
          let emp_coord_hour = new Map();
          gpsByEmpRange.forEach((day_map, emp) => {
            let map_day_el = new Map();
            day_map.forEach((hour_map, day) => {
              let map_hour_el = new Map();
              hour_map.forEach((arr, rangeH) => {
                let hour_list = new Set();
                arr.forEach((ele) => {
                  hour_list.add(ele.path_id);
                })
                map_hour_el.set(rangeH, hour_list);
              })
              map_day_el.set(day, map_hour_el);
            })
            emp_coord_hour.set(emp, map_day_el)
          })
          console.log("emp_coord_hour", emp_coord_hour);

        });
  },
  computed: {
    isAllday() {
      return this.selectedDay === ' ' || this.selectedDay === 0;
    },
    isPathToSendEmpty() {
      return this.pathCoordsToSend.size === 0;
    },
  },
  methods: {
    changeRange(rangeSelected) {
      this.rangeToAbila = rangeSelected;
    },
    refreshMap() {
      console.log("refresh map", this.refresh);
      console.log("refresh path", this.pathCoordsToSend);

      if (this.refresh) {
        this.pathCoordsToSend.clear();
        this.refresh = false;
      }
      else
        this.refresh = true;
    },
    /* Given a List of selected Employers filter the Map */
    filterEmployers(employers_list) {
      this.employers_sel = employers_list;
      // console.log("employers_sel", this.employers_sel);
      // console.log("selectedDay", this.selectedDay.length);
      console.log("select", this.rangeSelected)
      console.log("select hours", this.daySelected)
      /* Given a list of employers filters Stack GPS and Map */
      this.selected_all = false;
      let all_path = [];
      employers_list.forEach((k) => {
        console.log("k", k);
        let empC = this.empCoords.get(k);
        empC.forEach((array_path) => {
          array_path.forEach((el) => {
            {
              // console.log("!!!", el)
              all_path.push(el);
            }
          })
        })
      })
      let path_coords = new Map(this.pathCoords);
      for (let k of path_coords.keys()) {
        // console.log("k now", k);
        if (!(all_path.includes(k))) {
          path_coords.delete(k);
        }
      }
      console.log("pth",path_coords)
      for (let k of path_coords.keys()){

        let path=path_coords.get(k);
        console.log("path left", path);
        if(path[0].range_hour !== this.rangeSelected){
          if(this.rangeSelected!=="0-24")
            path_coords.delete(k);
        }
        if(path[0].Day !== this.daySelected){
          path_coords.delete(k);
        }

      }

      this.pathCoordsToSend = path_coords;//把路径数据传给Abila地图组件
      console.log("final",path_coords);
    },
  }
}
</script>

<style scoped>

</style>
