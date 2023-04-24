<template>
  <div id="scene-container" ref="sceneContainer"></div>
</template>

<script>
import { useRef, useEffect, useCallback, useState } from 'react'
import * as THREE from 'three'
import * as D3 from 'd3'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'

export default {
  name: 'HelloWorld',
  data () {
    return {
      container: null,
      scene: null,
      camera: null,
      controls: null,
      renderer: null,
      stats: null
    }
  },
  methods: {
    init () {
      useEffect(() => {
        page.current.appendChild(render.domElement);
        initScene();
        initLight();
        initGeom();
        renderScene();
      }, [])

      useEffect(() => {
        bindEvent();
      }, [])

      const bindEvent = () => {
        window.addEventListener('mousemove', (event) => {
          const pointer = new THREE.Vector2();
          // 像素坐标=>规范化设备坐标系 [-1,1]
          pointer.x = (event.clientX / window.innerWidth) * 2 - 1;
          pointer.y = - (event.clientY / window.innerHeight) * 2 + 1;

          // 获取鼠标点击的位置生成射线
          const raycaster = new THREE.Raycaster();
          raycaster.setFromCamera(pointer, camera);
          // 获取射线相交的物体集合
          // debugger
          const intersects = raycaster.intersectObjects(mapContainer.children, true);
          if (intersects.length) {
            const pcickedProvice = intersects[0].object;
            // 选中了新的省份
            if (lastPickedProvince.current?.properties !== pcickedProvice.properties) {
              // 上次选中的恢复半透明
              if (lastPickedProvince.current) {
                lastPickedProvince.current.material.opacity = 0.5
              }
              pcickedProvice.material.opacity = 1;  // 新选中的设置为不透明
              lastPickedProvince.current = pcickedProvice;
            }
          } else { // 鼠标移开地图，之前选中的省份回复半透明
            if (lastPickedProvince.current) {
              lastPickedProvince.current.material.opacity = 0.5
            }
            lastPickedProvince.current = null;
          }
        }, false)
      }
      const initScene = useCallback(() => {
        render.setSize(page.current.offsetWidth, page.current.offsetHeight); // 渲染器设置尺寸
        // 设置背景颜色
        render.setClearColor(new THREE.Color(0x000000)); // 设置背景颜色和透明度
        render.shadowMap.enabled = true; // 渲染器允许渲染阴影⭐

        /**
         * 设置摄像机的属性
         */
        camera.aspect = (page.current.offsetWidth / page.current.offsetHeight) // 摄像机设置屏幕宽高比
        camera.fov = 45; // 摄像机的视角
        camera.near = 0.01; // 近面距离
        camera.far = 1001; // 远面距离
        camera.position.set(2, 2, 200) // 设置摄像机在threejs坐标系中的位置
        camera.lookAt(0, 0, 0) // 摄像机的指向
        camera.updateProjectionMatrix(); // 更新摄像机投影矩阵,在任何参数被改变以后必须被调用

      }, [render, scence])

      // 初始化环境光
      const initLight = () => {
        const ambLight = new THREE.AmbientLight('#ffffff', 0.3) // 基本光源
        /**
         * 设置聚光灯相关的的属性，详情见P54
         */
        const spotLight = new THREE.SpotLight(0xFFFFFF); // 聚光灯
        spotLight.position.set(40, 200, 10);
        spotLight.castShadow = true; // 只有该属性为true时，该点光源允许产生阴影，并且下列属性可用
        scence.add(ambLight, spotLight); // 向场景中添加光源
      }

      // 初始化地理数据集
      const initGeom = () => {
        // 加载中国地区的geoJson数据集
        const fileLoader = new THREE.FileLoader();
        fileLoader.load(
            'https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json',
            (data) => {
              const chinaJson = JSON.parse(data)
              handleData(chinaJson)
            }
        )
      }

      // 处理GeoJson data
      const handleData = (jsonData) => {
        const feaureList = jsonData.features;
        feaureList.forEach((feature) => { // 每个feature都代表一个省份
          const province = new THREE.Object3D;
          province.properties = feature.properties.name // 省份名称
          province.name = feature.properties.name // 省份名称
          const coordinates = feature.geometry.coordinates // 省份坐标信息
          if (feature.geometry.type === 'MultiPolygon') {
            coordinates.forEach((coord) => {
              coord.forEach((coordinate) => {
                const extrudeMesh = creatDepthPolygon(coordinate)
                extrudeMesh.properties = feature.properties.name
                province.add(extrudeMesh)
              })
            })
          }
          if (feature.geometry.type === 'Polygon') {
            coordinates.forEach((coordinate) => {
              const extrudeMesh = creatDepthPolygon(coordinate)
              extrudeMesh.properties = feature.properties.name
              province.add(extrudeMesh)
            })
          }
          mapContainer.add(province)
        })
        scence.add(mapContainer)
      }

      // 创建三维多边形
      const creatDepthPolygon = (coordinate) => {
        const shape = new THREE.Shape();

        coordinate.forEach((item, index) => { // 每一个item都是MultiPolygon中的一个polygon
          const [x_XYZ, y_XYZ] = handleProj(item)
          if (index === 0) {
            shape.moveTo(x_XYZ, -y_XYZ)
          } else {
            shape.lineTo(x_XYZ, -y_XYZ)
          }
        })

        const geometry = new THREE.ExtrudeBufferGeometry(shape, { depth: 1, bevelEnabled: false, })
        const material = new THREE.MeshBasicMaterial({
          color: new THREE.Color(Math.random() * 0xffffff), // 每个省随机赋色
          transparent: true,
          opacity: 0.5
        })
        return new THREE.Mesh(geometry, material)
      }

      // 渲染器执行渲染
      const renderScene = useCallback(() => {
        timer.current = window.requestAnimationFrame(() => renderScene())
        controls.update();
        render.render(scence, camera);
      }, [render])

      // // set container
      // this.container = this.$refs.sceneContainer
      //
      // // add stats
      // this.stats = new Stats()
      // this.container.appendChild(this.stats.dom)
      //
      // // add camera
      // const fov = 60 // Field of view
      // const aspect = this.container.clientWidth / this.container.clientHeight
      // const near = 0.1 // the near clipping plane
      // const far = 30 // the far clipping plane
      // const camera = new THREE.PerspectiveCamera(fov, aspect, near, far)
      // camera.position.set(0, 5, 10)
      // this.camera = camera
      //
      // // create scene
      // this.scene = new THREE.Scene()
      // this.scene.background = new THREE.Color('skyblue')
      //
      // // add lights
      // const ambientLight = new THREE.HemisphereLight(
      //   0xffffff, // bright sky color
      //   0x222222, // dim ground color
      //   1 // intensity
      // )
      // const mainLight = new THREE.DirectionalLight(0xffffff, 4.0)
      // mainLight.position.set(10, 10, 10)
      // this.scene.add(ambientLight, mainLight)
      //
      // // add controls
      // this.controls = new OrbitControls(this.camera, this.container)
      //
      // // create renderer
      // this.renderer = new THREE.WebGLRenderer({ antialias: true })
      // this.renderer.setSize(this.container.clientWidth, this.container.clientHeight)
      // this.renderer.setPixelRatio(window.devicePixelRatio)
      // this.renderer.gammaFactor = 2.2
      // this.renderer.outputEncoding = THREE.sRGBEncoding
      // this.renderer.physicallyCorrectLights = true
      // this.container.appendChild(this.renderer.domElement)
      //
      // // set aspect ratio to match the new browser window aspect ratio
      // this.camera.aspect = this.container.clientWidth / this.container.clientHeight
      // this.camera.updateProjectionMatrix()
      // this.renderer.setSize(this.container.clientWidth, this.container.clientHeight)
      //
      // const loader = new GLTFLoader()
      //
      // loader.load(
      //   '/three-assets/RobotExpressive.glb',
      //   gltf => {
      //     this.scene.add(gltf.scene)
      //   },
      //   undefined,
      //   undefined
      // )
      //
      // this.renderer.setAnimationLoop(() => {
      //   this.render()
      // })
    },
    render () {
      this.renderer.render(this.scene, this.camera)
      this.stats.update()
    }
  },
  mounted () {
    this.init()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
#scene-container {
  height: 100%;
}
</style>
