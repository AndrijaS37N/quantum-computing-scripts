"""
IBM: Example showing how to use Qiskit at level 0 (novice).
See level 1 if you would like to understand how to compile
Note: if you have only cloned the Qiskit repository but not
used `pip install`, the examples only work from the root directory.
"""

import time
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, QISKitError
from qiskit import available_backends, execute, register
from qiskit.tools.visualization import circuit_drawer, plot_histogram

try:
    import quantum_scripts.Qconfig as Qconfig

    register(Qconfig.APItoken, Qconfig.config['url'])
except:
    print("""WARNING: There's no connection with the API for remote backends.
             Have you initialized a Qconfig.py file with your personal token?
             For now, there's only access to local simulator backends...""")
try:
    # create a quantum and classical register
    qr = QuantumRegister(2)
    cr = ClassicalRegister(2)

    # making first circuit: bell state
    qc1 = QuantumCircuit(qr, cr)
    qc1.h(qr[0])
    qc1.cx(qr[1], qr[0])
    qc1.measure(qr, cr)

    # making another circuit: superpositions
    qc2 = QuantumCircuit(qr, cr)
    qc2.h(qr)
    qc2.measure(qr, cr)

    # setting up the backend
    print("\n(Local Backends)")
    print(available_backends({'local': True}))

    # runing the job
    local_sim = "local_qasm_simulator"
    job_sim = execute([qc1, qc2], local_sim)
    sim_result = job_sim.result()
    print("\nRuning simulation on:", local_sim)

    # show the results
    print("\nSimulation: ", sim_result)
    print(sim_result.get_counts(qc1))
    print(sim_result.get_counts(qc2))

    # see a list of available remote backends
    print("\n(Remote Backends)")
    print(available_backends({'local': False}))

    # showing off the circuits
    diagram_1 = circuit_drawer(qc1, filename='q3a_diagram.png')
    diagram_2 = circuit_drawer(qc2, filename='q3b_diagram.png')
    diagram_1.show()
    diagram_2.show()
    print("Ignore the pdflatex warning.")

    # compile and run on a real device backend
    try:
        # select least busy available device and execute.
        # least_busy_device = least_busy(available_backends())
        # print("Running on current least busy device:", least_busy_device)

        # my own selection
        selected_machine = "ibmqx4"
        print("\nRunning on:", selected_machine)
        print("\nTimer:")

        # running the job
        # job_exp = execute([qc1, qc2], backend=least_busy_device, shots=1024, max_credits=10)
        job_exp = execute(qc1, backend=selected_machine, shots=1024, max_credits=10)

        lapse = 0
        interval = 5
        while not job_exp.done:
            print('Status @ {} seconds'.format(interval * lapse))
            print(job_exp.status)
            time.sleep(interval)
            lapse += 1

        print(job_exp.status)
        exp_result = job_exp.result()

        # show the results
        print("\nExperiment: ", exp_result)
        print(exp_result.get_counts(qc1))
        # print(exp_result.get_counts(qc2))
        plot_histogram(exp_result.get_counts(qc1))
    except:
        print("All devices are currently unavailable.")
except QISKitError as ex:
    print('There was an error in the circuit! Error = {}'.format(ex))
