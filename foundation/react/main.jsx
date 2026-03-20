import React from "react";
import { createRoot } from "react-dom/client";
import Dashboard from "./Dashboard";

const health = [
  { node: "q-a", state: "up", load: 0.31 },
  { node: "q-b", state: "up", load: 0.42 },
];

createRoot(document.getElementById("root")).render(<Dashboard health={health} />);
