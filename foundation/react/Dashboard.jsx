import React from "react";

export default function Dashboard({ health }) {
  return (
    <section>
      <h2>ENVR Quantum Cluster Dashboard</h2>
      <ul>
        {health.map((h) => (
          <li key={h.node}>{h.node}: {h.state} / load={h.load}</li>
        ))}
      </ul>
    </section>
  );
}
