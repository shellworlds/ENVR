/**
 * Quantum JV Platform - React Quantum Component
 * React component for quantum circuit visualization
 */

import React, { useState, useEffect } from 'react';
import './QuantumComponent.css';

const QuantumComponent = ({ circuitData, onCircuitUpdate }) => {
  const [qubits, setQubits] = useState(4);
  const [gates, setGates] = useState([]);
  const [measurements, setMeasurements] = useState([]);
  
  // Initialize quantum circuit
  useEffect(() => {
    if (circuitData) {
      setQubits(circuitData.qubits || 4);
      setGates(circuitData.gates || []);
      setMeasurements(circuitData.measurements || []);
    }
  }, [circuitData]);
  
  const addGate = (gateType, qubitIndex, params = {}) => {
    const newGate = {
      id: Date.now(),
      type: gateType,
      qubit: qubitIndex,
      params,
      timestamp: new Date().toISOString()
    };
    
    const updatedGates = [...gates, newGate];
    setGates(updatedGates);
    
    if (onCircuitUpdate) {
      onCircuitUpdate({
        qubits,
        gates: updatedGates,
        measurements
      });
    }
  };
  
  const renderQubitLine = (qubitIndex) => {
    const qubitGates = gates.filter(gate => gate.qubit === qubitIndex);
    
    return (
      <div className="qubit-line" key={qubitIndex}>
        <div className="qubit-label">Q{qubitIndex}</div>
        <div className="qubit-timeline">
          {qubitGates.map(gate => (
            <div 
              className={`gate ${gate.type}`}
              key={gate.id}
              title={`${gate.type} gate on Q${qubitIndex}`}
            >
              {gate.type.toUpperCase()}
            </div>
          ))}
        </div>
      </div>
    );
  };
  
  return (
    <div className="quantum-component">
      <div className="circuit-header">
        <h3>Quantum Circuit Visualization</h3>
        <div className="circuit-controls">
          <button onClick={() => addGate('H', 0)}>Add H Gate</button>
          <button onClick={() => addGate('X', 1)}>Add X Gate</button>
          <button onClick={() => addGate('CNOT', 0, {target: 1})}>
            Add CNOT
          </button>
          <input 
            type="number" 
            value={qubits}
            onChange={(e) => setQubits(parseInt(e.target.value))}
            min="1"
            max="10"
          />
        </div>
      </div>
      
      <div className="circuit-visualization">
        {Array.from({length: qubits}).map((_, index) => 
          renderQubitLine(index)
        )}
      </div>
      
      <div className="circuit-info">
        <h4>Circuit Information</h4>
        <p>Qubits: {qubits}</p>
        <p>Total Gates: {gates.length}</p>
        <p>Measurements: {measurements.length}</p>
      </div>
    </div>
  );
};

export default QuantumComponent;
