import {
    LineBasicMaterial,
    BufferGeometry,
    Vector3,
    Line,
    Color,
    MeshLambertMaterial,
    DoubleSide,
    Mesh
} from "three"
import {FontLoader} from "three/examples/jsm/loaders/FontLoader";
import {TextGeometry} from "three/examples/jsm/geometries/TextGeometry.js"
// import {Line2} from "three/examples/jsm/lines/Line2.js"
import abilbaJson from './Abila.json'
import * as d3 from "d3";
export const allBaseObject = []  // 返回所有基础模型

var material = new LineBasicMaterial( { color: 0xA5B1D2 , lineWidth: 20} );
/*
125版本就不再支持这个api了，如果还需要就用他的子类BufferGeometry。
var geometry = new THREE.Geometry();
*/

let xScale = d3.scaleLinear().domain([20,30]).range([-1035,1095]);
let yScale = d3.scaleLinear().domain([30,40]).range([-1290,840]);
abilbaJson.features.forEach(elem => {
    const geometry = new BufferGeometry();
    const pointsArray = [];
    if (elem.geometry != null) {
        const coordinates = elem.geometry.coordinates;
        for (let i = 0; i < coordinates.length; i++) {
            pointsArray.push(new Vector3(xScale(coordinates[i][0]), 0, -yScale(coordinates[i][1])));
        }
    }
    geometry.setFromPoints(pointsArray);

    var line = new Line( geometry, material );
    line.name = elem.properties.name  // 设置模型 name

// 给模型添加鼠标移入事件
    line.addEventListener("mouseenter", () => {
        line.material.color = new Color("#3366cc")  // 修改材质颜色为红色
        console.log(line.name)
    })

    // 给模型添加鼠标移除事件
    line.addEventListener("mouseleave", () => {
        line.material.color = new Color(0xA5B1D2) // 恢复模型的材质
    })
    allBaseObject.push(line);  // 添加到模型数组
})

var font2dMaterial = new MeshLambertMaterial({
    color: 0x912CEE,
    side: DoubleSide
});

var loader = new FontLoader();

loader.load( 'Microsoft YaHei_Regular.json', function ( font ) {

    let textGeometry = new TextGeometry('您好,three.js！', {
        font: font,
        size: 200,
        height: 0.1,
        curveSegments: 12,
    });
    let mesh = new Mesh(textGeometry, font2dMaterial);
    mesh.position.set(-8, 0, 0);
    allBaseObject.push(mesh)
});
