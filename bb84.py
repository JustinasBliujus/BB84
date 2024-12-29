from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np

# Parameters
num_qubits = 20  # Number of qubits to transmit

# Step 1: Alice generates random bits and bases
alice_bits = np.random.randint(2, size=num_qubits)  # Alice generates random bits (0 or 1)
alice_bases = np.random.randint(2, size=num_qubits)  # Alice randomly selects bases (0 = Z-basis, 1 = X-basis)

# Alice's polarizations based on the bases (0 = Z-basis, 1 = X-basis)
# For Z-basis: 0 = Horizontal (|0⟩), 1 = Vertical (|1⟩)
# For X-basis: 0 = Diagonal (|+⟩), 1 = Anti-diagonal (|-⟩)
print("Step 1: Alice's generated data")
print(f"Alice's bits:        {alice_bits}")
print(f"Alice's bases:       {alice_bases}")

# Step 2: Alice prepares and transmits qubits
# Alice encodes the bits in qubits according to her chosen basis
circuits = []
for i in range(num_qubits):
    qc = QuantumCircuit(1, 1)  # Create a single qubit circuit
    if alice_bits[i] == 1:
        qc.x(0)  # Encode bit 1 by applying an X gate
    if alice_bases[i] == 1:
        qc.h(0)  # Apply Hadamard gate for X-basis (diagonal states)
    circuits.append(qc)

# Step 3: Eve intercepts the qubits and measures them in a random basis
eve_bases = np.random.randint(2, size=num_qubits)  # Eve chooses a random basis (0 or 1)
print("\nStep 3: Eve's interception")
print(f"Eve's bases:         {eve_bases}")

eavesdrop_results = []  # To store Eve's measured bits
eve_tampered_circuits = []  # To store the tampered circuits with re-encoded qubits

# Eve intercepts and measures each qubit in a random basis
for i, qc in enumerate(circuits):
    eve_basis = eve_bases[i]  # Eve's chosen basis for this qubit
    qc_copy = qc.copy()  
    if eve_basis == 1:
        qc_copy.h(0)  # If Eve chooses the X-basis, apply Hadamard (to switch to Diagonal or Anti-diagonal)
    qc_copy.measure(0, 0)  # Measure the qubit in Eve's basis
    result = AerSimulator().run(qc_copy).result()  # Simulate the result of Eve's measurement
    counts = result.get_counts()  # Get the measurement result
    measured_bit = int(max(counts, key=counts.get))  # The bit Eve measures (0 or 1)
    eavesdrop_results.append(measured_bit)  # Store the measured bit

    # Eve re-encodes the qubit into her chosen basis
    eve_qc = QuantumCircuit(1, 1)
    if measured_bit == 1:
        eve_qc.x(0)  # Re-encode bit 1 if Eve measured 1
    if eve_basis == 1:
        eve_qc.h(0)  # Apply Hadamard for X-basis (diagonal states)
    eve_tampered_circuits.append(eve_qc)  # Store the re-encoded qubit for Bob

# Step 4: Bob chooses random bases and measures the qubits tampered by Eve
bob_bases = np.random.randint(2, size=num_qubits)  # Bob chooses random bases (0 = Z, 1 = X)
print("\nStep 4: Bob's measurement")
print(f"Bob's bases:         {bob_bases}")

bob_results = []  # To store Bob's measured bits

# Bob measures the tampered qubits (after Eve's interference)
for i, qc in enumerate(eve_tampered_circuits):
    if bob_bases[i] == 1:
        qc.h(0)  # If Bob chooses X-basis, apply Hadamard (diagonal states)
    qc.measure(0, 0)  # Bob measures the qubit in his chosen basis
    result = AerSimulator().run(qc).result()  # Simulate the result of Bob's measurement
    counts = result.get_counts()  # Get the measurement result
    measured_bit = int(max(counts, key=counts.get))  # The bit Bob measures (0 or 1)
    bob_results.append(measured_bit)  

# Step 5: Basis reconciliation
# Alice and Bob compare their bases to find matching indices
matching_bases = alice_bases == bob_bases
shared_key_indices = np.where(matching_bases)[0]  # Indices where Alice and Bob have matching bases
alice_shared_key = alice_bits[shared_key_indices]  # Alice's shared key bits
bob_shared_key = np.array(bob_results)[shared_key_indices]  # Bob's shared key bits

# Step 6: Detecting discrepancies and possible eavesdropping
# Errors are detected when Alice's and Bob's bits do not match
errors = alice_shared_key != bob_shared_key
error_rate = np.mean(errors)  # Calculate the error rate (QBER)

# Display the shared keys and detect Eve's interference
print("\nShared Key Comparison (Detecting Eve):")
print(f"{'Alice Shared Key':<20} {'Bob Shared Key':<20} {'Eve Detected':<12}")
print("-" * 55)
for i in range(len(shared_key_indices)):
    eve_detected = "Yes" if errors[i] else "No"  # If there's a mismatch, Eve is detected
    print(f"{alice_shared_key[i]:<20} {bob_shared_key[i]:<20} {eve_detected:<12}")

# Final Results
print("\nFinal Results:")
print(f"Alice's raw key:         {''.join(map(str, alice_bits))}")
print(f"Shared key (Alice):      {''.join(map(str, alice_shared_key))}")
print(f"Shared key (Bob):        {''.join(map(str, bob_shared_key))}")
print(f"Error rate (QBER):       {error_rate:.2%}")

# If the error rate is above a certain threshold, consider potential eavesdropping
if error_rate > 0.11:  # BB84 security threshold
    print("\nPotential eavesdropping detected!")
else:
    print("\nKey exchange successful and secure.")
