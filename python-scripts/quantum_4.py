"""
IBM: Example showing how to use Qiskit at level 1 (intermediate).
In Qiskit 0.6 we will be working on a pass manager for level 2+ users
Note: if you have only cloned the Qiskit repository but not
used `pip install`, the examples only work from the root directory.
"""

# https://github.com/Qiskit/qiskit-terra/blob/master/examples/python/using_qiskit_core_level_1.py

import pprint
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, QISKitError
from qiskit import available_backends, compile, register, get_backend, least_busy
from qiskit.tools.visualization import circuit_drawer, plot_histogram

try:
    import quantum_scripts.Qconfig as Qconfig

    register(Qconfig.APItoken, Qconfig.config['url'])
except:
    print("""WARNING: There's no connection with the API for remote backends.
             Have you initialized a Qconfig.py file with your personal token?
             For now, there's only access to local simulator backends...""")
try:
    # create a quantum and classical register and giving a name
    qubit_reg = QuantumRegister(2, name='q')
    clbit_reg = ClassicalRegister(2, name='c')

    # making first circuit: bell state
    qc1 = QuantumCircuit(qubit_reg, clbit_reg, name="bell")
    qc1.h(qubit_reg[0])
    qc1.cx(qubit_reg[0], qubit_reg[1])
    qc1.measure(qubit_reg, clbit_reg)

    # making another circuit: superpositions
    qc2 = QuantumCircuit(qubit_reg, clbit_reg, name="superposition")
    qc2.h(qubit_reg)
    qc2.measure(qubit_reg, clbit_reg)

    # setting up the backend
    print("\n(Local Backends)")
    for backend_name in available_backends({'local': True}):
        backend = get_backend(backend_name)
        print(backend.status)

    my_backend_name = 'local_qasm_simulator'
    my_backend = get_backend(my_backend_name)
    print("\n(Local QASM Simulator Configuration)")
    pprint.pprint(my_backend.configuration)
    print("\n(Local QASM Simulator Calibration)")
    pprint.pprint(my_backend.calibration)
    print("\n(Local QASM Simulator Parameters)")
    pprint.pprint(my_backend.parameters)

    # compiling the job
    qobj = compile([qc1, qc2], my_backend)
    # Note: in the near future qobj will become an object

    # runing the job
    sim_job = my_backend.run(qobj)

    # getting the result
    sim_result = sim_job.result()

    # show the results
    print("\nSimulation:", sim_result)
    print(sim_result.get_counts(qc1))
    print(sim_result.get_counts(qc2))

    # showing off the circuits
    diagram_1 = circuit_drawer(qc1, filename='q4a_diagram.png')
    diagram_2 = circuit_drawer(qc2, filename='q4b_diagram.png')
    diagram_1.show()
    diagram_2.show()
    print("Ignore the pdflatex warning.\n")

    # compile and run the quantum program on a real device backend
    # see a list of available remote backends
    try:
        print("(Remote Backends)")
        for backend_name in available_backends({'local': False}):
            backend = get_backend(backend_name)
            s = backend.status
            print(s)

        # select least busy available device and execute
        # least_busy_device = least_busy(available_backends())
        # print("\nRunning on current least busy device:", least_busy_device)

        # my_backend = get_backend(least_busy_device)
        my_backend = get_backend("ibmqx4")

        print("\n(With Configuration)")
        pprint.pprint(my_backend.calibration)
        print("\n(With Calibration)")
        pprint.pprint(my_backend.calibration)
        print("\n(With Parameters)")
        pprint.pprint(my_backend.parameters)

        # compiling the job
        # I want to make it so the compile is only done once and the needing
        # a backend is optional
        qobj = compile([qc1, qc2], backend=my_backend, shots=1024, max_credits=10)

        # runing the job
        exp_job = my_backend.run(qobj)
        exp_result = exp_job.result()

        # show the results
        print("\nExperiment:", exp_result)
        print(exp_result.get_counts(qc1))
        print(exp_result.get_counts(qc2))
    except:
        print("All devices are currently unavailable.")
except QISKitError as ex:
    print('There was an error in the circuit! Error = {}'.format(ex))
