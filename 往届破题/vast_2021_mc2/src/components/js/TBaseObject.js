import { BoxGeometry, Color, Mesh, MeshStandardMaterial } from "three"

export const allBaseObject = []  // 返回所有基础模型

// 创建地面
export const box = new Mesh(
  new BoxGeometry(20, 20, 20),  // 设置立方体的大小
  new MeshStandardMaterial({   // 设置材质
    color: 'rgb(36, 172, 242)',  // 设置材质的颜色
    metalness: 0.5,   // 金属度 （1 最像金属，0 最不想金属）
    roughness: 0   // 粗糙度（0 最光滑，1 最粗糙）
  })
)
box.name = 'box'  // 设置模型 name

// 给模型添加鼠标移入事件
box.addEventListener("mouseenter", () => {
  box.material.color = new Color("#ff3366")  // 修改材质颜色为红色
})
// 给模型添加鼠标移除事件
box.addEventListener("mouseleave", () => {
  box.material.color = new Color("rgb(36, 172, 242)") // 恢复模型的材质
})


allBaseObject.push(box)  // 添加到模型数组