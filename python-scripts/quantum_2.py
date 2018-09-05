from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.tools.visualization import circuit_drawer

def build_bell_circuit():
    """IBM: Returns a circuit putting 2 qubits in the Bell state."""
    q = QuantumRegister(2)
    c = ClassicalRegister(2)
    qc = QuantumCircuit(q, c)
    # made changes here
    qc.h(q[0])
    qc.cx(q[0], q[1])
    qc.measure(q, c)
    return qc


# create the circuit and display it
bell_circuit = build_bell_circuit()
diagram = circuit_drawer(bell_circuit, filename='./q2_diagram.png')
diagram.show()
print(
    "Ignore the pdflatex warning.\nMore on: https://github.com/Qiskit/qiskit-terra/blob/master/examples/python/hello_quantum.py")
