import { createRouter, createWebHistory } from "vue-router";
import ego from "../components/vis/Ego.vue";
import unity from "../components/vis/Unity.vue";
import hierarchy from "../components/vis/Hierarchy.vue";
import parallel from "../components/vis/Parallel.vue";
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/ego",
      component: ego,
    },
    {
      path: "/unity",
      component: unity,
    },
    {
      path: "/hierarchy",
      component: hierarchy,
    },
    {
      path: "/parallel",
      component: parallel,
    },
  ],
});

export default router;
