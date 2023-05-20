# mini json process

```
let nodes, links, source, target, cneter;

let entities = new Set([
  "Mar de la Vida OJSC",
  "979893388",
  "Oceanfront Oasis Inc Carrie",
  "8327",
]);

// mini json 的处理过程如下

let data, first, second, first_link, second_link;
d3.json("MC1.json").then((d) => {
  nodes = d.nodes;
  links = d.links;
  data = {};
  Array.from(entities).forEach((ego) => {
    first = new Set();
    first_link = new Set();
    second = new Set();
    second_link = new Set();
    // 第一遍遍历 links，获取一阶邻居
    links.forEach((link) => {
      source = link.source.toString();
      target = link.target.toString();
      if (source == ego) {
        first.add(target);
        first_link.add({
          source: source,
          target: target,
        });
      }
      if (target == ego) {
        first.add(source);
        first_link.add({
          source: source,
          target: target,
        });
      }
    });
    // 第二遍遍历 links，获取不与 center 直接连线的二阶邻居
    links.forEach((link) => {
      source = link.source.toString();
      target = link.target.toString();
      if (
        // 不与 center 直接相连
        source !== ego &&
        target !== ego &&
        // 且不能两端都在一阶中
        !(first.has(source) && first.has(target))
      ) {
        if (first.has(source)) {
          second.add(target);
          second_link.add({
            source: source,
            target: target,
          });
        }
        if (first.has(target)) {
          second.add(source);
          second_link.add({
            source: source,
            target: target,
          });
        }
      }
    });
    data[ego] = {
      first: Array.from(first),
      second: Array.from(second),
      first_link: Array.from(first_link),
      second_link: Array.from(second_link),
    };
  });
  console.log(data);
});

// 预览mini json
d3.json("mini.json").then((d) => {
  console.log(d);
});
```
