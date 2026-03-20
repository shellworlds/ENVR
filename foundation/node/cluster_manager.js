const nodes = [
  { id: "q-a", status: "up", load: 0.3 },
  { id: "q-b", status: "up", load: 0.7 },
  { id: "q-c", status: "down", load: 0.0 },
];

function selectLeastLoaded(activeOnly = true) {
  return nodes
    .filter((n) => (activeOnly ? n.status === "up" : true))
    .sort((a, b) => a.load - b.load)[0];
}

console.log(selectLeastLoaded());
