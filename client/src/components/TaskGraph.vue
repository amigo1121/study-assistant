<script lang="ts" setup>
import vis from "vis-network/dist/vis-network.min.js";
import { onMounted, ref, defineProps, nextTick } from "vue";
import axios from "axios";
import { API_URL } from "@/utils/config";
import { useAuthStore } from "@/stores/auth";
import { capitalize } from "@/utils/datetime";
const authStore = useAuthStore();
const props = defineProps({
  assignment_id: {
    type: Number,
    required: true,
  },
});

const nodes = ref([]);
const edges = ref([]);
const graph_edges = ref(null);
const graph_nodes = ref(null);
const options = ref({
  edges: {
    arrows: "to",
  },
});
const graph_data = ref({
  edges: graph_edges,
  nodes: graph_nodes,
});
let network;
const graphContainer = ref(null);
function centering() {
  network.fit({
    animation: {
      duration: 1000,
      easingFunction: "easeInOutQuad",
    },
  });
}

async function fetchData() {
  const config = {
    headers: {
      Authorization: `Bearer ${authStore.accessToken}`,
    },
  };
  await axios
    .get(API_URL + `/task/nodes/${props.assignment_id}`, config)
    .then((response) => {
      nodes.value = response.data;
    })
    .catch((error) => {
      console.log(error);
    });

  await axios
    .get(API_URL + `/task/edges/${props.assignment_id}`, config)
    .then((response) => {
      edges.value = response.data;
    })
    .catch((error) => {
      console.log(error);
    });
}

function getColor(task) {
  switch (task.status) {
    case "NOT_STARTED":
      return "#BDBDBD";
    case "IN_PROGRESS":
      return "#fccc55";
    case "COMPLETE":
      return "#6ebe71";
    default:
      return "#6ebe71";
  }
}
function updateNodes() {
  nodes.value = nodes.value.map((e) => {
    return {
      id: e.id,
      label: e.title,
      color: { background: getColor(e), border: getColor(e) },
    };
  });
}

function updateUI() {
  edges.value = edges.value.map((e) => {
    return { from: e.from_id, to: e.to_id };
  });
  updateNodes();

  graph_edges.value = new vis.DataSet(edges.value);
  graph_nodes.value = new vis.DataSet(nodes.value);

  network = new vis.Network(
    graphContainer.value,
    graph_data.value,
    options.value
  );
  centering();
}
onMounted(async () => {
  await fetchData();
  updateUI();
});

async function refresh() {
  await fetchData();
  updateUI();
}
</script>
<style scoped>
.mynetwork {
  width: 100%;
  height: 700px;
  border: 1px solid lightgray;
}
</style>
<template>
  <div class="mynetwork" ref="graphContainer"></div>
  <div class="flex gap-3 mt-3 justify-content-end">
    <Button @click="centering">Centering</Button>
    <Button @click="refresh" severity="success">Refresh</Button>
  </div>
</template>
