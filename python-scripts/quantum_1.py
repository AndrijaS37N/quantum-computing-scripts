from qiskit import ClassicalRegister, QuantumRegister
from qiskit import QuantumCircuit, execute
from qiskit.tools.visualization import circuit_drawer

# two quantum registers
q = QuantumRegister(2)
# two classical registers
c = ClassicalRegister(2)
# put the initiated registers onto the circuit
qc = QuantumCircuit(q, c)

qc.h(q[1])
qc.cx(q[0], q[1])
qc.measure(q, c)

job_sim = execute(qc, "local_qasm_simulator")
sim_result = job_sim.result()

print(sim_result.get_counts(qc))
image = circuit_drawer(qc, filename="./q1_diagram.png")
image.show()
print("Ignore the pdflatex warning.")
