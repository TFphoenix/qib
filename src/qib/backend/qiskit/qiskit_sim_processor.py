from itertools import combinations

from qib.backend import QuantumProcessor, ProcessorConfiguration, GateProperties
from qib.backend.qiskit import QiskitSimExperiment, QiskitSimOptions
from qib.circuit import Circuit


class QiskitSimProcessor(QuantumProcessor):
    _applicant_id_count = 1000

    def __init__(self, access_token: str):
        self.url: str = "https://wmiqc-api.wmi.badw.de/1/qiskitSimulator"
        self.access_token: str = access_token

    @staticmethod
    def configuration() -> ProcessorConfiguration:
        return ProcessorConfiguration(
            backend_name="QiskitSimulator",
            backend_version="1.0.0",
            n_qubits=3,
            basis_gates=['x', 'sx', 'rz', 'cz'],
            gates=[
                GateProperties('x', [[0]]),
                GateProperties('sx', [[0]]),
                GateProperties('rz', [[0]], ['theta']),
                GateProperties('cz', [[1,0], [2,0]])
            ],
            coupling_map=None,
            local=False,
            simulator=True,
            conditional=False,
            open_pulse=False
        )

    def submit_experiment(self, circ: Circuit, options: QiskitSimOptions = None) -> QiskitSimExperiment:
        if options is None:
            options = QiskitSimOptions.default()

        self._validate_experiment(circ, options)
        experiment = QiskitSimExperiment(circ, options)
        self._send_experiment(experiment)
        return experiment

    def _validate_experiment(self, circ: Circuit, options: QiskitSimOptions):
        # check that the number of shots is not exceeded
        if options.shots > self.configuration().max_shots:
            raise ValueError("Number of shots exceeds maximum allowed number of shots.")

        qubits_set = set()
        # clbits_set = set() # TODO: See if it's necessary
        for gate in circ.gates:
            gate_openQASM = gate.as_openQASM()
            gate_name = gate_openQASM['name']
            gate_qubits = gate_openQASM['qubits']
            gate_params = gate_openQASM['params'] if 'params' in gate_openQASM else []
            qubits_set.update(gate_qubits)
            # clbits_set.update(gate_openQASM['memory'] if gate_name == 'measure' else []) # TODO: See if it's necessary
            
            if gate_name != 'measure':
                # check that the gate is supported by the processor
                if gate_name not in self.configuration().basis_gates:
                    raise ValueError(f"Gate {type(gate)} is not supported by the processor.")
                
                # check that the used qubits are configured for the gate
                gate_properties = self.configuration().get_gate_by_name(gate_name)
                if gate_properties is None:
                    raise ValueError(f"Gate {type(gate)} is not configured by the processor.")
                if not gate_properties.check_qubits(gate_qubits):
                    raise ValueError(f"Gate {type(gate)} is not configured for the used qubits.")
                if not gate_properties.check_params(gate_params):
                    raise ValueError(f"Gate {type(gate)} is not configured for the used parameters.")

            # check that gates are performed only on coupled qubits
            if len(gate_qubits) > 1:
                qubit_pairs = list(combinations(gate_qubits, 2))
                for qubit_pair in qubit_pairs:
                    if qubit_pair not in self.configuration().coupling_map:
                        raise ValueError(f"Gate {type(gate)} is not performed on coupled qubits.")
            
        # check that the number of qubits is adequate
        if len(qubits_set) > self.configuration().n_qubits \
        and min(qubits_set) >= 0 \
        and max(qubits_set) < self.configuration().n_qubits:
            raise ValueError("Number of qubits exceeds maximum allowed number of qubits, or indexes are incorrect.")

    def _send_experiment(self, experiment: QiskitSimExperiment):
        # TODO: build HTTP request
        # TODO: send HTTP request via the HTTP PUT endpoint
        pass
