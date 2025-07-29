# BB84 Quantum Key Distribution Simulation (with Eavesdropping)

- This repository contains a complete implementation of the **BB84 Quantum Key Distribution (QKD)** protocol using **Qiskit**. 
- This was a part of coursework in Fundamentals of Quantum Computing
  
---

## Files

- `bb84.py` — Main Python script implementing the BB84 protocol in Qiskit.
- `bb84.pdf` — Written report detailing the implementation, theoretical background, diagrams, and analysis.

---

## Protocol Steps

### 1. Alice's Qubit Preparation
- Alice generates:
  - Random bits: `0` or `1`
  - Random bases: Z-basis (`|0⟩`, `|1⟩`) or X-basis (`|+⟩`, `|−⟩`)
- She encodes her bits in quantum states accordingly.

### 2. Eve Intercepts (Optional Eavesdropping)
- Eve randomly chooses bases and measures the qubits.
- She re-encodes and sends qubits to Bob.
- Her interference introduces detectable errors.

### 3. Bob's Measurement
- Bob randomly chooses measurement bases.
- He measures each qubit received from Eve (or directly from Alice in an ideal case).

### 4. Basis Reconciliation
- Alice and Bob publicly compare their bases.
- Only bits where bases match are kept to form the **raw key**.

### 5. Error Detection
- Alice and Bob compare part of their shared key.
- High error rate (QBER) indicates potential eavesdropping.

---
