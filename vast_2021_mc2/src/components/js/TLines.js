import {
    LineBasicMaterial,
    BufferGeometry,
    Vector3,
    Line,
    // Color,
    // MeshLambertMaterial,
    // DoubleSide,
    // Mesh
} from "three"
// import {FontLoader} from "three/examples/jsm/loaders/FontLoader";

// import {Line2} from "three/examples/jsm/lines/Line2.js"
import tkJson from './tracks.json'
import * as d3 from "d3";
export const allTrackLines = []

var material = new LineBasicMaterial({ color: 0xFF0000 });

let xScale = d3.scaleLinear().domain([20, 30]).range([-1035, 1095]);//地图太小了 比例尺放大
let yScale = d3.scaleLinear().domain([30, 40]).range([-1290, 840]);
let cnt=0;
tkJson.forEach(element => {
    cnt+=1;
    const geometry = new BufferGeometry();
    const pointsArray = [];
    if (element.date == "2014-01-06" && element.carID == "1") {
        const coordinates = element.coordinates;
        for (let i = 0; i < coordinates.length; i++) {
            pointsArray.push(new Vector3(xScale(coordinates[i][1]),0.5, yScale(coordinates[i][0])));
        }

        geometry.setFromPoints(pointsArray);
        // console.log(pointsArray[0])

        var line = new Line(geometry, material); 
        allTrackLines.push(line);
        // console.log(line)
    }
})
console.log(cnt)