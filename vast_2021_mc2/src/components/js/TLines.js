import * as THREE from 'three';

// import Stats from 'three/addons/libs/stats.module.js';
// import { GPUStatsPanel } from 'three/addons/utils/GPUStatsPanel.js';

// import { GUI } from 'three/addons/libs/lil-gui.module.min.js';
// import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// import { Line2 } from 'three/examples/jsm/lines/Line2.js';
// import { LineMaterial } from 'three/examples/jsm/lines/LineMaterial.js';
// import { LineGeometry } from 'three/examples/jsm/lines/LineGeometry.js';
// import * as GeometryUtils from 'three/addons/utils/GeometryUtils.js';
// import * as d3 from "d3";
import trackJson from './tracks.json';
let line,matLine;
// let insetWidth, insetHeight;
export const allTrackLines = []
trackJson.forEach(element => {
    const pointsArray = [];
    const coordinates = element.coordinates;
    // let xScale = d3.scaleLinear().domain([20,30]).range([-1035,1095]);//地图太小了 比例尺放大
    // let yScale = d3.scaleLinear().domain([30,40]).range([-1290,840]);
    if (element.date == "2014-01-06" && element.carID == "1") {
        for (let i = 0; i < coordinates.length; i++) {
            pointsArray.push(new THREE.Vector3((coordinates[i][0]/6),5,(coordinates[i][1]/6)));

        }
        console.log(pointsArray.length)
    }
    // const colors = new THREE.Color();
    const geometry = new THREE.BufferGeometry();
    geometry.setFromPoints(pointsArray);
    // geometry.setColors(colors);
    // console.log("here");
    // matLine = new LineMaterial({

    //     color: 0xffffff,
    //     linewidth: 5, // in world units with size attenuation, pixels otherwise
    //     vertexColors: true,

    //     //resolution:  // to be set by renderer, eventually
    //     dashed: false,
    //     alphaToCoverage: true,

    // });
    matLine = new THREE.LineBasicMaterial({color: 0x0000ff,linewidth:25});
    
    // line = new Line2(geometry, matLine);
    // line.computeLineDistances();
    // line.scale.set(1, 1, 1);
    // allTrackLines.push(line);
    // insetWidth = window.innerHeight / 4; // square
    // insetHeight = window.innerHeight / 4;
    // matLine.resolution.set( insetWidth, insetHeight ); // resolution of the inset viewport
    line = new THREE.Line( geometry, matLine );
    allTrackLines.push(line);
    // console.log(allTrackLines)
});

// var loader = new FontLoader();

// loader.load( 'Microsoft YaHei_Regular.json', function ( font ) {

//     let textGeometry = new TextGeometry('???????????????', {
//         font: font,
//         size: 200,
//         height: 0.1,
//         curveSegments: 12,
//     });
//     let mesh = new Mesh(textGeometry, font2dMaterial);
//     mesh.position.set(-8, 0, 0);
//     allBaseObject.push(mesh)
//     console.log(allBaseObject)
// });
